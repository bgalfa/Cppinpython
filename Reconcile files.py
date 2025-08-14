import pandas as pd
import os

def load_as_dataframe(file_path):
    try:
        # Read all sheets without headers
        all_sheets = pd.read_excel(file_path, sheet_name=None, header=None, dtype=str)
        df_list = [df for _, df in all_sheets.items()]
        combined_df = pd.concat(df_list, ignore_index=True)
        return combined_df
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def reconcile_cells_table(file1, file2):
    df1 = load_as_dataframe(file1)
    df2 = load_as_dataframe(file2)
    
    # If either file failed to load, skip comparison
    if df1 is None or df2 is None:
        return f"Error: Missing or unreadable file(s)"
    
    try:
        # Match shapes by expanding to max rows/cols
        max_rows = max(df1.shape[0], df2.shape[0])
        max_cols = max(df1.shape[1], df2.shape[1])
        df1 = df1.reindex(index=range(max_rows), columns=range(max_cols))
        df2 = df2.reindex(index=range(max_rows), columns=range(max_cols))
    except Exception as e:
        return f"Error adjusting shapes: {e}"
    
    rows = ["Row\tCol\tFile1 Value\tFile2 Value"]  # Table header
    
    try:
        for r in range(max_rows):
            for c in range(max_cols):
                val1 = str(df1.iat[r, c]).strip() if pd.notna(df1.iat[r, c]) else ""
                val2 = str(df2.iat[r, c]).strip() if pd.notna(df2.iat[r, c]) else ""
                
                if val1 != val2:
                    rows.append(f"{r+1}\t{c+1}\t{val1}\t{val2}")
    except Exception as e:
        return f"Error comparing cells: {e}"
    
    if len(rows) == 1:
        return "No differences found"
    
    return "\n".join(rows)  # Keep as single cell content

def reconcile_folders_table(folder1, folder2, output_file):
    try:
        files1 = set(os.listdir(folder1))
    except FileNotFoundError:
        print(f"Error: Folder not found - {folder1}")
        return
    
    try:
        files2 = set(os.listdir(folder2))
    except FileNotFoundError:
        print(f"Error: Folder not found - {folder2}")
        return
    
    common_files = files1 & files2
    if not common_files:
        print("No matching files found between folders.")
        return
    
    summary_data = []
    
    for filename in sorted(common_files):
        file1_path = os.path.join(folder1, filename)
        file2_path = os.path.join(folder2, filename)
        
        print(f"Processing: {filename}")
        diff_table = reconcile_cells_table(file1_path, file2_path)
        summary_data.append({"File Name": filename, "Differences Table": diff_table})
    
    try:
        final_df = pd.DataFrame(summary_data)
        final_df.to_excel(output_file, index=False)
        print(f"\nReconciliation complete. Table summary saved in '{output_file}'")
    except Exception as e:
        print(f"Error writing to Excel: {e}")

# Example usage
folder1 = "folder1"
folder2 = "folder2"
output_excel = "reconciliation_table_in_cell.xlsx"

reconcile_folders_table(folder1, folder2, output_excel)
