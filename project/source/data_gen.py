import csv


# Define the function to collect and write entries to a CSV file
def write_to_csv(filename):
    # Open the CSV file in append mode so new entries don't overwrite existing ones
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Define headers, but only write if the file is empty
        if file.tell() == 0:
            headers = ["Id", "Name", "Definition", "Class", "PropList", "Picture"]
            writer.writerow(headers)

    # Start data entry process
    while True:
        data = {"Id": "", "Name": "", "Definition": "", "Class": "", "PropList": "", "Picture": ""}
        fields = list(data.keys())
        current_index = 0

        while current_index < len(fields):
            field = fields[current_index]
            value = input(f"Enter data for {field} (type 'redo' to re-enter previous field or 'exit' to quit): ")

            # Handle the 'exit' command
            if value.lower() == 'exit':
                return

            # Handle the 'redo' command
            if value.lower() == 'redo':
                # Go back to the previous field if not at the first field
                if current_index > 0:
                    current_index -= 1
                continue  # Skip to prompt again for the previous field

            # If valid input, store it and move to the next field
            data[field] = value
            current_index += 1

        # Write the row to the CSV
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([data["Id"], data["Name"], data["Definition"],
                             data["Class"], data["PropList"], data["Picture"]])

        print("Entry added to CSV!\n")


if __name__ == "__main__":
    filename = '../micro_nodes.csv'  # Name your file as needed
    write_to_csv(filename)
    print(f"Entries saved to {filename}")
