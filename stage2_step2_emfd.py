"""
Stage 2, Step 2c: eMFD moral foundations scoring.

Dictionary-based scoring using the Extended Moral Foundations Dictionary
(Hopp et al. 2021). Downloaded from medianeuroscience/emfdscore GitHub.

For each narrative, counts word hits per moral foundation, weighted by
the foundation probability (_p columns). Normalized by total word count
to produce per-word moral foundation density scores.
"""

import pandas as pd
import numpy as np
import re
import os

CLASSIFIED_PATH = "/workspaces/HumanxAI-2026/output/cfpb_classified_9000.csv"
EMFD_DICT_PATH = "/workspaces/HumanxAI-2026/data/emfd/emfd_scoring.csv"
OUTPUT_PATH = "/workspaces/HumanxAI-2026/output/cfpb_emfd_scores.csv"

FOUNDATIONS = ['care', 'fairness', 'loyalty', 'authority', 'sanctity']

print("Loading eMFD dictionary...")
emfd = pd.read_csv(EMFD_DICT_PATH)
print(f"  {len(emfd)} words in dictionary")

# Build lookup dict: word -> {care_p, fairness_p, ...}
emfd_lookup = {}
for _, row in emfd.iterrows():
    word = str(row['word']).lower().strip()
    emfd_lookup[word] = {
        f: row[f'{f}_p'] for f in FOUNDATIONS
    }
    # Also include sentiment scores
    for f in FOUNDATIONS:
        emfd_lookup[word][f'{f}_sent'] = row[f'{f}_sent']

print(f"  Built lookup for {len(emfd_lookup)} unique words")

def tokenize(text):
    """Simple whitespace + punctuation tokenizer."""
    return re.findall(r'[a-z]+', text.lower())

def score_narrative(text):
    """Score a narrative against the eMFD dictionary.

    Returns dict with:
    - {foundation}_p: sum of probability weights for matched words, normalized by word count
    - {foundation}_sent: mean sentiment for matched words (or 0 if no matches)
    - emfd_hits: number of dictionary words found
    - word_count: total words in narrative
    """
    tokens = tokenize(text)
    word_count = len(tokens)

    if word_count == 0:
        result = {f'{f}_p': 0.0 for f in FOUNDATIONS}
        result.update({f'{f}_sent': 0.0 for f in FOUNDATIONS})
        result['emfd_hits'] = 0
        result['word_count'] = 0
        return result

    # Accumulate scores
    p_sums = {f: 0.0 for f in FOUNDATIONS}
    sent_sums = {f: 0.0 for f in FOUNDATIONS}
    sent_counts = {f: 0 for f in FOUNDATIONS}
    hits = 0

    for token in tokens:
        if token in emfd_lookup:
            hits += 1
            entry = emfd_lookup[token]
            for f in FOUNDATIONS:
                p_val = entry[f]
                p_sums[f] += p_val
                if p_val > 0:  # only count sentiment when foundation is relevant
                    sent_sums[f] += entry[f'{f}_sent']
                    sent_counts[f] += 1

    result = {}
    for f in FOUNDATIONS:
        # Probability score: normalized by word count (density)
        result[f'{f}_p'] = p_sums[f] / word_count
        # Sentiment: mean of matched words (or 0)
        result[f'{f}_sent'] = sent_sums[f] / sent_counts[f] if sent_counts[f] > 0 else 0.0

    result['emfd_hits'] = hits
    result['word_count'] = word_count

    return result


print(f"\nLoading classified narratives...")
df = pd.read_csv(CLASSIFIED_PATH, dtype={'complaint_id': 'int64'})
print(f"  {len(df):,} narratives loaded")

print(f"\nScoring narratives with eMFD...")
scores = []
for i, (_, row) in enumerate(df.iterrows()):
    text = str(row.get('narrative_text', ''))
    score = score_narrative(text)
    score['complaint_id'] = row['complaint_id']
    scores.append(score)

    if (i + 1) % 1000 == 0:
        print(f"  {i + 1:,}/{len(df):,} scored")

scores_df = pd.DataFrame(scores)
print(f"\nScoring complete.")

# Summary
print(f"\neMFD summary statistics:")
print(f"  Mean hits per narrative: {scores_df['emfd_hits'].mean():.1f}")
print(f"  Mean word count: {scores_df['word_count'].mean():.0f}")
print(f"\n  Foundation probability densities (mean across all narratives):")
for f in FOUNDATIONS:
    mean_p = scores_df[f'{f}_p'].mean()
    print(f"    {f:<12}: {mean_p:.6f}")

# Save
scores_df.to_csv(OUTPUT_PATH, index=False)
print(f"\nSaved to: {OUTPUT_PATH}")
