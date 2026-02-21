"""
CFPB Stage 1: Structural Exploration & Narrative Sampling
Chunked processing for memory efficiency on 7.7GB CSV.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
from collections import Counter

DATA_PATH = "/workspaces/HumanxAI-2026/data/complaints.csv"
OUTPUT_DIR = "/workspaces/HumanxAI-2026/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CHUNK_SIZE = 250_000

# Only load the columns we need
USE_COLS = [
    'Date received', 'Product', 'Sub-product',
    'Consumer complaint narrative', 'Company', 'Complaint ID'
]

print("=" * 70)
print("CFPB COMPLAINT DATABASE — STAGE 1 STRUCTURAL EXPLORATION")
print("=" * 70)
print(f"\nProcessing {DATA_PATH} in chunks of {CHUNK_SIZE:,}...")

# ============================================================
# PASS 1: Structural stats (no narrative text stored)
# ============================================================
print("\n--- PASS 1: Structural statistics ---")

total_complaints = 0
narrative_count = 0
product_counter = Counter()
company_counter = Counter()
company_mortgage = Counter()
company_checking = Counter()
company_cc = Counter()
year_counter = Counter()
length_data = []  # Store lengths only, not text
date_min = None
date_max = None

for chunk_num, chunk in enumerate(pd.read_csv(
    DATA_PATH,
    usecols=USE_COLS,
    dtype={
        'Product': 'str',
        'Sub-product': 'str',
        'Consumer complaint narrative': 'str',
        'Company': 'str',
        'Complaint ID': 'int64',
    },
    parse_dates=['Date received'],
    chunksize=CHUNK_SIZE,
    low_memory=False,
    on_bad_lines='skip'
)):
    total_complaints += len(chunk)

    # Filter to rows with narratives
    has_narr = chunk['Consumer complaint narrative'].notna()
    narr_chunk = chunk[has_narr]
    n_narr = len(narr_chunk)
    narrative_count += n_narr

    if n_narr == 0:
        if (chunk_num + 1) % 5 == 0:
            print(f"  Chunk {chunk_num + 1}: {total_complaints:,} total, {narrative_count:,} narratives")
        continue

    # Product counts
    for product, cnt in narr_chunk['Product'].value_counts().items():
        product_counter[product] += cnt

    # Company counts (overall)
    for company, cnt in narr_chunk['Company'].value_counts().items():
        company_counter[company] += cnt

    # Company counts by category
    mort_mask = narr_chunk['Product'].str.contains('Mortgage', case=False, na=False)
    check_mask = narr_chunk['Product'].str.contains('Checking or savings', case=False, na=False)
    cc_mask = narr_chunk['Product'].str.contains('Credit card', case=False, na=False)

    for company, cnt in narr_chunk[mort_mask]['Company'].value_counts().items():
        company_mortgage[company] += cnt
    for company, cnt in narr_chunk[check_mask]['Company'].value_counts().items():
        company_checking[company] += cnt
    for company, cnt in narr_chunk[cc_mask]['Company'].value_counts().items():
        company_cc[company] += cnt

    # Date range
    chunk_min = narr_chunk['Date received'].min()
    chunk_max = narr_chunk['Date received'].max()
    if date_min is None or chunk_min < date_min:
        date_min = chunk_min
    if date_max is None or chunk_max > date_max:
        date_max = chunk_max

    # Year counts
    for year, cnt in narr_chunk['Date received'].dt.year.value_counts().items():
        year_counter[year] += cnt

    # Narrative lengths
    lengths = narr_chunk['Consumer complaint narrative'].str.len().tolist()
    length_data.extend(lengths)

    if (chunk_num + 1) % 5 == 0:
        print(f"  Chunk {chunk_num + 1}: {total_complaints:,} total, {narrative_count:,} narratives")

print(f"\n  DONE: {total_complaints:,} total complaints, {narrative_count:,} with narratives")

# Compute length stats
length_arr = np.array(length_data, dtype=np.int64)
del length_data  # free memory

length_stats = {
    'count': len(length_arr),
    'mean': float(np.mean(length_arr)),
    'std': float(np.std(length_arr)),
    'min': float(np.min(length_arr)),
    'p25': float(np.percentile(length_arr, 25)),
    'median': float(np.median(length_arr)),
    'p75': float(np.percentile(length_arr, 75)),
    'p90': float(np.percentile(length_arr, 90)),
    'p95': float(np.percentile(length_arr, 95)),
    'p99': float(np.percentile(length_arr, 99)),
    'max': float(np.max(length_arr)),
}
del length_arr

# ============================================================
# Print structural results
# ============================================================
print("\n" + "=" * 70)
print("SECTION 1: TOTAL COMPLAINT COUNT")
print("=" * 70)
print(f"Total complaints: {total_complaints:,}")
print(f"With narratives:  {narrative_count:,} ({narrative_count/total_complaints*100:.1f}%)")

print("\n" + "=" * 70)
print("SECTION 2: NARRATIVE COUNT BY PRODUCT TYPE")
print("=" * 70)
product_sorted = product_counter.most_common()
print(f"\n{'Product':<55} {'Count':>10} {'Pct':>7}")
print("-" * 75)
for product, count in product_sorted:
    pct = count / narrative_count * 100
    print(f"{product:<55} {count:>10,} {pct:>6.1f}%")

print("\n" + "=" * 70)
print("SECTION 3: DATE RANGE")
print("=" * 70)
print(f"Earliest: {date_min}")
print(f"Latest:   {date_max}")
print(f"Span: {(date_max - date_min).days:,} days ({(date_max - date_min).days / 365.25:.1f} years)")
print("\nBy year:")
for year in sorted(year_counter.keys()):
    print(f"  {year}: {year_counter[year]:>10,}")

print("\n" + "=" * 70)
print("SECTION 4: NARRATIVE LENGTH DISTRIBUTION (CHARS)")
print("=" * 70)
for k, v in length_stats.items():
    print(f"  {k:<8}: {v:>12,.0f}")

print("\n" + "=" * 70)
print("SECTION 5: TOP 10 COMPANIES")
print("=" * 70)
print("\n--- OVERALL ---")
for i, (company, count) in enumerate(company_counter.most_common(10), 1):
    print(f"  {i:>2}. {company:<50} {count:>8,}")

print("\n--- MORTGAGES ---")
for i, (company, count) in enumerate(company_mortgage.most_common(10), 1):
    print(f"  {i:>2}. {company:<50} {count:>8,}")

print("\n--- CHECKING/SAVINGS ---")
for i, (company, count) in enumerate(company_checking.most_common(10), 1):
    print(f"  {i:>2}. {company:<50} {count:>8,}")

print("\n--- CREDIT CARDS ---")
for i, (company, count) in enumerate(company_cc.most_common(10), 1):
    print(f"  {i:>2}. {company:<50} {count:>8,}")


# ============================================================
# PASS 2: Stratified narrative sample + bonus searches
# (Single pass to avoid re-reading 7.7GB)
# ============================================================
print("\n" + "=" * 70)
print("PASS 2: Narrative sampling + fintech/trigger searches")
print("=" * 70)

# Reservoir sampling for the three strata
# We'll collect ALL narratives from the three product types into reservoirs
# using reservoir sampling to keep memory bounded.
MORTGAGE_N = 20
CHECKING_N = 15
CC_N = 15

np.random.seed(42)

reservoir_mortgage = []
reservoir_checking = []
reservoir_cc = []
mort_seen = 0
check_seen = 0
cc_seen = 0

# Fintech search
fintech_companies = ['Betterment', 'Wealthfront', 'Robinhood', 'SoFi', 'Chime',
                     'Cash App', 'Venmo', 'Acorns', 'Stash']
fintech_results = {fc: {'company_match': 0, 'narrative_match': 0, 'products': Counter()} for fc in fintech_companies}

# Trigger word search
trigger_terms = [
    'algorithm', 'automated', 'bot', 'computer decided',
    'the system flagged', 'auto-rejected', 'auto-denied',
    'automatically denied', 'automatically closed', 'automated system'
]
trigger_counts = {t: 0 for t in trigger_terms}
trigger_any_count = 0
trigger_examples = []  # reservoir of 10

for chunk_num, chunk in enumerate(pd.read_csv(
    DATA_PATH,
    usecols=USE_COLS,
    dtype={
        'Product': 'str',
        'Sub-product': 'str',
        'Consumer complaint narrative': 'str',
        'Company': 'str',
        'Complaint ID': 'int64',
    },
    parse_dates=['Date received'],
    chunksize=CHUNK_SIZE,
    low_memory=False,
    on_bad_lines='skip'
)):
    has_narr = chunk['Consumer complaint narrative'].notna()
    narr_chunk = chunk[has_narr].copy()
    if len(narr_chunk) == 0:
        continue

    narr_lower = narr_chunk['Consumer complaint narrative'].str.lower()
    company_lower = narr_chunk['Company'].str.lower()
    product_str = narr_chunk['Product'].fillna('')

    # --- Reservoir sampling for three strata ---
    mort_rows = narr_chunk[product_str.str.contains('Mortgage', case=False, na=False)]
    for _, row in mort_rows.iterrows():
        mort_seen += 1
        if len(reservoir_mortgage) < MORTGAGE_N:
            reservoir_mortgage.append(row.to_dict())
        else:
            j = np.random.randint(0, mort_seen)
            if j < MORTGAGE_N:
                reservoir_mortgage[j] = row.to_dict()

    check_rows = narr_chunk[product_str.str.contains('Checking or savings', case=False, na=False)]
    for _, row in check_rows.iterrows():
        check_seen += 1
        if len(reservoir_checking) < CHECKING_N:
            reservoir_checking.append(row.to_dict())
        else:
            j = np.random.randint(0, check_seen)
            if j < CHECKING_N:
                reservoir_checking[j] = row.to_dict()

    cc_rows = narr_chunk[product_str.str.contains('Credit card', case=False, na=False)]
    for _, row in cc_rows.iterrows():
        cc_seen += 1
        if len(reservoir_cc) < CC_N:
            reservoir_cc.append(row.to_dict())
        else:
            j = np.random.randint(0, cc_seen)
            if j < CC_N:
                reservoir_cc[j] = row.to_dict()

    # --- Fintech company search ---
    for fc in fintech_companies:
        fc_lower = fc.lower()
        c_match = company_lower.str.contains(fc_lower, na=False)
        n_match = narr_lower.str.contains(fc_lower, na=False)
        combined = c_match | n_match
        n_combined = int(combined.sum())

        fintech_results[fc]['company_match'] += int(c_match.sum())
        fintech_results[fc]['narrative_match'] += int(n_match.sum())

        if n_combined > 0:
            for prod, cnt in narr_chunk[combined]['Product'].value_counts().items():
                fintech_results[fc]['products'][prod] += cnt

    # --- Trigger word search ---
    any_match_this_chunk = pd.Series(False, index=narr_chunk.index)
    for term in trigger_terms:
        matches = narr_lower.str.contains(term.lower(), na=False)
        trigger_counts[term] += int(matches.sum())
        any_match_this_chunk = any_match_this_chunk | matches

    n_any = int(any_match_this_chunk.sum())
    trigger_any_count += n_any

    # Reservoir sample 10 trigger examples
    if n_any > 0:
        trigger_rows = narr_chunk[any_match_this_chunk]
        for _, row in trigger_rows.iterrows():
            total_trigger_seen = trigger_any_count  # approximate
            if len(trigger_examples) < 10:
                trigger_examples.append(row.to_dict())
            else:
                j = np.random.randint(0, total_trigger_seen)
                if j < 10:
                    trigger_examples[j] = row.to_dict()

    if (chunk_num + 1) % 5 == 0:
        print(f"  Chunk {chunk_num + 1}: sampled {len(reservoir_mortgage)}/{MORTGAGE_N} mort, "
              f"{len(reservoir_checking)}/{CHECKING_N} check, {len(reservoir_cc)}/{CC_N} cc")

print(f"\n  Reservoir sampling complete:")
print(f"    Mortgage: {len(reservoir_mortgage)} sampled from {mort_seen:,}")
print(f"    Checking: {len(reservoir_checking)} sampled from {check_seen:,}")
print(f"    Credit card: {len(reservoir_cc)} sampled from {cc_seen:,}")

# ============================================================
# Write 50 narratives to markdown
# ============================================================
sample_output_path = os.path.join(OUTPUT_DIR, "cfpb_50_narrative_sample.md")
all_samples = (
    [(r, 'Mortgage') for r in reservoir_mortgage] +
    [(r, 'Checking/Savings') for r in reservoir_checking] +
    [(r, 'Credit Card') for r in reservoir_cc]
)

with open(sample_output_path, 'w') as f:
    f.write("# CFPB Complaint Narratives — Stratified Sample (N=50)\n\n")
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"Random seed: 42 (reservoir sampling)\n")
    f.write(f"Stratification: 20 mortgage, 15 checking/savings, 15 credit card\n\n")
    f.write("**Purpose:** Hand-read these narratives to assess whether consumer language\n")
    f.write("naturally splits into evaluative trust failure (performance disappointment,\n")
    f.write("functional problems, unmet expectations) versus delegative trust betrayal\n")
    f.write("(moral violation, betrayal of relationship, abuse of granted authority).\n\n")
    f.write("---\n\n")

    for idx, (row, stratum) in enumerate(all_samples, 1):
        f.write(f"## Narrative {idx} [{stratum}]\n\n")
        f.write(f"- **Product:** {row.get('Product', 'N/A')}\n")
        f.write(f"- **Sub-product:** {row.get('Sub-product', 'N/A')}\n")
        f.write(f"- **Company:** {row.get('Company', 'N/A')}\n")
        f.write(f"- **Date:** {row.get('Date received', 'N/A')}\n")
        f.write(f"- **Complaint ID:** {row.get('Complaint ID', 'N/A')}\n\n")
        narrative = str(row.get('Consumer complaint narrative', ''))
        f.write(f"{narrative}\n\n")
        f.write("---\n\n")

print(f"\n50 narratives saved to: {sample_output_path}")

# ============================================================
# Print and save fintech results
# ============================================================
print("\n" + "=" * 70)
print("FINTECH COMPANY SEARCH RESULTS")
print("=" * 70)
print(f"\n{'Company':<20} {'Total':>8} {'Filed Against':>14} {'In Narrative':>14}")
print("-" * 60)
for fc in fintech_companies:
    r = fintech_results[fc]
    total = r['company_match'] + r['narrative_match'] - min(r['company_match'], r['narrative_match'])
    # Approximate total (company_match | narrative_match counted per chunk)
    total_approx = r['company_match']  # mostly filed-against drives this
    print(f"{fc:<20} {r['company_match'] + r['narrative_match']:>8,} {r['company_match']:>14,} {r['narrative_match']:>14,}")

print("\nProduct breakdown:")
for fc in fintech_companies:
    r = fintech_results[fc]
    if r['products']:
        print(f"\n  {fc}:")
        for prod, cnt in r['products'].most_common():
            print(f"    {prod:<50} {cnt:>6,}")

# ============================================================
# Print and save trigger word results
# ============================================================
print("\n" + "=" * 70)
print("ALGORITHMIC TRIGGER WORD SEARCH")
print("=" * 70)
for term in trigger_terms:
    print(f"  '{term}': {trigger_counts[term]:>8,}")
print(f"\n  ANY trigger term: {trigger_any_count:>8,}")

# Write trigger examples
trigger_output_path = os.path.join(OUTPUT_DIR, "cfpb_algorithmic_trigger_examples.md")
with open(trigger_output_path, 'w') as f:
    f.write("# CFPB Narratives Containing Algorithmic Trigger Terms\n\n")
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    f.write("**Search terms:** algorithm, automated, bot, computer decided, ")
    f.write("the system flagged, auto-rejected, auto-denied, automatically denied, ")
    f.write("automatically closed, automated system\n\n")
    f.write(f"**Total narratives matching any term:** {trigger_any_count:,}\n\n")
    f.write("**Term-by-term counts:**\n\n")
    for term in sorted(trigger_counts, key=trigger_counts.get, reverse=True):
        f.write(f"- `{term}`: {trigger_counts[term]:,}\n")
    f.write("\n---\n\n")
    f.write("## 10 Example Narratives\n\n")

    for idx, row in enumerate(trigger_examples, 1):
        f.write(f"### Example {idx}\n\n")
        f.write(f"- **Product:** {row.get('Product', 'N/A')}\n")
        f.write(f"- **Sub-product:** {row.get('Sub-product', 'N/A')}\n")
        f.write(f"- **Company:** {row.get('Company', 'N/A')}\n")
        f.write(f"- **Date:** {row.get('Date received', 'N/A')}\n")
        f.write(f"- **Complaint ID:** {row.get('Complaint ID', 'N/A')}\n\n")
        narrative = str(row.get('Consumer complaint narrative', ''))
        f.write(f"{narrative}\n\n")
        f.write("---\n\n")

print(f"\nTrigger examples saved to: {trigger_output_path}")

# ============================================================
# Write fintech results to separate file
# ============================================================
fintech_output_path = os.path.join(OUTPUT_DIR, "cfpb_fintech_search_results.md")
with open(fintech_output_path, 'w') as f:
    f.write("# CFPB Fintech Company Search Results\n\n")
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    f.write("Search method: matched company name field OR mention in narrative text (case-insensitive).\n")
    f.write("Only complaints with consumer narratives included.\n\n")

    f.write("## Summary\n\n")
    f.write("| Company | Filed Against | Mentioned in Text |\n")
    f.write("|---------|-------------:|------------------:|\n")
    for fc in fintech_companies:
        r = fintech_results[fc]
        f.write(f"| {fc} | {r['company_match']:,} | {r['narrative_match']:,} |\n")

    f.write("\n## Product Breakdown\n\n")
    for fc in fintech_companies:
        r = fintech_results[fc]
        if r['products']:
            f.write(f"### {fc}\n\n")
            f.write("| Product | Count |\n|---------|------:|\n")
            for prod, cnt in r['products'].most_common():
                f.write(f"| {prod} | {cnt:,} |\n")
            f.write("\n")

print(f"Fintech results saved to: {fintech_output_path}")

# ============================================================
# Write structural summary
# ============================================================
summary_path = os.path.join(OUTPUT_DIR, "cfpb_structural_summary.md")
with open(summary_path, 'w') as f:
    f.write("# CFPB Complaint Database — Stage 1 Structural Summary\n\n")
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"Source: consumerfinance.gov full complaint database CSV\n\n")

    f.write("## 1. Total Complaint Count\n\n")
    f.write(f"- **Total complaints:** {total_complaints:,}\n")
    f.write(f"- **Complaints with narratives:** {narrative_count:,} ({narrative_count/total_complaints*100:.1f}%)\n")
    f.write(f"- **Complaints without narratives:** {total_complaints - narrative_count:,}\n\n")

    f.write("## 2. Narrative Count by Product Type\n\n")
    f.write(f"| Product | Count | Pct |\n|---------|------:|----:|\n")
    for product, count in product_sorted:
        pct = count / narrative_count * 100
        f.write(f"| {product} | {count:,} | {pct:.1f}% |\n")

    f.write("\n## 3. Date Range\n\n")
    f.write(f"- **Earliest narrative complaint:** {date_min}\n")
    f.write(f"- **Latest narrative complaint:** {date_max}\n")
    f.write(f"- **Span:** {(date_max - date_min).days:,} days ({(date_max - date_min).days / 365.25:.1f} years)\n\n")

    f.write("### Narratives by Year\n\n")
    f.write("| Year | Count |\n|------|------:|\n")
    for year in sorted(year_counter.keys()):
        f.write(f"| {int(year)} | {year_counter[year]:,} |\n")

    f.write("\n## 4. Narrative Length Distribution (Characters)\n\n")
    f.write("| Statistic | Value |\n|-----------|------:|\n")
    for label, key in [('Count', 'count'), ('Mean', 'mean'), ('Std Dev', 'std'),
                        ('Min', 'min'), ('25th pctl', 'p25'), ('Median', 'median'),
                        ('75th pctl', 'p75'), ('90th pctl', 'p90'),
                        ('95th pctl', 'p95'), ('99th pctl', 'p99'), ('Max', 'max')]:
        f.write(f"| {label} | {length_stats[key]:,.0f} |\n")

    f.write("\n## 5. Top 10 Companies by Narrative Count\n\n")

    f.write("### Overall\n\n")
    f.write("| Rank | Company | Narratives |\n|------|---------|----------:|\n")
    for i, (company, count) in enumerate(company_counter.most_common(10), 1):
        f.write(f"| {i} | {company} | {count:,} |\n")

    f.write("\n### Mortgages\n\n")
    f.write("| Rank | Company | Narratives |\n|------|---------|----------:|\n")
    for i, (company, count) in enumerate(company_mortgage.most_common(10), 1):
        f.write(f"| {i} | {company} | {count:,} |\n")

    f.write("\n### Checking/Savings\n\n")
    f.write("| Rank | Company | Narratives |\n|------|---------|----------:|\n")
    for i, (company, count) in enumerate(company_checking.most_common(10), 1):
        f.write(f"| {i} | {company} | {count:,} |\n")

    f.write("\n### Credit Cards\n\n")
    f.write("| Rank | Company | Narratives |\n|------|---------|----------:|\n")
    for i, (company, count) in enumerate(company_cc.most_common(10), 1):
        f.write(f"| {i} | {company} | {count:,} |\n")

    f.write("\n## 6. Fintech Company Search\n\n")
    f.write("See `cfpb_fintech_search_results.md` for full details.\n\n")
    f.write("| Company | Filed Against | Mentioned in Text |\n")
    f.write("|---------|-------------:|------------------:|\n")
    for fc in fintech_companies:
        r = fintech_results[fc]
        f.write(f"| {fc} | {r['company_match']:,} | {r['narrative_match']:,} |\n")

    f.write("\n## 7. Algorithmic Trigger Word Search\n\n")
    f.write("See `cfpb_algorithmic_trigger_examples.md` for 10 example narratives.\n\n")
    f.write("| Term | Narratives |\n|------|----------:|\n")
    for term in sorted(trigger_counts, key=trigger_counts.get, reverse=True):
        f.write(f"| `{term}` | {trigger_counts[term]:,} |\n")
    f.write(f"\n**Any trigger term:** {trigger_any_count:,} narratives\n")

print(f"\nStructural summary saved to: {summary_path}")

print("\n" + "=" * 70)
print("STAGE 1 COMPLETE — ALL OUTPUT FILES:")
print("=" * 70)
print(f"  1. {summary_path}")
print(f"  2. {sample_output_path}")
print(f"  3. {trigger_output_path}")
print(f"  4. {fintech_output_path}")
