"""
Step 1: 
Adds Oncotree codes to variant data my mapping from clinical sample data from GENIE 
Maps using sample ID (Tumor_Sample_Barcode).
""" 

import pandas as pd 
import os 
import argparse

# Function to load clinical mapping 
def load_clinical_mapping(clinical_sample_file): 

    """Load the clinical sample data and create a mapping from sample ID to Oncotree code."""
    print("\nLOADING CLINICAL SAMPLE DATA...\n") 

    clinical_df = pd.read_csv(clinical_sample_file, sep='\t', skiprows=4)
    oncotree_mapping = dict(zip(clinical_df['SAMPLE_ID'], clinical_df['ONCOTREE_CODE']))

    print(f"Loaded {len(oncotree_mapping)} sample-to-oncotree mappings")
    print("Examples of mapping:") 
    for sample_id, code in list(oncotree_mapping.items())[:5]: 
        print(f"  {sample_id} -> {code}")  
    return oncotree_mapping


# Function to process variant file 
def process_variant_file(input_file, output_file, oncotree_mapping, chunk_size=5000): 

    """Process the variant file in chunks, adding Oncotree codes."""

    print(f"\nProcessing variant file in chunks of {chunk_size} rows...")
    first_chunk = True 
    matched_samples = 0 
    unmatched_samples = 0 
    total_variants = 0 

    try: 
        chunk_iter = pd.read_csv(input_file, sep='\t', chunksize=chunk_size, low_memory=False)
        for chunk_num, chunk in enumerate(chunk_iter): 
            total_variants += len(chunk)
            chunk['ONCOTREE_CODE'] = chunk['Tumor_Sample_Barcode'].apply(lambda x: oncotree_mapping.get(x, None))
            matched_samples += chunk['ONCOTREE_CODE'].notnull().sum() 
            unmatched_samples += chunk['ONCOTREE_CODE'].isnull().sum() 

            mode = 'w' if first_chunk else 'a'
            header = first_chunk
            chunk.to_csv(output_file, sep='\t', mode=mode, header=header, index=False)
            first_chunk = False

            if (chunk_num + 1) % 10 == 0:
                match_rate = matched_samples / total_variants * 100 if total_variants > 0 else 0
                print(f"Processed {chunk_num + 1} chunks ({total_variants:,} variants) — {match_rate:.1f}% mapped")
    except Exception as e: 
        print(f"Error processing file: {e}") 
        raise 

    print("\nProcessing complete!")
    print(f"Total variants processed: {total_variants:,}")
    print(f"Matched samples: {matched_samples:,}")
    print(f"Unmatched samples: {unmatched_samples:,}")
    if total_variants > 0:
        print(f"Overall match rate: {matched_samples / total_variants * 100:.1f}%")


# Verify one sample 
def verify_sample(output_file, sample_id): 

    """Verify the Oncotree mapping by checking a specific sample ID."""

    print(f"\nVerifying results for sample: {sample_id}")
    found = False
    for chunk in pd.read_csv(output_file, sep='\t', chunksize=10000, low_memory=False):
        sample_rows = chunk[chunk['Tumor_Sample_Barcode'] == sample_id]
        if len(sample_rows) > 0:
            found = True
            print(f"Found {len(sample_rows)} rows for sample {sample_id}:")
            print(sample_rows[['Tumor_Sample_Barcode', 'ONCOTREE_CODE']])
            break
    if not found:
        print(f"Sample {sample_id} not found in the output file.")


# --- Argparse setup ---
def get_args(): 
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Add Oncotree codes to variants by mapping sample IDs."
        )

    parser.add_argument(
        "--clinical", 
        required=False, 
        default="data/GENIE/data_clinical_sample.txt",
        help="Path to the clinical sample file (e.g. data/GENIE/data_clinical_sample.txt)"
        )

    parser.add_argument(
        "--variants", 
        required=False,
        default="data/GENIE/data_mutations_extended.txt",
        help="Path to the variant file (e.g. data/GENIE/data_mutations_extended.txt)"
        )

    parser.add_argument(
        "--output", 
        required=False, 
        default="data/variants_with_oncotree.txt",
        help="Path for the output file (default: data/variants_with_oncotree.txt)"
        )

    return parser.parse_args()


# Main method

def main(): 
    args = get_args()

    clinical_file = args.clinical
    variant_file = args.variants

    if args.output:
        output_file = args.output
    else:
        output_file = os.path.join(os.path.dirname(variant_file), "variants_with_oncotree.txt")

    print("=" * 60)
    print("Adding OncoTree codes to variant data!")
    print("=" * 60)

    oncotree_mapping = load_clinical_mapping(clinical_file)
    process_variant_file(variant_file, output_file, oncotree_mapping)

    sample_id = input("\nEnter a sample ID to verify (e.g. 'GENIE-XXXX-XXXXXX-XXX-X'):  ").strip()
    verify_sample(output_file, sample_id)

    print(f"\nOutput file created: {output_file}")
    print("Done!")


if __name__ == "__main__":
    main()
