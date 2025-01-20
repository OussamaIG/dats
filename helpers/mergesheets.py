import pandas as pd

def merge_xlsx_files(file1, file2, output_file):
    # Read the two Excel files
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    # Concatenate the dataframes
    merged_df = pd.concat([df1, df2], ignore_index=True)

    # Write the merged dataframe to a new Excel file
    merged_df.to_excel(output_file, index=False)

# Example usage
file1 = 'comedy.xlsx'
file2 = 'educational.xlsx'
output_file = 'merged_file.xlsx'
merge_xlsx_files(file1, file2, output_file)