"""
Stage 2: GPT-4o classification of the full 9,000-narrative dataset.

Uses the SAME classification prompt as the Claude Sonnet classifier
(from cfpb_stage2_prompt_revised_20260222.md) but routed through
OpenAI's GPT-4o API, for inter-rater reliability comparison.

Requires: OPENAI_API_KEY environment variable.
Input:  data/classification_sample_9000.csv (9,000 narratives)
Output: output/cfpb_gpt4o_classified_9000.csv (GPT-4o classifications)
"""

import pandas as pd
import json
import os
import sys
import time
import asyncio
import traceback

INPUT_PATH = "/workspaces/HumanxAI-2026/data/classification_sample_9000.csv"
OUTPUT_PATH = "/workspaces/HumanxAI-2026/output/cfpb_gpt4o_classified_9000.csv"
CHECKPOINT_PATH = "/workspaces/HumanxAI-2026/output/cfpb_gpt4o_classified_9000_checkpoint.csv"
FAILED_LOG = "/workspaces/HumanxAI-2026/output/cfpb_gpt4o_9000_failures.log"

MODEL = "gpt-4o"
MAX_CONCURRENT = 5
TEMPERATURE = 0.0
MAX_TOKENS = 300

# ── Same prompts as the Claude classifier ──────────────────────────────

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
    """Classify a single narrative via GPT-4o with rate limiting."""
    user_prompt = make_user_prompt(narrative_text)

    async with semaphore:
        raw_text = ""
        for attempt in range(max_retries):
            try:
                response = await client.chat.completions.create(
                    model=MODEL,
                    temperature=TEMPERATURE,
                    max_tokens=MAX_TOKENS,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt},
                    ],
                )
                raw_text = response.choices[0].message.content
                return parse_response(raw_text)

            except json.JSONDecodeError as e:
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                else:
                    return {'error': f'JSON parse failed: {e}', 'raw_response': raw_text}

            except Exception as e:
                error_str = str(e)
                if any(s in error_str.lower() for s in ['rate_limit', 'rate limit', '429']):
                    wait = min(2 ** (attempt + 2), 60)
                    print(f"    Rate limited, waiting {wait}s...")
                    await asyncio.sleep(wait)
                elif attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                else:
                    return {'error': str(e), 'raw_response': raw_text}

    return {'error': 'max retries exceeded', 'raw_response': ''}


BATCH_SIZE = 100  # process and checkpoint in batches of 100


def build_row(row, result):
    """Build an output row from input row + classification result."""
    if result and 'error' not in result:
        return {
            'complaint_id': row['complaint_id'],
            'product_group': row['product_group'],
            'classification': result['classification'],
            'confidence': result['confidence'],
            'delegative_score': result['delegative_score'],
            'evaluative_score': result['evaluative_score'],
            'primary_evidence': result['primary_evidence'],
            'secondary_signals': result['secondary_signals'],
        }, None
    else:
        error_info = result if result else {'error': 'unknown', 'raw_response': ''}
        return {
            'complaint_id': row['complaint_id'],
            'product_group': row['product_group'],
            'classification': 'PARSE_ERROR',
            'confidence': None,
            'delegative_score': None,
            'evaluative_score': None,
            'primary_evidence': error_info.get('raw_response', ''),
            'secondary_signals': error_info.get('error', ''),
        }, {'complaint_id': row['complaint_id'], 'error': error_info.get('error', 'unknown')}


async def main():
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set.")
        print("  export OPENAI_API_KEY='sk-...'")
        sys.exit(1)

    try:
        from openai import AsyncOpenAI
    except ImportError:
        print("Installing openai package...")
        os.system("pip install openai")
        from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=api_key)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)

    # Load the 9,000 narratives
    print("Loading 9,000-narrative dataset...")
    df = pd.read_csv(INPUT_PATH, dtype={'complaint_id': 'int64'}, parse_dates=['date'])
    print(f"Loaded {len(df)} narratives")

    # Check for checkpoint — resume if it exists
    done_ids = set()
    results = []
    if os.path.exists(CHECKPOINT_PATH):
        checkpoint_df = pd.read_csv(CHECKPOINT_PATH, dtype={'complaint_id': 'int64'})
        done_ids = set(checkpoint_df['complaint_id'].tolist())
        results = checkpoint_df.to_dict('records')
        print(f"Resuming from checkpoint: {len(done_ids)} already classified")

    remaining = df[~df['complaint_id'].isin(done_ids)].reset_index(drop=True)
    total = len(df)
    already_done = len(done_ids)
    print(f"Remaining to classify: {len(remaining)}")

    print(f"\nClassifying with {MODEL} (temperature={TEMPERATURE})...")
    print(f"Concurrency: {MAX_CONCURRENT}, batch size: {BATCH_SIZE}")
    start_time = time.time()
    failed = []

    # Process in batches of BATCH_SIZE, checkpoint after each batch
    for batch_start in range(0, len(remaining), BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, len(remaining))
        batch_df = remaining.iloc[batch_start:batch_end]

        # Fire off batch concurrently
        tasks = []
        for _, row in batch_df.iterrows():
            narrative = str(row['narrative_text'])
            tasks.append(classify_one(client, narrative, semaphore))
        batch_results = await asyncio.gather(*tasks)

        # Process batch results
        for i, (_, row) in enumerate(batch_df.iterrows()):
            out_row, fail = build_row(row, batch_results[i])
            results.append(out_row)
            if fail:
                failed.append(fail)

        # Save checkpoint
        checkpoint_df = pd.DataFrame(results)
        checkpoint_df.to_csv(CHECKPOINT_PATH, index=False)

        # Progress
        done_now = already_done + batch_end
        elapsed = time.time() - start_time
        classified_this_run = batch_end
        rate = classified_this_run / elapsed if elapsed > 0 else 0
        remaining_count = total - done_now
        eta = remaining_count / rate if rate > 0 else 0
        print(f"  [{done_now}/{total}] {elapsed:.0f}s elapsed, "
              f"{rate:.1f}/s, ~{eta:.0f}s remaining — checkpoint saved")

    # Final output
    results_df = pd.DataFrame(results)
    results_df.to_csv(OUTPUT_PATH, index=False)

    # Clean up checkpoint
    if os.path.exists(CHECKPOINT_PATH):
        os.remove(CHECKPOINT_PATH)

    elapsed = time.time() - start_time
    print(f"\n{'=' * 70}")
    print(f"GPT-4o CLASSIFICATION COMPLETE")
    print(f"{'=' * 70}")
    print(f"Total classified: {len(results_df)}")
    print(f"Failures: {len(failed)}")
    print(f"Elapsed: {elapsed:.1f} seconds")
    print(f"Saved to: {OUTPUT_PATH}")

    if failed:
        with open(FAILED_LOG, 'w') as f:
            for fail in failed:
                f.write(f"{fail}\n")
        print(f"Failure log: {FAILED_LOG}")

    # Distribution summary
    valid = results_df[results_df['classification'] != 'PARSE_ERROR']
    print(f"\nClassification distribution:")
    for cls, count in valid['classification'].value_counts().items():
        pct = count / len(valid) * 100
        print(f"  {cls}: {count} ({pct:.1f}%)")

    # Mean scores
    print(f"\nMean scores:")
    for cls in ['EVALUATIVE', 'DELEGATIVE', 'UNCLASSIFIABLE']:
        subset = valid[valid['classification'] == cls]
        if len(subset) > 0:
            d = subset['delegative_score'].mean()
            e = subset['evaluative_score'].mean()
            c = subset['confidence'].mean()
            print(f"  {cls}: deleg={d:.3f}, eval={e:.3f}, conf={c:.3f} (n={len(subset)})")

    await client.close()


if __name__ == '__main__':
    asyncio.run(main())
