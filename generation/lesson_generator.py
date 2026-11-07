
from config import generate_response


def generate_lesson(title: str, objective: str, research: dict):
    """Generate a structured 45-minute lesson using Gemini."""

    if not title or not title.strip():
        raise ValueError("Lesson title cannot be empty.")

    if not objective or not objective.strip():
        raise ValueError("Learning objective cannot be empty.")

    websites = research.get("websites", [])
    books = research.get("books", [])
    youtube = research.get("youtube", [])

    prompt = f"""
You are an expert instructional designer.

Create a complete beginner-friendly lesson.

LESSON TITLE:
{title}

LEARNING OBJECTIVE:
{objective}

RESEARCH MATERIALS:

WEBSITES:
{websites}

BOOKS:
{books}

YOUTUBE VIDEOS:
{youtube}

Create a lesson that takes exactly 45 minutes.

Use this structure:

1. Lesson Overview
2. Learning Objectives
3. Introduction (5 minutes)
4. Main Concepts and Explanations (15 minutes)
5. Practical Examples and Applications (10 minutes)
6. Hands-on Activity (10 minutes)
7. Knowledge Check (5 minutes)
8. Summary
9. References

Requirements:
- Explain concepts in simple language.
- Include practical examples.
- Include GET and POST examples for HTTP.
- Explain 2xx, 4xx and 5xx status codes.
- Include at least five questions with answers.
- Use supplied research as references.
- Never invent sources, URLs or authors.
- Clearly mention insufficient research.
- Return the complete lesson in Markdown.
"""

    return generate_response(prompt)


def apply_qc_recommendations(
    lesson: str,
    qc1_report: str,
    qc2_report: str
):
    """Improve the lesson using both independent QC reports."""

    if not lesson or not lesson.strip():
        raise ValueError("Lesson content cannot be empty.")

    if not qc1_report or not qc1_report.strip():
        raise ValueError("QC1 report is required.")

    if not qc2_report or not qc2_report.strip():
        raise ValueError("QC2 report is required.")

    prompt = f"""
You are an expert instructional designer and lesson editor.

Improve the lesson using the two independent quality audit reports.

ORIGINAL LESSON:
{lesson}

QC1 - FACTUAL ACCURACY REPORT:
{qc1_report}

QC2 - INSTRUCTIONAL QUALITY REPORT:
{qc2_report}

INSTRUCTIONS:

1. Correct factual errors identified by QC1.
2. Address unsupported or misleading claims.
3. Improve explanations and examples.
4. Address learning objective alignment.
5. Improve activities and knowledge checks.
6. Ensure the lesson fits within 45 minutes.
7. Preserve accurate original content.
8. Never invent references, facts or sources.
9. Do not blindly apply incorrect recommendations.
10. Preserve Markdown formatting.

Return only the complete improved lesson in Markdown.
"""

    return generate_response(prompt)
