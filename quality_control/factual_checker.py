
from config import generate_response


def check_factual_accuracy(lesson: str, research: dict):
    """Audit lesson content for factual accuracy and source reliability."""

    if not lesson or not lesson.strip():
        raise ValueError("Lesson content cannot be empty.")

    research_material = {
        "websites": research.get("websites", []),
        "books": research.get("books", []),
        "youtube": research.get("youtube", [])
    }

    prompt = f"""
You are an independent factual accuracy auditor.

Your task is to review the lesson using the supplied research.

LESSON:
{lesson}

RESEARCH MATERIAL:
{research_material}

Perform a detailed factual audit.

Check:

1. Factual correctness.
2. Unsupported or misleading claims.
3. Reliability and relevance of references.
4. Missing important facts.
5. Contradictions or inconsistencies.

IMPORTANT:
- Do not assume every supplied source is reliable.
- Do not invent facts or references.
- Do not claim you verified a source if you only received its title or URL.
- Distinguish verified issues from claims that need further verification.
- Give specific examples from the lesson.
- Suggest a correction for every identified issue.
- If no issue is found, say so clearly.

Return the report in Markdown using these headings:

# QC1: Factual Accuracy Audit

## Overall Assessment
## Factual Issues
## Unsupported or Misleading Claims
## Source Reliability and Relevance
## Missing Information
## Suggested Corrections
## Final QC1 Verdict

For the final verdict, choose:
PASS, PASS WITH WARNINGS, or FAIL.
"""

    return generate_response(prompt)
