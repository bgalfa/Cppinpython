import pandas as pd
import numpy as np

def load_as_dataframe(file_path):
    # Read all sheets into one DataFrame
    all_sheets = pd.read_excel(file_path, sheet_name=None, header=None, dtype=str)
    
    # Combine sheets vertically, keeping NaN for empty cells
    df_list = []
    for sheet_name, df in all_sheets.items():
        df_list.append(df)
    combined_df = pd.concat(df_list, ignore_index=True)
    
    return combined_df

def reconcile_cells(file1, file2):
    df1 = load_as_dataframe(file1)
    df2 = load_as_dataframe(file2)
    
    # Ensure both have same shape by filling with NaN
    max_rows = max(df1.shape[0], df2.shape[0])
    max_cols = max(df1.shape[1], df2.shape[1])
    df1 = df1.reindex(index=range(max_rows), columns=range(max_cols))
    df2 = df2.reindex(index=range(max_rows), columns=range(max_cols))
    
    differences = []
    
    for r in range(max_rows):
        for c in range(max_cols):
            val1 = str(df1.iat[r, c]).strip() if pd.notna(df1.iat[r, c]) else ""
            val2 = str(df2.iat[r, c]).strip() if pd.notna(df2.iat[r, c]) else ""
            
            if val1 != val2:
                differences.append({
                    "row": r+1,      # +1 for human-friendly index
                    "column": c+1,   # +1 for human-friendly index
                    "file1_value": val1,
                    "file2_value": val2
                })
    
    return differences

# Example usage
file_path1 = "folder1/messy_file.xlsx"
file_path2 = "folder2/messy_file.xlsx"

diffs = reconcile_cells(file_path1, file_path2)

if diffs:
    print(f"Found {len(diffs)} differences:")
    for d in diffs:
        print(f"Row {d['row']}, Column {d['column']}: "
              f"File1='{d['file1_value']}' | File2='{d['file2_value']}'")
else:
    print("No differences found.")
    
