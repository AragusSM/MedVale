from bs4 import BeautifulSoup
import csv

# Load the HTML file
html_file = "1.html"  # Replace with your file path
output_csv = "clinical_vignettes.csv"

# Parse the HTML
with open(html_file, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Function to scrape the quiz data
def scrape_quiz_data(soup):
    quiz_data = []

    # Find all question blocks
    question_blocks = soup.find_all("div", class_="display_question")
    for question_block in question_blocks:
        # Extract the question text
        question_text_block = question_block.find("div", class_="question_text")
        question_text = question_text_block.get_text(strip=True) if question_text_block else "No question text found"

        # Extract all answer choices
        answers = []
        correct_answer = None
        answer_blocks = question_block.find_all("div", class_="answer")
        for answer_block in answer_blocks:
            answer_text_block = answer_block.find("div", class_="answer_text")
            answer_text = answer_text_block.get_text(strip=True) if answer_text_block else "No answer text found"
            answers.append(answer_text)

            # Check if this answer is marked as correct
            if "correct_answer" in answer_block.get("class", []):
                correct_answer = answer_text

        # Add the question and answers to the data list
        quiz_data.append({
            "question": question_text,
            "choices": ", ".join(answers),
            "correct_answer": correct_answer if correct_answer else "No correct answer found"
        })

    return quiz_data

# Function to append data to a CSV file
def append_to_csv(data, filename):
    # Check if file exists
    file_exists = False
    try:
        with open(filename, "r", encoding="utf-8") as file:
            file_exists = True
    except FileNotFoundError:
        pass

    # Write to the CSV file
    with open(filename, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["question", "choices", "correct_answer"])
        if not file_exists:
            writer.writeheader()  # Write header only if file is new
        writer.writerows(data)

# Scrape the quiz data
quiz_data = scrape_quiz_data(soup)

# Append the data to a CSV file
append_to_csv(quiz_data, output_csv)

print(f"Scraped {len(quiz_data)} questions and appended to {output_csv}.")
