import csv
import os

def extract_second_column(input_csv, output_folder):
    with open(input_csv, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        # Skip header row if present
        next(csv_reader, None)

        i = 0
        for row in csv_reader:
            i += 1
            # Assuming there are at least two columns in each row
            if len(row) >= 2:
                second_column_value = row[1]

                # Generate a unique filename based on the second column value
                filename = os.path.join(output_folder, f"chat_{i}.txt")

                # Write the second column value to the text file
                with open(filename, 'w') as txt_file:
                    txt_file.write(second_column_value)

# Replace 'input.csv' with the path to your CSV file
input_csv_file = './topical_chat.csv'

# Replace 'output_folder' with the path to the folder where you want to save the text files
output_folder = './output_folder'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Call the function to extract the second column and save to text files
extract_second_column(input_csv_file, output_folder)