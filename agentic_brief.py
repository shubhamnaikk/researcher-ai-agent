"""
Agentic Researcher -> 1-page brief (with sources + fact-check pass)
- Uses OpenAI Responses API + built-in web_search tool
- Produces: Summary, Key points, Pros/Cons, Risks, Next steps, Sources
- Then runs a "fact-check" pass that flags claims that seem unsupported by the cited sources.

Requirements:
  pip install -U openai python-dotenv
Env:
  export OPENAI_API_KEY="..."
Usage:
  python agentic_brief.py "Your topic question here" --out brief.md
"""

from __future__ import annotations

import argparse
import os
import re
from datetime import datetime
from typing import Optional

from openai import OpenAI
from dotenv import load_dotenv


SYSTEM_STYLE = """You are a careful research assistant.
Rules:
- Use the web_search tool to gather up-to-date information.
- Do not guess. If sources disagree or data is uncertain, say so.
- Prefer authoritative sources (gov, universities, major journals, reputable news).
- Write concisely in a 1-page brief format.
- Every non-trivial factual claim should be supported by a source in the Sources section.
- Include absolute dates when referencing "recent" events.
"""

BRIEF_INSTRUCTIONS = """Create a 1-page research brief on the user's topic.

Format exactly as:

# Title
**Date:** <today>

## Executive summary (5 bullets)
- ...

## Key points (6–10 bullets)
- ...

## Pros / opportunities (3–6 bullets)
- ...

## Cons / tradeoffs (3–6 bullets)
- ...

## Risks / uncertainties (3–6 bullets)
- ...

## Next steps (5 bullets)
- Each bullet should be an actionable next step.

## Sources
- [1] <Title> — <Publisher/Org> (<YYYY-MM-DD if available>) <URL>
- [2] ...

Constraints:
- Keep it within ~500–900 words.
- If you can't find credible sources, say so and explain what’s missing.
"""

FACTCHECK_INSTRUCTIONS = """You are now a fact-checker.

Input will be the brief you wrote.
Task:
1) List 5–12 important claims from the brief that should be verifiable.
2) For each claim, label: Supported / Partially supported / Not supported
3) For Partially/Not supported: explain what is missing or contradictory and suggest a safer rewrite.
4) If sources disagree, label "Partially supported" and describe the disagreement.

Return format:

# Fact-check
## Claims review
1) Claim: ...
   Verdict: Supported|Partially supported|Not supported
   Notes: ...
   Safer rewrite (if needed): ...

Keep it tight.
"""

def today_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")

def sanitize_markdown(md: str) -> str:
    # Ensure a Date line exists; replace placeholder if needed
    md = re.sub(r"\*\*Date:\*\*\s*<today>", f"**Date:** {today_str()}", md)
    return md.strip() + "\n"

def write_file(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def make_client() -> OpenAI:
    # OPENAI_API_KEY is automatically read by the SDK
    return OpenAI()

def generate_brief(client: OpenAI, topic: str, model: str) -> tuple[str, str]:
    """
    Returns:
      (brief_markdown, previous_response_id)
    We keep previous_response_id so the follow-up fact-check can reuse context.
    """
    prompt = f"{BRIEF_INSTRUCTIONS}\n\nUser topic:\n{topic}\n"

    resp = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": SYSTEM_STYLE},
            {"role": "user", "content": prompt},
        ],
        # Built-in web search tool (agentic loop handled by Responses API)
        tools=[{"type": "web_search"}],
    )

    brief = resp.output_text or ""
    brief = sanitize_markdown(brief)
    prev_id = getattr(resp, "id", None) or ""
    return brief, prev_id

def fact_check(client: OpenAI, brief_markdown: str, model: str, previous_response_id: Optional[str] = None) -> str:
    """
    Fact-check pass. We feed the brief back and ask for claim verification.
    Using previous_response_id helps keep tool context if supported.
    """
    input_items = [
        {"role": "system", "content": SYSTEM_STYLE},
        {"role": "user", "content": FACTCHECK_INSTRUCTIONS + "\n\n---\n\n" + brief_markdown},
    ]

    kwargs = {}
    if previous_response_id:
        # Responses API can carry conversation state this way for follow-ups
        # (If unsupported by your SDK version, remove this and it will still work.)
        kwargs["previous_response_id"] = previous_response_id

    resp = client.responses.create(
        model=model,
        input=input_items,
        # Allow web search again if the fact-checker needs to resolve ambiguities
        tools=[{"type": "web_search"}],
        **kwargs,
    )

    fc = resp.output_text or ""
    return fc.strip() + "\n"

def main() -> None:
    parser = argparse.ArgumentParser(description="Agentic Researcher -> 1-page brief with sources + fact-check")
    parser.add_argument("topic", type=str, help="Topic or question to research")
    parser.add_argument("--model", type=str, default="gpt-5.2", help="Model name (default: gpt-5.2)")
    parser.add_argument("--out", type=str, default="", help="Optional output markdown file path (e.g., brief.md)")
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Missing OPENAI_API_KEY. Set it via environment variable or .env file.")

    client = make_client()

    brief, prev_id = generate_brief(client, args.topic, args.model)
    fc = fact_check(client, brief, args.model, previous_response_id=prev_id)

    final_md = brief + "\n---\n\n" + fc

    if args.out:
        write_file(args.out, final_md)
        print(f"Wrote: {args.out}")
    else:
        print(final_md)

if __name__ == "__main__":
    main()