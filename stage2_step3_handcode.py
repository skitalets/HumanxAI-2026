"""
Stage 2, Step 3: Hand-validation sample of 100 narratives.

Confidence-stratified sampling adapted to actual distribution:
  - Sonnet's confidence floor is 0.65 (no cases < 0.4)
  - Adapted bins: low (<0.75), medium (0.75-0.85), high (>0.85)
  - Target: 40% medium, 30% high, 30% low, balanced across 3 product types

Produces:
  - cfpb_handcode_100_blind.md (no classifications)
  - cfpb_handcode_100_blind.csv (spreadsheet format with empty coding columns)
  - cfpb_handcode_100_key.csv (answer key)
"""

import pandas as pd
import numpy as np
import os

CLASSIFIED_PATH = "/workspaces/HumanxAI-2026/output/cfpb_classified_9000.csv"
OUTPUT_DIR = "/workspaces/HumanxAI-2026/output"

BLIND_MD = os.path.join(OUTPUT_DIR, "cfpb_handcode_100_blind.md")
BLIND_CSV = os.path.join(OUTPUT_DIR, "cfpb_handcode_100_blind.csv")
KEY_CSV = os.path.join(OUTPUT_DIR, "cfpb_handcode_100_key.csv")

np.random.seed(42)

print("Loading classified narratives...")
df = pd.read_csv(CLASSIFIED_PATH, dtype={'complaint_id': 'int64'})
valid = df[df['classification'].isin(['EVALUATIVE', 'DELEGATIVE', 'UNCLASSIFIABLE'])].copy()
valid['confidence'] = pd.to_numeric(valid['confidence'], errors='coerce')

print(f"Valid classifications: {len(valid):,}")

# Adapted confidence bins based on actual distribution
# Original spec: low (<0.4), medium (0.4-0.7), high (>0.7)
# Actual: min=0.65, so we shift bins to capture real variation
# Low: bottom ~5% (<0.75), Medium: middle ~64% (0.75-0.85), High: top ~31% (>0.85)
def conf_bin(c):
    if c < 0.75:
        return 'low'
    elif c <= 0.85:
        return 'medium'
    else:
        return 'high'

valid['conf_bin'] = valid['confidence'].apply(conf_bin)

print("\nAdapted confidence bins:")
for b in ['low', 'medium', 'high']:
    n = len(valid[valid['conf_bin'] == b])
    print(f"  {b}: {n:,}")

# Target: 100 total, ~34 per product, split 40% medium / 30% high / 30% low
# Per product: ~13 medium, ~10 high, ~10 low (rounding to get ~33-34 per product)
PRODUCTS = ['mortgage', 'checking_savings', 'credit_card']
TARGET_PER_PRODUCT = {
    'mortgage': {'medium': 14, 'high': 10, 'low': 10},
    'checking_savings': {'medium': 13, 'high': 10, 'low': 10},
    'credit_card': {'medium': 13, 'high': 10, 'low': 10},
}
# Total: 34 + 33 + 33 = 100

samples = []
shortfalls = []

for prod in PRODUCTS:
    for conf in ['medium', 'high', 'low']:
        target_n = TARGET_PER_PRODUCT[prod][conf]
        pool = valid[(valid['product_group'] == prod) & (valid['conf_bin'] == conf)]

        if len(pool) >= target_n:
            s = pool.sample(n=target_n, random_state=42)
        else:
            # Take all available, note shortfall
            s = pool
            shortfall = target_n - len(pool)
            shortfalls.append((prod, conf, shortfall))
            print(f"  WARNING: {prod}/{conf} has only {len(pool)}, need {target_n} (shortfall: {shortfall})")

        samples.append(s)

sample = pd.concat(samples, ignore_index=True)
actual_n = len(sample)

# Fill shortfalls from adjacent bins in same product
if shortfalls:
    for prod, conf, shortfall in shortfalls:
        already_ids = set(sample['complaint_id'])
        # Try to fill from other bins
        remaining_pool = valid[
            (valid['product_group'] == prod) &
            (~valid['complaint_id'].isin(already_ids))
        ]
        if len(remaining_pool) >= shortfall:
            extra = remaining_pool.sample(n=shortfall, random_state=42)
            sample = pd.concat([sample, extra], ignore_index=True)
            print(f"  Filled {shortfall} shortfall for {prod}/{conf} from other bins")

# Shuffle the final sample
sample = sample.sample(frac=1, random_state=42).reset_index(drop=True)
sample['narrative_number'] = range(1, len(sample) + 1)

print(f"\nFinal sample: {len(sample)} narratives")
print(f"\nBy product:")
for prod in PRODUCTS:
    n = len(sample[sample['product_group'] == prod])
    print(f"  {prod}: {n}")

print(f"\nBy confidence bin:")
for b in ['low', 'medium', 'high']:
    n = len(sample[sample['conf_bin'] == b])
    print(f"  {b}: {n}")

print(f"\nBy classification:")
for cls in ['EVALUATIVE', 'DELEGATIVE', 'UNCLASSIFIABLE']:
    n = len(sample[sample['classification'] == cls])
    print(f"  {cls}: {n}")

# ============================================================
# Produce blind coding markdown
# ============================================================
print(f"\nWriting blind coding markdown...")
with open(BLIND_MD, 'w') as f:
    f.write("# CFPB Hand-Coding: 100 Narratives (Blind)\n\n")
    f.write("For each narrative, code:\n")
    f.write("- **Classification:** EVALUATIVE / DELEGATIVE / UNCLASSIFIABLE\n")
    f.write("- **Delegative score:** 0.0-1.0\n")
    f.write("- **Evaluative score:** 0.0-1.0\n")
    f.write("- **Confidence:** 0.0-1.0\n")
    f.write("- **Justification:** one sentence\n\n")
    f.write("---\n\n")

    for _, row in sample.iterrows():
        num = row['narrative_number']
        f.write(f"## Narrative {num}\n\n")
        f.write(f"- **Complaint ID:** {row['complaint_id']}\n")
        f.write(f"- **Product:** {row['product']}\n")
        f.write(f"- **Company:** {row['company']}\n")
        f.write(f"- **Date:** {row['date']}\n\n")
        narrative = str(row['narrative_text'])
        f.write(f"{narrative}\n\n")
        f.write("---\n\n")

print(f"  Saved: {BLIND_MD}")

# ============================================================
# Produce blind coding CSV (spreadsheet format)
# ============================================================
print(f"Writing blind coding CSV...")
blind_csv_df = sample[['narrative_number', 'complaint_id', 'product_group',
                        'company', 'date', 'narrative_text']].copy()
blind_csv_df = blind_csv_df.rename(columns={'product_group': 'product_type'})
blind_csv_df['classification'] = ''
blind_csv_df['delegative_score'] = ''
blind_csv_df['evaluative_score'] = ''
blind_csv_df['confidence'] = ''
blind_csv_df['justification'] = ''

blind_csv_df.to_csv(BLIND_CSV, index=False)
print(f"  Saved: {BLIND_CSV}")

# ============================================================
# Produce answer key CSV
# ============================================================
print(f"Writing answer key CSV...")
key_df = sample[['narrative_number', 'complaint_id', 'product_group',
                  'classification', 'confidence', 'delegative_score',
                  'evaluative_score', 'primary_evidence',
                  'secondary_signals', 'conf_bin']].copy()
key_df.to_csv(KEY_CSV, index=False)
print(f"  Saved: {KEY_CSV}")

print(f"\n{'=' * 70}")
print("STEP 3 COMPLETE")
print(f"{'=' * 70}")
print(f"  Blind MD:  {BLIND_MD}")
print(f"  Blind CSV: {BLIND_CSV}")
print(f"  Answer key: {KEY_CSV}")
