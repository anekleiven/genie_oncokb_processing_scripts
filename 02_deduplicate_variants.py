"""
Step 2 of 3: 
Perform this step after adding oncotree codes (01_add_oncotree.py)
Deduplicates variants from GENIE data
Removes recurring variants (same variant in multiple tumors) to speed up further annotation.
"""

import pandas as pd
import argparse
import os

# function to remove recurrent variants 

def deduplicate_variants(input_file, output_file):
    """
    Create a unique variant set from GENIE mutation data.

    Keeps all original columns and removes recurrent variants.
    Keeps the first occurrence of each unique variant identity. 

    Args:
        input_file (str): Path to the input mutations file (with duplicates)
        output_file (str): Path to save the deduplicated variants
    """
    print("-" * 60)
    print("Deduplicating variants for OncoKB annotator")
    print("-" * 60)
    
    print(f"\nReading variant file: ") 
    print(f"{input_file}")
    print(f"\nThis may take some time for large files...\n")
    
    # Read the variant file
    df = pd.read_csv(input_file, sep='\t', low_memory=False)
    
    print(f"Total variants in input file: {len(df):,}")
    
    # Define columns that identify a unique variant
    # Columns that define the variant itself (not sample-specific)

    variant_cols = [
        'Hugo_Symbol',                      # Gene
        'Chromosome',                       # Chromosome number 
        'Start_Position',                   # Start position of the variant
        'End_Position',                     # End position of the variant 
        'Reference_Allele',                 # How the variant looks at the reference allele 
        'Tumor_Seq_Allele1',                # One allele observed in the tumor 
        'Tumor_Seq_Allele2',                # The other allele observed in the tumor 
        'Variant_Classification',           # Category (missense, nonsense, silent) 
        'Variant_Type',                     # SNP, INS, DEL etc. 
        'HGVSp_Short',                      # Protein change
        'HGVSc'                             # cDNA change
    ]
    
    print(f"\nIdentifying unique variants based on: {', '.join(variant_cols)}")
    

    # Select the first occurence for each unique variant identity.
    # Keeps all original columns and removes recurrent variants.
    print("\nSelecting representative rows (first occurrence) for each unique variant...")

    unique_df = df.drop_duplicates(subset=variant_cols, keep='first').copy()

    print(f"\nUnique variants: {len(unique_df):,}")
    

    # Save to output file
    print(f"\nSaving deduplicated variants to: {output_file}")
    unique_df.to_csv(output_file, sep='\t', index=False)
    
    # Calculate reduction of DF
    reduction = (1 - len(unique_df) / len(df)) * 100
    print(f"\nFile size reduction: {reduction:.1f}%")
    print(f"  Before: {len(df):,} rows")
    print(f"  After:  {len(unique_df):,} rows")
    
    print("\n✓ Deduplication complete!")
    return unique_df

def get_args():
    """
    Parse command line arguments 
    Example usage:
    python deduplicate_variants.py --input path/to/file.txt

    """
    parser = argparse.ArgumentParser(description="deduplicate cancer variants")
    parser.add_argument(
        "--input",
        required=False,
        default="data/variants_with_oncotree.txt",
        help="Path to the input file (e.g. variants_with_oncotree.txt)" 
    )
    return parser.parse_args()


def main():

    # call get_args() function 
    args = get_args()

    # path to input file
    input_file = args.input
    
    # Output: deduplicated file for OncoKB
    output_file = os.path.join(os.path.dirname(input_file), "unique_variants_with_oncotree.txt")
    
    # Run deduplication (keeps all columns)
    deduplicate_variants(input_file, output_file)
    
    print(f"\nDone! The deduplicated file is now ready and saved as:") 
    print(f"{output_file}.\n")


if __name__ == "__main__":
    main()

