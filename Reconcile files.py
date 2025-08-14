import pandas as pd
import os

def load_as_dataframe(file_path):
    # Read all sheets without headers
    all_sheets = pd.read_excel(file_path, sheet_name=None, header=None, dtype=str)
    df_list = []
    for sheet_name, df in all_sheets.items():
        df_list.append(df)
    combined_df = pd.concat(df_list, ignore_index=True)
    return combined_df

def reconcile_cells(file1, file2):
    df1 = load_as_dataframe(file1)
    df2 = load_as_dataframe(file2)
    
    # Match shapes
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
                    "Row": r + 1,         # Human-readable row
                    "Column": c + 1,      # Human-readable column
                    "File1 Value": val1,
                    "File2 Value": val2
                })
    return pd.DataFrame(differences)

def reconcile_folders(folder1, folder2, output_file):
    files1 = set(os.listdir(folder1))
    files2 = set(os.listdir(folder2))
    common_files = files1 & files2  # Files with same names in both folders
    
    with pd.ExcelWriter(output_file) as writer:
        for filename in sorted(common_files):
            file1_path = os.path.join(folder1, filename)
            file2_path = os.path.join(folder2, filename)
            
            try:
                diff_df = reconcile_cells(file1_path, file2_path)
                if diff_df.empty:
                    diff_df = pd.DataFrame({"Info": ["No differences found"]})
                
                # Use sheet name without extension (max length Excel supports is 31 chars)
                sheet_name = os.path.splitext(filename)[0][:31]
                diff_df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"Processed: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Example usage
folder1 = "folder1"
folder2 = "folder2"
output_excel = "reconciliation_results.xlsx"

reconcile_folders(folder1, folder2, output_excel)

print(f"\nReconciliation complete. Results saved in '{output_excel}'")
