from flask import Flask, request, jsonify, render_template
import json
from source import microbiology as micro
import google.generativeai as genai
import pandas as pd
import random

# Initialize the SDK
genai.configure(api_key="AIzaSyAM7Ta6FzBExxBAKzzGlHXCdLohLC-bO9A")

app = Flask(__name__)

CLASSES_WITH_CHARACTERISTICS = ["Bacteria", "Coccus", "Bacillus", "Branched_Rods", "Mycobacteria", "Coccobacillus",
                                "Spirochete", "Fungus", "Virus", "PositiveSenseRNA", "NegativeSenseRNA", "DNAVirus",
                                "Parasite"]


def get_nodes(filename):
    node_data = pd.read_csv(filename)
    return node_data


def get_edges(filename):
    edge_data = pd.read_csv(filename)
    return edge_data


# check for edge labels
# edges = get_edges("micro_edges.csv")
# labels = edges["Label"]
# indices = labels.isna()
# final = labels[indices].index

def get_class_hierarchy(cls):
    """Retrieve the full class hierarchy for a given class."""
    return [base.__name__ for base in cls.mro() if base != object]


def node_gen(node_data):
    node_list = []
    for i in range(0, node_data.shape[0]):
        node = node_data.iloc[i]
        # Extract necessary fields
        id = node.get("Id")
        class_name = node.get("Class")  # E.g., "Bacteria"
        definition = node.get("Definition", "No definition provided")
        prop_list = node.get("PropList", "[]")  # Default to an empty list
        name = node.get("Name", "Unnamed Object")  # Default to a placeholder name
        picture = node.get("Picture", "")  # Default to an empty string if no picture is specified

        # Handle missing or malformed `PropList`
        if pd.isna(prop_list):  # Check for NaN
            prop_list = []
        elif isinstance(prop_list, str):  # Convert string representation of a list
            try:
                prop_list = eval(prop_list)
            except Exception as e:
                print(f"Error parsing properties for node {i}: {e}")
                prop_list = []

        # Validate class name
        if class_name not in CLASSES_WITH_CHARACTERISTICS:
            try:
                cls = getattr(micro, class_name)
                node_obj = cls(id, definition, name)

                # Set the picture using the set_picture() method
                pic_url = "/static/img/" + str(picture)
                node_obj.set_picture(pic_url)

                # Add all properties to the object using add_property()
                for prop in prop_list:
                    node_obj.add_property(prop)

                node_list.append(node_obj)
            except AttributeError:
                print(f"Class {class_name} not found in module")
            except TypeError as e:
                print(f"Error instantiating {class_name}: {e}")
            continue

        # Dynamically retrieve and instantiate the class
        try:
            cls = getattr(micro, class_name)
            # Use the first property if available, otherwise provide a default value
            first_property = prop_list[0] if prop_list else "Default Property"
            node_obj = cls(id, definition, first_property, name)

            # Set the picture using the set_picture() method
            pic_url = "/static/img/" + str(picture)
            node_obj.set_picture(pic_url)

            # Add all properties to the object using add_property()
            for prop in prop_list:
                node_obj.add_property(prop)

            node_list.append(node_obj)
        except AttributeError:
            print(f"Class {class_name} not found in module")
        except TypeError as e:
            print(f"Error instantiating {class_name}: {e}")
    return node_list


def edge_gen(edge_data, valid_node_ids):
    edge_list = []
    for i in range(0, edge_data.shape[0]):
        edge = edge_data.iloc[i]
        # Extract necessary fields
        from_edge = edge.get("From")
        to_edge = edge.get("To")
        label = edge.get("Label")
        description = edge.get("Desc", "")

        # Validate parent and child nodes exist in valid_node_ids
        if from_edge not in valid_node_ids or to_edge not in valid_node_ids:
            print(f"Skipping edge {i}: Invalid parent or child node (From: {from_edge}, To: {to_edge})")

        connection = micro.Connection(connection_type=label, parent=from_edge, child=to_edge)
        if pd.isna(description):
            connection.set_desc("")
        else:
            connection.set_desc(description)

        edge_list.append(connection)

    return edge_list


def network_gen(node_list, edge_list):
    visnetwork_nodes = []
    visnetwork_edges = []
    for node in node_list:
        # Create a visNetwork node
        # Get the full class hierarchy
        class_hierarchy = get_class_hierarchy(type(node))
        vis_node = {
            "id": node.identity,  # Unique ID for the node
            "label": node.get_name(),
            "definition": node.get_def(),
            "properties": node.properties,
            "picture": node.get_picture(),
            "hierarchy": class_hierarchy
        }
        visnetwork_nodes.append(vis_node)

    id = 1
    for edge in edge_list:
        # create a visNetwork edge
        vis_edge = {
            "id": id,
            "from": edge.get_parent(),
            "to": edge.get_child(),
            "label": edge.get_connection(),
            "description": edge.get_desc()
        }
        id += 1
        visnetwork_edges.append(vis_edge)
    return visnetwork_nodes, visnetwork_edges


# function to return a list with specific characteristics in a node
def node_char_list(node_list, class_name, prop=None, value=None):
    """
    Filter nodes by class and optionally filter by an attribute (prop) and its value.
    """
    filtered_nodes = []

    # Get the class reference from the micro module dynamically using getattr
    cls = getattr(micro, class_name, None)  # This will get the class from the micro module

    if cls is None:
        print(f"Class {class_name} not found in the micro module.")
        return filtered_nodes  # Return empty if the class does not exist

    # Loop through the nodes and check if the node is an instance of the class
    for node in node_list:
        if isinstance(node, cls):  # Check if node is an instance of the class
            if prop:
                # If a property is specified, check if it matches the value
                if hasattr(node, prop):
                    attribute_value = getattr(node, prop, None)
                    if attribute_value == value or value is None:
                        filtered_nodes.append(node.identity)
            else:
                # If no property filter is provided, add the node
                filtered_nodes.append(node.identity)

    return filtered_nodes


@app.route('/')
def index():
    data_node = get_nodes("micro_nodes.csv")
    data_edge = get_edges("micro_edges.csv")
    node_list = node_gen(data_node)

    # Extract valid node IDs from the node list
    valid_node_ids = [node.identity for node in node_list]

    edge_list = edge_gen(data_edge, valid_node_ids)
    nodes, edges = network_gen(node_list, edge_list)

    gram_positive_bacteria = node_char_list(node_list, "Bacteria", "gram_type", "positive")
    gram_negative_bacteria = node_char_list(node_list, "Bacteria", "gram_type", "negative")
    gram_variable_bacteria = node_char_list(node_list, "Bacteria", "gram_type", "indeterminate")
    antimicrobials = node_char_list(node_list, "Antimicrobial")
    fungi = node_char_list(node_list, "Fungus")
    parasites = node_char_list(node_list, "Parasite")
    dna_viruses = node_char_list(node_list, "Virus", "gene_material", "dna")
    rna_viruses = node_char_list(node_list, "Virus", "gene_material", "rna")

    node_lists = {
        'gram_positive': gram_positive_bacteria,
        'gram_negative': gram_negative_bacteria,
        'gram_ind': gram_variable_bacteria,
        'antimicrobials': antimicrobials,
        'fungi': fungi,
        'parasites': parasites,
        'dna_viruses': dna_viruses,
        'rna_viruses': rna_viruses
    }

    return render_template("index.html", nodes=nodes, edges=edges, node_lists=node_lists)


@app.route('/get_info', methods=['POST'])
def get_info():
    model = genai.GenerativeModel("gemini-1.5-flash")
    # Get the user message and location from the request
    object = request.json.get("object", "Red Blood Cell")  # Default location

    # Customize the user message with the location
    user_message = f"Tell me the function of {object}."

    try:
        response = model.generate_content(user_message)
        return jsonify({"content": response.text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/get_text", methods=["GET"])
def get_text():
    # Retrieve the selected node ID and previous node ID from the request arguments
    selected_node_id = request.args.get("selected_node_id", "unknown")
    previous_node_id = request.args.get("previous_node_id", "unknown")

    model = genai.GenerativeModel("gemini-1.5-flash")

    # Customize the user message with the location
    user_message = (f"How does {previous_node_id} relate to {selected_node_id} in the context of microbiology? "
                    f"keep your response short and concise.")

    try:
        response = model.generate_content(user_message)
        return jsonify({"text": response.text}), 200
    except Exception as e:
        return jsonify({"text": str(e)}), 400

    # # Generate a custom message using both node IDs
    # text = (
    #     f"This is the dynamic message for Node {selected_node_id}, "
    #     f"connected from Node {previous_node_id}."
    # )
    # return jsonify({"text": text})


@app.route('/generate_question', methods=['GET'])
def generate_question():
    model = genai.GenerativeModel("gemini-1.5-flash")
    # Load nodes and edges
    data_node = get_nodes("micro_nodes.csv")
    data_edge = get_edges("micro_edges.csv")
    node_list = node_gen(data_node)
    edge_list = edge_gen(data_edge, [node.identity for node in node_list])
    prompt = ""

    # Randomly pick a node or edge
    if random.choice(["node", "edge"]) == "node":
        node = random.choice(node_list)
        if (node.properties):
            property = random.choice(node.properties)
            prompt = f"{property} in {node.get_name()}"
        else:
            edge = random.choice(edge_list)
            prompt = f"how {edge.get_parent()} {edge.get_connection()} {edge.get_child()}"

    else:
        edge = random.choice(edge_list)
        prompt = f"how {edge.get_parent()} {edge.get_connection()} {edge.get_child()}"

    user_message = (
        f"Create a multiple-choice question about {prompt}."
        f" Respond with clean JSON only, no extra text or formatting. Use this exact structure:"
        f"""
            {{
                "question": "Your question here",
                "options": [
                    "Correct answer",
                    "Incorrect answer 1",
                    "Incorrect answer 2",
                    "Incorrect answer 3"
                ],
                "correct_option": "Correct answer"
            }}
            """
    )
    try:
        response = model.generate_content(user_message)
        response_text = response.text.strip()

        # Extract substring from '{' to '}'
        start_index = response_text.find('{')
        end_index = response_text.rfind('}') + 1  # Include the closing brace
        if start_index != -1 and end_index != -1:
            json_substring = response_text[start_index:end_index]
        else:
            json_substring = None  # Handle the case where braces are missing


        # Attempt to parse the response as JSON
        try:
            question_data = json.loads(json_substring)
            return jsonify(question_data), 200
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON response from model"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 400



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

