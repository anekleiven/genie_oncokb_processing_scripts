"""
Step 3: 
Perform this after running the two scripts:
    01_add_oncotree.py
    02_deduplicate_variants.py 
Formats the input file (deduplicated variants) to ensure MAF compliance.
After this step, the resulting file can be used as input to the OncoKB Annotator for functional annotation.
"""

import pandas as pd
import numpy as np
import os
import argparse

# function to convert input file to MAF format: 

def MAF_formatter(input_file):
    """
    Prepare variants file for OncoKB annotator by fixing data types and formatting
    
    Args:
        input_file (str): Path to the unique variants file
    """
    print("-" * 70)
    print("Preparing variants for the OncoKB annotator...")
    print("-" * 70)
    print(f"\nReading variants file: {input_file}")

    df = pd.read_csv(input_file, sep='\t', low_memory=False)
    print(f"\nSuccessfully read file with {len(df):,} variants and {len(df.columns)} columns.\n")
    
    
    print(f"Checking for missing required MAF columns ...")

    required_cols = ["Hugo_Symbol", 
                     "Variant_Classification", 
                     "Variant_Type", 
                     "Tumor_Sample_Barcode", 
                     "Chromosome", 
                     "Start_Position", 
                     "End_Position", 
                     "Reference_Allele", 
                     "Tumor_Seq_Allele1", 
                     "Tumor_Seq_Allele2",]

    missing = [c for c in required_cols if c not in df.columns]

    if len(missing) == 0: 
        print("No missing columns. Proceeding...\n") 
    else: 
        print(f"⚠️ Missing required columns: {missing}\n")
    
    print("-" * 60)
    print("Converting integer columns to Int64...") 
    print("-" * 60)

    int_cols =  ['Entrez_Gene_Id', 
                 'Start_Position', 
                 'End_Position', 
                 't_ref_count', 
                 't_alt_count', 
                 'n_ref_count', 
                 'n_alt_count',
                 'n_depth', 
                 't_depth',
                 'Protein_position']
    
    for col in int_cols:
        if col in df.columns: 
            df[col] = pd.to_numeric(df[col], errors = 'coerce').astype('Int64') 
            print(f"'{col}' converted to Int64")
        else:
            print(f"Warning: Column '{col}' not found in dataframe")

    print("-" * 60)
    print("Converting float columns to Float64...") 
    print("-" * 60)
    
    float_cols = ["Score",
                  "gnomAD_AF",
                  "gnomAD_AFR_AF",
                  "gnomAD_AMR_AF",
                  "gnomAD_ASJ_AF",
                  "gnomAD_EAS_AF",
                  "gnomAD_FIN_AF",
                  "gnomAD_NFE_AF",
                  "gnomAD_OTH_AF",
                  "gnomAD_SAS_AF",
                  "Polyphen_Score",
                  "SIFT_Score"]
    
    for col in float_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors = 'coerce').astype("Float64")
            print(f"'{col}' converted to Float64")
        else:
            print(f"Warning: Column '{col}' not found in dataframe")

    print("-" * 60) 
    print("Convert all remaining columns to string...") 
    print("-" * 60) 

    numeric_cols = int_cols + float_cols 
    for col in df.columns: 
        if col not in numeric_cols: 
            df[col] = df[col].astype("string") 
            print(f"{col} successfully converted to string") 
    
    print("\nFinal column data types:") 
    print(df.dtypes) 

    base, ext = os.path.splitext(input_file) 
    output_file = base + "_maf_ready.txt" 
    df.to_csv(output_file, sep= "\t", index = False) 

    print("\n" + "-" * 70)
    print(f"MAF-ready file saved at:\n{output_file}")
    print("-" * 70)


# create function for user input file path:

def get_args(): 
    """
    Parse command line arguments 
    Example usage:
    python maf_formatter_oncokb.py --input path/to/file.txt

    """
    parser = argparse.ArgumentParser(description="Format variants to MAF format.")
    parser.add_argument(
        "--input",
        required=False,
        default="data/unique_variants_with_oncotree.txt",
        help="Path to the input file (e.g. unique_variants_with_oncotree.txt)"
    )
    return parser.parse_args()

def main(): 
    # call get_args() function 
    args = get_args()

    # path to input file
    input_file = args.input

    # call function to make MAF format 
    MAF_formatter(input_file)


if __name__ == "__main__": 
    main() 