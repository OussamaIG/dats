import json
import pandas as pd

def json_to_excel(json_file, excel_file):
    # Load the JSON file
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"File {json_file} not found.")
        return
    except json.JSONDecodeError:
        print(f"File {json_file} is not a valid JSON file.")
        return

    # Ensure the data is a list of strings
    if not isinstance(data, list) or not all(isinstance(item, str) for item in data):
        print("JSON file must contain an array of strings.")
        return

    # Create a DataFrame with two columns
    df = pd.DataFrame({
        "Text": data,
        "Category": ["Educational" for _ in data]
    })

    # Save to Excel
    try:
        df.to_excel(excel_file, index=False, sheet_name="Data")
        print(f"Excel file created successfully: {excel_file}")
    except Exception as e:
        print(f"Error saving Excel file: {e}")

# Example usage
json_file = "hashtagposts.json"
excel_file = "educational.xlsx"
json_to_excel(json_file, excel_file)