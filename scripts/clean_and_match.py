"""
Prolific x Qualtrics Data Cleaning Pipeline
============================================
Matches Qualtrics survey responses to Prolific demographic records
by completion timestamp, then applies pre-registered exclusions.

Input:
  - data/Financial_Decision-Making_Study_February_27__2026_06_17.csv (Qualtrics, 3-header-row format)
  - data/prolific_demographic_export_699f424337ff6955d494e879.csv (Prolific demographics)

Output (all to output/):
  - cleaned_matched_data.csv        — analysis-ready dataset
  - exclusion_funnel.csv            — stage-by-stage exclusion summary
  - match_diagnostics.csv           — audit trail for timestamp matching
"""

import pandas as pd
import numpy as np
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────
DATA = Path("data")
OUT = Path("output")
OUT.mkdir(exist_ok=True)

QUALTRICS_FILE = DATA / "Financial_Decision-Making_Study_February_27__2026_06_17.csv"
PROLIFIC_FILE = DATA / "prolific_demographic_export_699f424337ff6955d494e879.csv"

# ── Load data ────────────────────────────────────────────────────────────────
# Qualtrics: row 0 = field names, rows 1-2 = question text + import IDs → skip
q = pd.read_csv(QUALTRICS_FILE, header=0, skiprows=[1, 2])
p = pd.read_csv(PROLIFIC_FILE)

print(f"Qualtrics loaded: {len(q)} rows")
print(f"Prolific loaded:  {len(p)} rows")
print(f"  Prolific status counts: {p['Status'].value_counts().to_dict()}")
print()

# Track funnel
funnel = []
funnel.append(("Qualtrics total", len(q), 0, "Raw export"))

# ── STEP 1: Remove previews and pilots ───────────────────────────────────────
print("=" * 70)
print("STEP 1: Remove previews and pilots")
print("=" * 70)

# 1a: Drop Survey Preview rows
n_preview = (q["Status"] == "Survey Preview").sum()
q = q[q["Status"] != "Survey Preview"].copy()
print(f"  Dropped {n_preview} Survey Preview rows → {len(q)} remaining")
funnel.append(("After removing previews", len(q), n_preview, "Status = Survey Preview"))

# 1b: Drop pilot responses completed before the earliest Prolific completion
# Parse timestamps
p["Completed at"] = pd.to_datetime(p["Completed at"], utc=True)

# Qualtrics EndDate is in America/Denver (UTC-7)
q["EndDate_parsed"] = pd.to_datetime(q["EndDate"])
q["EndDate_utc"] = q["EndDate_parsed"].dt.tz_localize("America/Denver").dt.tz_convert("UTC")

# Earliest Prolific APPROVED completion
p_approved = p[p["Status"] == "APPROVED"]
earliest_prolific = p_approved["Completed at"].min()
print(f"  Earliest Prolific APPROVED completion: {earliest_prolific}")

n_before = len(q)
q = q[q["EndDate_utc"] >= earliest_prolific].copy()
n_pilot = n_before - len(q)
print(f"  Dropped {n_pilot} pilot rows (completed before Prolific launch) → {len(q)} remaining")
funnel.append(("After removing pilots", len(q), n_pilot,
               f"Qualtrics EndDate < earliest Prolific completion ({earliest_prolific})"))

print(f"\n  STEP 1 RESULT: {len(q)} Qualtrics rows remaining\n")

# ── STEP 2: Match Qualtrics to Prolific on completion time ───────────────────
print("=" * 70)
print("STEP 2: Match Qualtrics ↔ Prolific on completion time")
print("=" * 70)

MATCH_THRESHOLD_SECONDS = 30

# Build candidate pairs with time gaps
pairs = []
for _, pr in p_approved.iterrows():
    for _, qr in q.iterrows():
        gap = abs((qr["EndDate_utc"] - pr["Completed at"]).total_seconds())
        pairs.append({
            "prolific_id": pr["Participant id"],
            "qualtrics_id": qr["ResponseId"],
            "gap_seconds": gap,
        })

pairs_df = pd.DataFrame(pairs).sort_values("gap_seconds")

# Greedy 1:1 matching — smallest gap first
matched_prolific = set()
matched_qualtrics = set()
matches = []

for _, row in pairs_df.iterrows():
    pid = row["prolific_id"]
    qid = row["qualtrics_id"]
    gap = row["gap_seconds"]

    if pid in matched_prolific or qid in matched_qualtrics:
        continue
    if gap > MATCH_THRESHOLD_SECONDS:
        continue

    matches.append({"prolific_id": pid, "qualtrics_id": qid, "gap_seconds": gap})
    matched_prolific.add(pid)
    matched_qualtrics.add(qid)

matches_df = pd.DataFrame(matches)
n_matched = len(matches_df)
n_unmatched_prolific = len(p_approved) - len(matched_prolific)
n_unmatched_qualtrics = len(q) - len(matched_qualtrics)

print(f"  Matched:              {n_matched}")
print(f"  Unmatched Prolific:   {n_unmatched_prolific}")
print(f"  Unmatched Qualtrics:  {n_unmatched_qualtrics}")

gaps = matches_df["gap_seconds"]
print(f"\n  Match gap distribution:")
print(f"    Min:    {gaps.min():.1f}s")
print(f"    Median: {gaps.median():.1f}s")
print(f"    Max:    {gaps.max():.1f}s")
print(f"    Within  5s: {(gaps <= 5).sum()}")
print(f"    Within 10s: {(gaps <= 10).sum()}")
print(f"    Within 30s: {(gaps <= 30).sum()}")

# Merge matched data
q_matched = q.set_index("ResponseId")
p_indexed = p_approved.set_index("Participant id")

prolific_keep_cols = [
    "Participant id", "Age", "Sex", "Ethnicity simplified",
    "Country of birth", "Country of residence", "Nationality",
    "Employment status",
]

merged = q.merge(
    matches_df, left_on="ResponseId", right_on="qualtrics_id", how="inner"
)
prolific_for_merge = p_approved[prolific_keep_cols].copy()
merged = merged.merge(
    prolific_for_merge, left_on="prolific_id", right_on="Participant id", how="left"
)

# Build match diagnostics
diag_rows = []
for _, m in matches_df.iterrows():
    qr = q[q["ResponseId"] == m["qualtrics_id"]].iloc[0]
    pr = p_approved[p_approved["Participant id"] == m["prolific_id"]].iloc[0]
    diag_rows.append({
        "Qualtrics_ResponseId": m["qualtrics_id"],
        "Prolific_ParticipantId": m["prolific_id"],
        "Qualtrics_EndDate_UTC": qr["EndDate_utc"],
        "Prolific_CompletedAt": pr["Completed at"],
        "Gap_seconds": m["gap_seconds"],
        "Qualtrics_Duration": qr["Duration (in seconds)"],
        "Prolific_TimeTaken": pr["Time taken"],
    })
diag = pd.DataFrame(diag_rows)

n_dropped_match = len(q) - n_matched
funnel.append(("After timestamp matching", n_matched, n_dropped_match,
               f"Unmatched Qualtrics rows (RETURNED/TIMED-OUT participants)"))

print(f"\n  STEP 2 RESULT: {n_matched} matched records\n")

# Work with merged from here
df = merged.copy()

# ── STEP 3: Pre-registered exclusion — completion time < 2 min ───────────────
print("=" * 70)
print("STEP 3: Exclude completion time < 120 seconds")
print("=" * 70)

df["Duration (in seconds)"] = pd.to_numeric(df["Duration (in seconds)"], errors="coerce")
n_before = len(df)
speed_mask = df["Duration (in seconds)"] < 120
n_speed = speed_mask.sum()
df = df[~speed_mask].copy()
print(f"  Excluded: {n_speed} (duration < 120s)")
print(f"  Remaining: {len(df)}")
funnel.append(("After speed exclusion", len(df), n_speed,
               "Pre-registered: Duration < 120 seconds"))

print(f"\n  STEP 3 RESULT: {len(df)} remaining\n")

# ── STEP 4: Pre-registered exclusion — dual attention/comprehension failure ──
print("=" * 70)
print("STEP 4: Dual attention + comprehension check")
print("=" * 70)

# Attention check: D6 should be "Somewhat disagree" (case-insensitive)
print(f"\n  D6 (attention check) unique values:")
print(f"    {df['D6'].value_counts().to_dict()}")

attn_fail = ~df["D6"].str.strip().str.lower().eq("somewhat disagree")
print(f"\n  Attention FAIL: {attn_fail.sum()}")
print(f"  Attention PASS: {(~attn_fail).sum()}")

# Comprehension check: C2 should indicate WealthPath performed WORSE
print(f"\n  C2 (comprehension check) unique values:")
print(f"    {df['C2'].value_counts().to_dict()}")

comp_fail = ~df["C2"].str.strip().str.lower().str.contains("worse")
print(f"\n  Comprehension FAIL: {comp_fail.sum()}")
print(f"  Comprehension PASS: {(~comp_fail).sum()}")

# Exclusion: fail BOTH
attn_only = attn_fail & ~comp_fail
comp_only = ~attn_fail & comp_fail
both_fail = attn_fail & comp_fail

print(f"\n  Failing attention ONLY:       {attn_only.sum()}")
print(f"  Failing comprehension ONLY:   {comp_only.sum()}")
print(f"  Failing BOTH (excluded):      {both_fail.sum()}")

n_before = len(df)
df = df[~both_fail].copy()
print(f"\n  Remaining: {len(df)}")
funnel.append(("After dual-check exclusion", len(df), both_fail.sum(),
               "Pre-registered: failed BOTH attention (D6) and comprehension (C2)"))

print(f"\n  STEP 4 RESULT: {len(df)} remaining\n")

# ── STEP 5: Save outputs ────────────────────────────────────────────────────
print("=" * 70)
print("STEP 5: Save outputs")
print("=" * 70)

# Drop working columns before saving
drop_cols = ["EndDate_parsed", "EndDate_utc", "qualtrics_id", "prolific_id", "gap_seconds"]
df_out = df.drop(columns=[c for c in drop_cols if c in df.columns])
df_out.to_csv(OUT / "cleaned_matched_data.csv", index=False)
print(f"  cleaned_matched_data.csv   — {len(df_out)} rows")

funnel_df = pd.DataFrame(funnel, columns=["Stage", "N_Remaining", "N_Excluded", "Reason"])
funnel_df.to_csv(OUT / "exclusion_funnel.csv", index=False)
print(f"  exclusion_funnel.csv       — {len(funnel_df)} stages")

diag.to_csv(OUT / "match_diagnostics.csv", index=False)
print(f"  match_diagnostics.csv      — {len(diag)} matched pairs")

print("\n" + "=" * 70)
print("FINAL SUMMARY")
print("=" * 70)
print(funnel_df.to_string(index=False))
print(f"\nFinal analysis-ready N = {len(df_out)}")
