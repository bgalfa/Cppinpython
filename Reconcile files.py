import pandas as pd

def load_and_flatten(file_path):
    # Load Excel file (all sheets, as strings to avoid NaN float issues)
    df = pd.read_excel(file_path, sheet_name=None, dtype=str, header=None)
    
    # Flatten all sheets into one list of strings
    values = []
    for sheet_name, sheet_df in df.items():
        for val in sheet_df.values.flatten():
            if pd.notna(val):
                # Strip spaces and normalize case for fair comparison
                values.append(str(val).strip().lower())
    return sorted(values)  # Sort for easier comparison

def reconcile(file1, file2):
    data1 = load_and_flatten(file1)
    data2 = load_and_flatten(file2)

    # Convert to sets for reconciliation
    set1, set2 = set(data1), set(data2)

    only_in_file1 = set1 - set2
    only_in_file2 = set2 - set1
    common = set1 & set2

    return {
        "only_in_file1": only_in_file1,
        "only_in_file2": only_in_file2,
        "common": common
    }

# Example usage
file_path1 = "folder1/messy_file.xlsx"
file_path2 = "folder2/messy_file.xlsx"

result = reconcile(file_path1, file_path2)

print("Only in File 1:")
for item in result["only_in_file1"]:
    print("-", item)

print("\nOnly in File 2:")
for item in result["only_in_file2"]:
    print("-", item)

print(f"\nCommon Values ({len(result['common'])}):")
for item in list(result["common"])[:10]:  # print sample of common
    print("-", item)
