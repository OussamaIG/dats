import pandas as pd

# Function to remove duplicate rows based on the 'text' column
def remove_duplicates(input_file, output_file):
    # Load the Excel file into a pandas DataFrame
    df = pd.read_excel(input_file)
    
    # Check for duplicates in the 'text' column and remove them
    df_cleaned = df.drop_duplicates(subset=['text'], keep='first')
    
    # Save the cleaned DataFrame to a new Excel file
    df_cleaned.to_excel(output_file, index=False)
    print(f"Duplicate rows removed. The cleaned file has been saved as {output_file}.")

# Example usage
input_file_path = 'generated_instagram_tiktok_posts_v2.xlsx'  # Replace with your file path
output_file_path = 'generated_instagram_tiktok_posts_v2.xlsx'  # Replace with desired output file path
remove_duplicates(input_file_path, output_file_path)
