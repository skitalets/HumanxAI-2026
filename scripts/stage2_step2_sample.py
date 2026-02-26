"""
Stage 2, Step 2a: Draw stratified sample of 9,000 narratives.
3,000 per product category. Random seed = 42.
"""

import pandas as pd
import numpy as np

INPUT_PATH = "/workspaces/HumanxAI-2026/data/cfpb_filtered_corpus.csv"
OUTPUT_PATH = "/workspaces/HumanxAI-2026/data/classification_sample_9000.csv"

print("Loading filtered corpus...")
df = pd.read_csv(INPUT_PATH, dtype={'complaint_id': 'int64'}, parse_dates=['date'])
print(f"Loaded {len(df):,} rows")

N_PER_GROUP = 3000

np.random.seed(42)

samples = []
for group in ['mortgage', 'checking_savings', 'credit_card']:
    pool = df[df['product_group'] == group]
    s = pool.sample(n=N_PER_GROUP, random_state=42)
    samples.append(s)
    print(f"  {group}: sampled {len(s):,} from {len(pool):,}")

sample_df = pd.concat(samples, ignore_index=True)
print(f"\nTotal sample: {len(sample_df):,}")

# Summary
lengths = sample_df['narrative_text'].str.len()
print(f"Narrative length: median={lengths.median():.0f}, mean={lengths.mean():.0f}")

sample_df.to_csv(OUTPUT_PATH, index=False)
print(f"Saved to: {OUTPUT_PATH}")
