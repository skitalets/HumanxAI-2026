"""
Stage 2, Step 1: Filter CFPB corpus to classifiable narratives.

Filters:
  - Product: Mortgage, Checking/savings, Credit card
  - Has narrative (non-null)
  - 200+ characters
  - Date >= 2015-06-01
  - Not a template (near-verbatim duplicates appearing 5+ times,
    or common credit repair / identity theft openings)

Outputs:
  - data/cfpb_filtered_corpus.csv
  - Printed: counts, excluded template examples, length distribution,
    10-narrative sanity sample
"""

import pandas as pd
import numpy as np
import os
import re
import hashlib
from collections import Counter
from datetime import datetime

DATA_PATH = "/workspaces/HumanxAI-2026/data/complaints.csv"
OUTPUT_PATH = "/workspaces/HumanxAI-2026/data/cfpb_filtered_corpus.csv"
OUTPUT_DIR = "/workspaces/HumanxAI-2026/output"
CHUNK_SIZE = 250_000

USE_COLS = [
    'Complaint ID', 'Date received', 'Product', 'Sub-product',
    'Company', 'State', 'Consumer complaint narrative'
]

# Template opening patterns (case-insensitive)
TEMPLATE_OPENINGS = [
    r'^i am writing to dispute',
    r'^this letter is to inform you',
    r'^under the fair credit reporting act',
    r'^i am a victim of identity theft',
    r'^to whom it may concern.*i am writing',
    r'^i am exercising my right',
    r'^please be advised',
    r'^pursuant to',
    r'^in accordance with the fair credit',
    r'^i recently obtained a copy of my credit report',
    r'^i have reviewed my credit report',
    r'^i am requesting that you',
    r'^this is not a duplicate',
    r'^i writing to request',
    r'^as a consumer i have the right',
    r'^as per the fair credit reporting act',
    r'^i sent a letter to',
    r'^i, .{2,40}, am a natural person',
    r'^according to the fair credit reporting act',
    r'^15 u\.?s\.?c',
    r'^i am sending this letter',
    r'^i have not given .{0,30} permission',
    r'^i am not liable for this debt',
]

TEMPLATE_PATTERNS = [re.compile(p, re.IGNORECASE) for p in TEMPLATE_OPENINGS]


def classify_product(product_str):
    if pd.isna(product_str):
        return None
    p = product_str.lower()
    if 'mortgage' in p:
        return 'mortgage'
    if 'checking or savings' in p or 'bank account or service' in p:
        return 'checking_savings'
    if 'credit card' in p:
        return 'credit_card'
    return None


def is_template_opening(text):
    """Check if narrative starts with a known template pattern."""
    first_200 = text[:200].strip()
    for pat in TEMPLATE_PATTERNS:
        if pat.search(first_200):
            return True
    return False


def narrative_hash(text):
    """Hash first 300 chars (normalized) for near-duplicate detection."""
    normalized = re.sub(r'\s+', ' ', text[:300].lower().strip())
    # Also strip XXXX redactions which vary
    normalized = re.sub(r'x{2,}', 'XXXX', normalized)
    return hashlib.md5(normalized.encode()).hexdigest()


print("=" * 70)
print("STAGE 2, STEP 1: FILTER TO CLASSIFIABLE NARRATIVES")
print("=" * 70)

# ============================================================
# PASS 1: Collect narrative hashes to find near-duplicates
# ============================================================
print("\n--- PASS 1: Finding near-duplicate narratives ---")

hash_counter = Counter()
total_candidates = 0  # narratives that pass product/date/length filters

for chunk_num, chunk in enumerate(pd.read_csv(
    DATA_PATH,
    usecols=USE_COLS,
    dtype={
        'Product': 'str', 'Sub-product': 'str',
        'Consumer complaint narrative': 'str',
        'Company': 'str', 'Complaint ID': 'int64', 'State': 'str',
    },
    parse_dates=['Date received'],
    chunksize=CHUNK_SIZE,
    low_memory=False,
    on_bad_lines='skip'
)):
    # Basic filters
    mask = (
        chunk['Consumer complaint narrative'].notna()
        & (chunk['Date received'] >= '2015-06-01')
    )
    sub = chunk[mask].copy()

    # Product filter
    sub['product_group'] = sub['Product'].apply(classify_product)
    sub = sub[sub['product_group'].notna()]

    # Length filter
    sub = sub[sub['Consumer complaint narrative'].str.len() >= 200]

    total_candidates += len(sub)

    # Hash narratives for duplicate detection
    for text in sub['Consumer complaint narrative']:
        h = narrative_hash(text)
        hash_counter[h] += 1

    if (chunk_num + 1) % 10 == 0:
        print(f"  Chunk {chunk_num + 1}: {total_candidates:,} candidates so far")

# Identify duplicate hashes (5+ occurrences)
dup_hashes = {h for h, count in hash_counter.items() if count >= 5}
print(f"\n  Total candidate narratives: {total_candidates:,}")
print(f"  Unique narrative hashes: {len(hash_counter):,}")
print(f"  Hashes appearing 5+ times: {len(dup_hashes):,}")
dup_count_total = sum(c for h, c in hash_counter.items() if c >= 5)
print(f"  Narratives covered by 5+ hashes: {dup_count_total:,}")

del hash_counter  # free memory

# ============================================================
# PASS 2: Apply all filters, collect results and examples
# ============================================================
print("\n--- PASS 2: Applying all filters, collecting results ---")

filtered_chunks = []
total_read = 0
kept = 0
excluded_template_opening = 0
excluded_near_duplicate = 0

# Collect examples of excluded narratives
template_examples = []  # (reason, first_100_chars)
duplicate_examples = []
MAX_EXAMPLES = 15

np.random.seed(42)

for chunk_num, chunk in enumerate(pd.read_csv(
    DATA_PATH,
    usecols=USE_COLS,
    dtype={
        'Product': 'str', 'Sub-product': 'str',
        'Consumer complaint narrative': 'str',
        'Company': 'str', 'Complaint ID': 'int64', 'State': 'str',
    },
    parse_dates=['Date received'],
    chunksize=CHUNK_SIZE,
    low_memory=False,
    on_bad_lines='skip'
)):
    total_read += len(chunk)

    # Basic filters
    mask = (
        chunk['Consumer complaint narrative'].notna()
        & (chunk['Date received'] >= '2015-06-01')
    )
    sub = chunk[mask].copy()

    # Product filter
    sub['product_group'] = sub['Product'].apply(classify_product)
    sub = sub[sub['product_group'].notna()]

    # Length filter
    sub = sub[sub['Consumer complaint narrative'].str.len() >= 200]

    if len(sub) == 0:
        continue

    # Template opening filter
    template_mask = sub['Consumer complaint narrative'].apply(is_template_opening)
    template_excluded = sub[template_mask]
    excluded_template_opening += len(template_excluded)

    # Collect template examples
    if len(template_examples) < MAX_EXAMPLES:
        for _, row in template_excluded.head(MAX_EXAMPLES - len(template_examples)).iterrows():
            text = str(row['Consumer complaint narrative'])
            template_examples.append({
                'product': row['Product'],
                'opening': text[:150].replace('\n', ' '),
            })

    sub = sub[~template_mask]

    # Near-duplicate filter
    dup_mask = sub['Consumer complaint narrative'].apply(
        lambda t: narrative_hash(t) in dup_hashes
    )
    dup_excluded = sub[dup_mask]
    excluded_near_duplicate += len(dup_excluded)

    # Collect duplicate examples
    if len(duplicate_examples) < MAX_EXAMPLES:
        for _, row in dup_excluded.head(MAX_EXAMPLES - len(duplicate_examples)).iterrows():
            text = str(row['Consumer complaint narrative'])
            duplicate_examples.append({
                'product': row['Product'],
                'opening': text[:150].replace('\n', ' '),
            })

    sub = sub[~dup_mask]

    if len(sub) > 0:
        # Rename columns for output
        sub = sub.rename(columns={
            'Consumer complaint narrative': 'narrative_text',
            'Complaint ID': 'complaint_id',
            'Date received': 'date',
            'Product': 'product',
            'Sub-product': 'sub_product',
            'Company': 'company',
            'State': 'state',
        })
        sub = sub[['complaint_id', 'product', 'sub_product', 'product_group',
                    'company', 'date', 'state', 'narrative_text']]
        filtered_chunks.append(sub)
        kept += len(sub)

    if (chunk_num + 1) % 10 == 0:
        print(f"  Chunk {chunk_num + 1}: kept {kept:,}, "
              f"excl template={excluded_template_opening:,}, "
              f"excl dup={excluded_near_duplicate:,}")

print(f"\n  Total rows read: {total_read:,}")
print(f"  Excluded by template opening: {excluded_template_opening:,}")
print(f"  Excluded as near-duplicate (5+): {excluded_near_duplicate:,}")
print(f"  Final kept: {kept:,}")

# Concatenate
print("\nConcatenating...")
df = pd.concat(filtered_chunks, ignore_index=True)
del filtered_chunks

# ============================================================
# REPORT
# ============================================================
print("\n" + "=" * 70)
print("RESULTS")
print("=" * 70)

print(f"\n## Total filtered narratives: {len(df):,}")
print(f"\nBy product_group:")
for group in ['mortgage', 'checking_savings', 'credit_card']:
    n = len(df[df['product_group'] == group])
    print(f"  {group:<20} {n:>8,}")

print(f"\nDate range: {df['date'].min()} to {df['date'].max()}")

lengths = df['narrative_text'].str.len()
print(f"\nNarrative length distribution (chars):")
print(f"  Min:    {lengths.min():>8,}")
print(f"  25th:   {lengths.quantile(0.25):>8,.0f}")
print(f"  Median: {lengths.median():>8,.0f}")
print(f"  75th:   {lengths.quantile(0.75):>8,.0f}")
print(f"  Max:    {lengths.max():>8,}")
print(f"  Mean:   {lengths.mean():>8,.0f}")

print(f"\nLength by product_group:")
for group in ['mortgage', 'checking_savings', 'credit_card']:
    gl = df[df['product_group'] == group]['narrative_text'].str.len()
    print(f"  {group}: median={gl.median():.0f}, mean={gl.mean():.0f}, n={len(gl):,}")

# ============================================================
# EXCLUDED TEMPLATE EXAMPLES
# ============================================================
print("\n" + "=" * 70)
print("EXCLUDED: TEMPLATE OPENING EXAMPLES")
print("=" * 70)
for i, ex in enumerate(template_examples, 1):
    print(f"\n  {i}. [{ex['product']}]")
    print(f"     \"{ex['opening']}...\"")

print("\n" + "=" * 70)
print("EXCLUDED: NEAR-DUPLICATE EXAMPLES (appeared 5+ times)")
print("=" * 70)
for i, ex in enumerate(duplicate_examples, 1):
    print(f"\n  {i}. [{ex['product']}]")
    print(f"     \"{ex['opening']}...\"")

# ============================================================
# 10-NARRATIVE SANITY SAMPLE
# ============================================================
print("\n" + "=" * 70)
print("SANITY CHECK: 10 RANDOM NARRATIVES FROM FILTERED CORPUS")
print("=" * 70)

sample_10 = df.sample(n=10, random_state=42)
for idx, (_, row) in enumerate(sample_10.iterrows(), 1):
    text = str(row['narrative_text'])
    preview = text[:300].replace('\n', ' ')
    print(f"\n--- Sample {idx} [{row['product_group']}] ---")
    print(f"Company: {row['company']}")
    print(f"Date: {row['date']}")
    print(f"Length: {len(text):,} chars")
    print(f"\"{preview}...\"")

# ============================================================
# SAVE
# ============================================================
print("\n" + "=" * 70)
print("SAVING FILTERED CORPUS")
print("=" * 70)

df.to_csv(OUTPUT_PATH, index=False)
file_size = os.path.getsize(OUTPUT_PATH) / 1e6
print(f"Saved to: {OUTPUT_PATH}")
print(f"File size: {file_size:.1f} MB")
print(f"Rows: {len(df):,}")

print("\n" + "=" * 70)
print("STEP 1 COMPLETE — AWAITING YOUR INPUT")
print("=" * 70)
print(f"\nFiltered corpus: {len(df):,} narratives")
print("How many should I classify? (And should I adjust the filters?)")
