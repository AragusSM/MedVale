import os
from neo4j import GraphDatabase
import sys
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
import pandas as pd
import json
import PyPDF2
import docx
import re
import time

# Neo4j Connection Setup
NEO4J_URI = "bolt://localhost:7687"  # Adjust if using remote DB
NEO4J_USER = "neo4j"
NEO4J_PASS = "password"
debug = True

api_key = "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"

# Initialize the text splitter
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)


class GraphDatabaseHandler:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

    def close(self):
        self.driver.close()

    def create_node(self, label, properties):
        # Sanitize label
        safe_label = re.sub(r"[^a-zA-Z0-9_]", "_", label)
        query = f"MERGE (n:{safe_label} {{name: $name}})"
        with self.driver.session() as session:
            session.run(query, name=properties.get("name"))

    def create_relationship(self, from_node, to_node, relation):
        # Sanitize relationship name for Cypher compatibility
        safe_relation = re.sub(r"[^a-zA-Z0-9_]", "_", relation)
        query = f"""
        MATCH (a {{name: $from_id}}), (b {{name: $to_id}})
        MERGE (a)-[r:{safe_relation}]->(b)
        """
        with self.driver.session() as session:
            session.run(query, from_id=from_node, to_id=to_node)


db = GraphDatabaseHandler()

# Ollama AI Model for Concept Extraction
os.environ["OPENAI_API_KEY"] = api_key
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
llm = ChatOpenAI(model="deepseek/deepseek-r1-0528:free", base_url=os.environ["OPENAI_API_BASE"])

# Define system and human prompt
system_prompt = SystemMessagePromptTemplate.from_template(
    """You are a medical expert specializing in technical medical terminology extraction.
    Your task is to analyze text and extract ONLY specific medical terms, not general words.
    Return results ONLY as a JSON array - no explanations or other text should be included."""
)

human_prompt = HumanMessagePromptTemplate.from_template(
    """
    TEXT:
            {input_text}
            
            Please analyze the text and identify ALL relevant medical concepts. For each concept:
            1. Identify the name of the concept
            2. Extract the concept text
            3. Assign a relevant subcategory (e.g., diagnosis, symptom, pathology, treatment, anatomy, etc.)
            4. Provide a brief description (2-3 sentences)
            
            Format your response as a JSON array of objects with the following structure:
            [
                {{
                    "name": "name of concept",
                    "concept": "concept text",
                    "subcategory": "relevant subcategory",
                    "description": "brief description"
                }},
                ...
            ]
            
            Only include the JSON array in your response, no additional text.
    """
)

# Combine into one template
chat_prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])


# Define a function that calls the LLM
def run_llm(input_text):
    formatted_messages = chat_prompt.format_messages(input_text=input_text)
    if debug:
        print("Sending to LLM:", formatted_messages)
    return llm.invoke(formatted_messages)


def extract_concepts(chunk, retries=3, delay=2):
    for attempt in range(retries):
        try:
            response = run_llm(chunk)
            print(response.content)

            concepts_raw = clean_json_response(response.content)
            concepts = json.loads(concepts_raw)

            for item in concepts:
                concept_name = item["name"].strip()
                concept_text = item["concept"].strip()
                subcategory = item["subcategory"].strip()
                description = item["description"].strip()

                db.create_node(concept_name, {"name": concept_name, "concept": concept_text,
                                              "subcategory": subcategory, "description": description})

            return  # success, exit the loop
        except Exception as e:
            print(f"[Chunk attempt {attempt + 1}] Error processing chunk: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                print(f"Skipping chunk after {retries} attempts.")


def process_chunk_and_store(chunk, retries=3, delay=2):
    for attempt in range(retries):
        try:
            response = run_llm(chunk)
            print(response.content)

            concepts_raw = clean_json_response(response.content)
            concepts = json.loads(concepts_raw)

            for item in concepts:
                concept_name = item["concept"].strip()
                related_to_name = item["related_to"].strip()
                relationship = item["relationship"].strip()

                db.create_node(concept_name, {"name": concept_name})
                db.create_node(related_to_name, {"name": related_to_name})
                db.create_relationship(concept_name, related_to_name, relationship)
            return  # success, exit the loop
        except Exception as e:
            print(f"[Chunk attempt {attempt + 1}] Error processing chunk: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                print(f"Skipping chunk after {retries} attempts.")


def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text


def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])


def ingest_document(file_path):
    if file_path.endswith(".pdf"):
        document_text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        document_text = extract_text_from_docx(file_path)
    else:
        with open(file_path, "r") as f:
            document_text = f.read()

    # Split the document into chunks
    chunks = splitter.split_text(document_text)
    for i, chunk in enumerate(chunks):
        print(f"\n--- Processing chunk {i + 1}/{len(chunks)} ---")
        extract_concepts(chunk)


def export_graph_to_csv():
    with db.driver.session() as session:
        nodes_query = "MATCH (n) RETURN n.name AS Id, labels(n)[0] AS Class, n.name AS Name"
        edges_query = "MATCH (a)-[r]->(b) RETURN a.name AS From, b.name AS To, type(r) AS Label"

        nodes_result = session.run(nodes_query)
        edges_result = session.run(edges_query)

        nodes_df = pd.DataFrame([dict(record) for record in nodes_result])
        nodes_df["Id"] = nodes_df["Name"].str.lower().str.replace(r"[^a-z0-9]+", "_", regex=True).str.strip("_")
        nodes_df["Name"] = nodes_df["Name"].str.replace(r"[_\-]+", " ", regex=True).str.title().str.strip()
        edges_df = pd.DataFrame([dict(record) for record in edges_result])
        edges_df["From"] = edges_df["From"].str.lower().str.replace(r"[^a-z0-9]+", "_", regex=True).str.strip("_")
        edges_df["To"] = edges_df["To"].str.lower().str.replace(r"[^a-z0-9]+", "_", regex=True).str.strip("_")
        nodes_df.to_csv("generated_nodes.csv", index=False)
        edges_df.to_csv("generated_edges.csv", index=False)


def clean_json_response(response):
    # Remove markdown formatting like ```json or ```
    cleaned = re.sub(r"```json|```", "", response).strip()

    # Optionally remove leading/trailing content if needed
    # You can also do stricter pattern matching here
    return cleaned


if __name__ == '__main__':
    # Example usage:
    ingest_document("lecture_notes.pdf")
    # ingest_document("lecture_notes.docx")
    # export_graph_to_csv()
