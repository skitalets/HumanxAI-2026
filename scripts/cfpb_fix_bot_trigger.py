"""
Fix the 'bot' trigger word search - use word boundary matching to avoid
matching 'both', 'about', 'bottom', etc.
Also re-run trigger examples with corrected counts.
"""

import pandas as pd
import numpy as np
import os
import re
from datetime import datetime
from collections import Counter

DATA_PATH = "/workspaces/HumanxAI-2026/data/complaints.csv"
OUTPUT_DIR = "/workspaces/HumanxAI-2026/output"
CHUNK_SIZE = 250_000

USE_COLS = [
    'Date received', 'Product', 'Sub-product',
    'Consumer complaint narrative', 'Company', 'Complaint ID'
]

# Updated trigger terms - use regex word boundaries for 'bot'
trigger_terms_exact = [
    'algorithm',
    'automated',
    'computer decided',
    'the system flagged',
    'auto-rejected',
    'auto-denied',
    'automatically denied',
    'automatically closed',
    'automated system'
]

# 'bot' needs word boundary matching
bot_pattern = re.compile(r'\bbot\b|\bchatbot\b|\brobot\b|\brobo\b', re.IGNORECASE)

trigger_counts = {t: 0 for t in trigger_terms_exact}
trigger_counts['bot (word boundary: bot/chatbot/robot/robo)'] = 0
trigger_any_count = 0
trigger_examples = []

print("Re-running trigger word search with corrected 'bot' matching...")

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

    any_match = pd.Series(False, index=narr_chunk.index)

    for term in trigger_terms_exact:
        matches = narr_lower.str.contains(term.lower(), na=False)
        trigger_counts[term] += int(matches.sum())
        any_match = any_match | matches

    # Word-boundary bot match
    bot_matches = narr_chunk['Consumer complaint narrative'].str.contains(bot_pattern, na=False)
    trigger_counts['bot (word boundary: bot/chatbot/robot/robo)'] += int(bot_matches.sum())
    any_match = any_match | bot_matches

    n_any = int(any_match.sum())
    trigger_any_count += n_any

    # Reservoir sample 10 examples
    if n_any > 0:
        trigger_rows = narr_chunk[any_match]
        for _, row in trigger_rows.iterrows():
            if len(trigger_examples) < 10:
                trigger_examples.append(row.to_dict())
            else:
                j = np.random.randint(0, trigger_any_count)
                if j < 10:
                    trigger_examples[j] = row.to_dict()

    if (chunk_num + 1) % 10 == 0:
        print(f"  Chunk {chunk_num + 1}...")

print("\nCORRECTED TRIGGER WORD COUNTS:")
print("-" * 60)
for term in sorted(trigger_counts, key=trigger_counts.get, reverse=True):
    print(f"  '{term}': {trigger_counts[term]:>8,}")
print(f"\n  ANY trigger term: {trigger_any_count:>8,}")

# Rewrite output files with corrected counts
trigger_output_path = os.path.join(OUTPUT_DIR, "cfpb_algorithmic_trigger_examples.md")
with open(trigger_output_path, 'w') as f:
    f.write("# CFPB Narratives Containing Algorithmic Trigger Terms\n\n")
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    f.write("**Search terms:** algorithm, automated, bot (word boundary), computer decided, ")
    f.write("the system flagged, auto-rejected, auto-denied, automatically denied, ")
    f.write("automatically closed, automated system\n\n")
    f.write(f"**Note:** 'bot' is matched with word boundaries (`\\bbot\\b|\\bchatbot\\b|\\brobot\\b|\\brobo\\b`) ")
    f.write("to avoid false matches on 'both', 'about', 'bottom', etc.\n\n")
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

print(f"\nCorrected trigger file saved to: {trigger_output_path}")

# Also update the structural summary's trigger section
summary_path = os.path.join(OUTPUT_DIR, "cfpb_structural_summary.md")
with open(summary_path, 'r') as f:
    content = f.read()

# Find and replace the trigger section
trigger_section_start = content.find("## 7. Algorithmic Trigger Word Search")
if trigger_section_start >= 0:
    new_trigger = "## 7. Algorithmic Trigger Word Search\n\n"
    new_trigger += "See `cfpb_algorithmic_trigger_examples.md` for 10 example narratives.\n\n"
    new_trigger += "**Note:** 'bot' matched with word boundaries to avoid 'both'/'about'/'bottom' false positives.\n\n"
    new_trigger += "| Term | Narratives |\n|------|----------:|\n"
    for term in sorted(trigger_counts, key=trigger_counts.get, reverse=True):
        new_trigger += f"| `{term}` | {trigger_counts[term]:,} |\n"
    new_trigger += f"\n**Any trigger term:** {trigger_any_count:,} narratives\n"

    content = content[:trigger_section_start] + new_trigger
    with open(summary_path, 'w') as f:
        f.write(content)
    print(f"Updated trigger section in: {summary_path}")
