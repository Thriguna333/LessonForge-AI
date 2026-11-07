
from config import generate_response


def check_instructional_quality(
    lesson: str,
    title: str,
    objective: str
):
    """Audit lesson structure and instructional effectiveness."""

    if not lesson or not lesson.strip():
        raise ValueError("Lesson content cannot be empty.")

    if not objective or not objective.strip():
        raise ValueError("Learning objective cannot be empty.")

    prompt = f"""
You are an independent instructional design quality auditor.

Review the lesson for instructional quality.

LESSON TITLE:
{title}

LEARNING OBJECTIVE:
{objective}

GENERATED LESSON:
{lesson}

Evaluate the following areas:

1. Objective alignment:
   Does the lesson actually achieve the stated learning objective?

2. Clarity:
   Are explanations easy for beginners to understand?

3. Structure:
   Is the lesson organized logically?

4. Examples:
   Are examples relevant and understandable?

5. Practical applications:
   Does the lesson connect concepts to real-world situations?

6. Activities:
   Are activities useful and appropriate for learners?

7. Knowledge checks:
   Do questions test the stated learning objective?

8. Time allocation:
   Can the lesson realistically be completed in 45 minutes,
   including activities and knowledge checks?

IMPORTANT:
- Evaluate the actual lesson, not an imagined version.
- Do not invent missing content.
- Identify specific weaknesses with examples.
- Suggest practical improvements for every issue.
- Check whether the learning objective is measurable.
- If a section is missing, explicitly mention it.

Return the report in Markdown using these headings:

# QC2: Instructional Quality Audit

## Overall Assessment
## Learning Objective Alignment
## Clarity and Explanations
## Lesson Structure
## Examples and Practical Applications
## Activities and Knowledge Checks
## 45-Minute Time Feasibility
## Missing Elements
## Suggested Improvements
## Final QC2 Verdict

For the final verdict, choose:
PASS, PASS WITH WARNINGS, or FAIL.
"""

    return generate_response(prompt)
