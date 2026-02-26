"""
Stage 2, Step 2b: Classify 9,000 narratives via Claude API.

Uses the exact classification prompt from cfpb_stage2_prompt_revised_20260222.md.
- 0.0-1.0 float scores (not Likert)
- Three-way categorical: EVALUATIVE / DELEGATIVE / UNCLASSIFIABLE
- Confidence as separate float
- NO product type or company passed to classifier (prevents hypothesis leakage)
- temperature=0.0, max_tokens=300

Uses async concurrency for speed (20 parallel requests).
Resumes from checkpoint if available.
"""

import pandas as pd
import json
import os
import sys
import time
import asyncio
import traceback
from datetime import datetime

INPUT_PATH = "/workspaces/HumanxAI-2026/data/classification_sample_9000.csv"
OUTPUT_PATH = "/workspaces/HumanxAI-2026/output/cfpb_classified_9000.csv"
CHECKPOINT_PATH = "/workspaces/HumanxAI-2026/output/cfpb_classified_9000_checkpoint.csv"
FAILED_LOG = "/workspaces/HumanxAI-2026/output/cfpb_classify_failures.log"

MODEL = "claude-sonnet-4-5-20250929"
MAX_CONCURRENT = 20
CHECKPOINT_INTERVAL = 200

SYSTEM_PROMPT = """You are a research assistant classifying consumer financial complaints for an academic study on trust in financial relationships.

The study distinguishes two modes of trust failure:

EVALUATIVE TRUST FAILURE: The consumer's complaint is primarily about unmet performance expectations, functional problems, or verification failures. The consumer treats the financial institution as a service provider that failed to deliver. Language focuses on: incorrect charges, broken processes, unmet promises, poor service quality, failure to perform as advertised. The emotional register is frustration, dissatisfaction, or anger at incompetence. The consumer's implicit stance is: "You didn't do what you were supposed to do."

DELEGATIVE TRUST FAILURE: The consumer's complaint reflects betrayal of a relationship in which they had granted the institution discretionary authority or relied on it as a fiduciary. Language focuses on: betrayal, abandonment, broken loyalty, abuse of the relationship, violation of good faith, taking advantage of vulnerability. The emotional register is moral outrage, a sense of personal violation, or grief at a relationship destroyed. The consumer's implicit stance is: "I trusted you and you betrayed me."

UNCLASSIFIABLE: The complaint does not clearly reflect either trust mode. This includes: template/form letters, pure factual disputes with no emotional content, identity theft reports where the consumer has no relationship with the institution, complaints too brief or unclear to assess, or complaints that mix both modes without a dominant one.

Important: Many complaints will be unclassifiable. That is expected. Do not force a classification. Only assign EVALUATIVE or DELEGATIVE when the language clearly reflects one mode."""


def make_user_prompt(narrative_text):
    return f"""Classify this consumer financial complaint. Respond in exactly this JSON format:

{{
  "classification": "EVALUATIVE" | "DELEGATIVE" | "UNCLASSIFIABLE",
  "confidence": <float 0.0 to 1.0>,
  "primary_evidence": "<one sentence quoting or paraphrasing the specific language that drove your classification>",
  "secondary_signals": "<one sentence noting any additional signals, or 'none'>",
  "delegative_score": <float 0.0 to 1.0>,
  "evaluative_score": <float 0.0 to 1.0>
}}

The delegative_score and evaluative_score are independent dimensions, not a zero-sum scale. A complaint can score high on both (mixed), low on both (unclassifiable), or high on one and low on the other (clean classification).

COMPLAINT:
\"\"\"
{narrative_text}
\"\"\""""


def parse_response(raw_text):
    """Extract and parse JSON from API response."""
    text = raw_text.strip()
    # Handle markdown code blocks
    if text.startswith("```"):
        lines = text.split("\n")
        json_lines = []
        in_block = False
        for line in lines:
            if line.startswith("```") and not in_block:
                in_block = True
                continue
            elif line.startswith("```") and in_block:
                break
            elif in_block:
                json_lines.append(line)
        text = "\n".join(json_lines)

    parsed = json.loads(text)

    required = ['classification', 'confidence', 'primary_evidence',
                'secondary_signals', 'delegative_score', 'evaluative_score']
    for field in required:
        if field not in parsed:
            raise ValueError(f"Missing field: {field}")

    if parsed['classification'] not in ['EVALUATIVE', 'DELEGATIVE', 'UNCLASSIFIABLE']:
        raise ValueError(f"Invalid classification: {parsed['classification']}")

    return parsed


async def classify_one(client, narrative_text, semaphore, max_retries=5):
    """Classify a single narrative with rate limiting."""
    user_prompt = make_user_prompt(narrative_text)

    async with semaphore:
        for attempt in range(max_retries):
            try:
                response = await client.messages.create(
                    model=MODEL,
                    max_tokens=300,
                    temperature=0.0,
                    system=SYSTEM_PROMPT,
                    messages=[{"role": "user", "content": user_prompt}]
                )
                raw_text = response.content[0].text
                return parse_response(raw_text)

            except json.JSONDecodeError as e:
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                else:
                    return {'error': f'JSON parse failed: {e}', 'raw_response': raw_text}

            except Exception as e:
                error_str = str(e)
                if any(s in error_str.lower() for s in ['rate_limit', 'overloaded', '529', '429']):
                    wait = min(2 ** (attempt + 2), 60)
                    await asyncio.sleep(wait)
                elif attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                else:
                    return {'error': str(e), 'raw_response': ''}

    return {'error': 'max retries exceeded', 'raw_response': ''}


async def main():
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set.")
        sys.exit(1)

    try:
        import anthropic
    except ImportError:
        os.system("pip install anthropic")
        import anthropic

    client = anthropic.AsyncAnthropic(api_key=api_key)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)

    # Load sample
    print("Loading sample...")
    df = pd.read_csv(INPUT_PATH, dtype={'complaint_id': 'int64'}, parse_dates=['date'])
    print(f"Loaded {len(df):,} narratives")

    # Check for checkpoint
    already_done = {}
    if os.path.exists(CHECKPOINT_PATH):
        checkpoint = pd.read_csv(CHECKPOINT_PATH, dtype={'complaint_id': 'int64'})
        for _, row in checkpoint.iterrows():
            already_done[row['complaint_id']] = row.to_dict()
        print(f"Resuming from checkpoint: {len(already_done):,} already classified")

    # Filter to remaining work
    remaining = df[~df['complaint_id'].isin(already_done)].copy()
    print(f"Remaining to classify: {len(remaining):,}")

    if len(remaining) == 0:
        print("All narratives already classified!")
        # Just copy checkpoint to output
        checkpoint.to_csv(OUTPUT_PATH, index=False)
        return

    # Process in batches for checkpointing
    results = list(already_done.values())
    failed = []
    start_time = time.time()
    batch_start = 0
    total_remaining = len(remaining)

    while batch_start < total_remaining:
        batch_end = min(batch_start + CHECKPOINT_INTERVAL, total_remaining)
        batch = remaining.iloc[batch_start:batch_end]

        # Create async tasks for the batch
        tasks = []
        row_data = []
        for _, row in batch.iterrows():
            narrative = str(row['narrative_text'])
            task = classify_one(client, narrative, semaphore)
            tasks.append(task)
            row_data.append(row)

        # Run batch concurrently
        batch_results = await asyncio.gather(*tasks)

        # Process results
        for row, result in zip(row_data, batch_results):
            if result and 'error' not in result:
                results.append({
                    'complaint_id': row['complaint_id'],
                    'product': row['product'],
                    'sub_product': row['sub_product'],
                    'product_group': row['product_group'],
                    'company': row['company'],
                    'date': row['date'],
                    'state': row['state'],
                    'narrative_text': str(row['narrative_text']),
                    'classification': result['classification'],
                    'confidence': result['confidence'],
                    'primary_evidence': result['primary_evidence'],
                    'secondary_signals': result['secondary_signals'],
                    'delegative_score': result['delegative_score'],
                    'evaluative_score': result['evaluative_score'],
                })
            else:
                error_info = result if result else {'error': 'unknown', 'raw_response': ''}
                failed.append({
                    'complaint_id': row['complaint_id'],
                    'error': error_info.get('error', 'unknown'),
                })
                results.append({
                    'complaint_id': row['complaint_id'],
                    'product': row['product'],
                    'sub_product': row['sub_product'],
                    'product_group': row['product_group'],
                    'company': row['company'],
                    'date': row['date'],
                    'state': row['state'],
                    'narrative_text': str(row['narrative_text']),
                    'classification': 'PARSE_ERROR',
                    'confidence': None,
                    'primary_evidence': error_info.get('raw_response', ''),
                    'secondary_signals': error_info.get('error', ''),
                    'delegative_score': None,
                    'evaluative_score': None,
                })

        # Save checkpoint
        results_df = pd.DataFrame(results)
        results_df.to_csv(CHECKPOINT_PATH, index=False)

        new_done = batch_end
        total_done = len(already_done) + new_done
        elapsed = time.time() - start_time
        rate = new_done / elapsed * 60 if elapsed > 0 else 0
        remaining_time = (total_remaining - new_done) / (rate / 60) if rate > 0 else 0

        print(f"  {total_done:,}/{len(df):,} done "
              f"({rate:.0f}/min, ~{remaining_time/60:.1f}h remaining) "
              f"| {len(failed)} failures")

        batch_start = batch_end

    # Final save
    final_df = pd.DataFrame(results)
    final_df.to_csv(OUTPUT_PATH, index=False)

    elapsed = time.time() - start_time
    print(f"\n{'=' * 70}")
    print(f"CLASSIFICATION COMPLETE")
    print(f"{'=' * 70}")
    print(f"Total classified: {len(final_df):,}")
    print(f"Failures: {len(failed)}")
    print(f"Elapsed: {elapsed/60:.1f} minutes")
    print(f"Saved to: {OUTPUT_PATH}")

    if failed:
        with open(FAILED_LOG, 'w') as f:
            for fail in failed:
                f.write(f"{fail}\n")
        print(f"Failure log: {FAILED_LOG}")

    # Quick distribution summary
    print(f"\nClassification distribution:")
    for cls, count in final_df['classification'].value_counts().items():
        pct = count / len(final_df) * 100
        print(f"  {cls}: {count:,} ({pct:.1f}%)")

    await client.close()


if __name__ == '__main__':
    asyncio.run(main())
