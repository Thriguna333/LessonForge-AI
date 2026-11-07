
import os

from research.research_engine import conduct_research
from quality_control.factual_checker import check_factual_accuracy
from quality_control.instructional_checker import check_instructional_quality


TITLE = "HTTP Requests and Responses"

OBJECTIVE = """
Explain how GET and POST requests work
and distinguish between 2xx, 4xx and 5xx
HTTP response status codes.
"""


try:
    print("Step 1: Loading generated lesson...")

    lesson_path = "outputs/generated_lesson.md"

    if not os.path.exists(lesson_path):
        raise FileNotFoundError(
            "Generated lesson not found. Run test_lesson.py first."
        )

    with open(lesson_path, "r", encoding="utf-8") as file:
        lesson = file.read()

    print("Lesson loaded successfully!")

    print("\nStep 2: Collecting research for factual audit...")
    research = conduct_research(TITLE)

    print("\nStep 3: Running QC1 - Factual Accuracy...")
    factual_report = check_factual_accuracy(
        lesson,
        research
    )

    print("\nStep 4: Running QC2 - Instructional Quality...")
    instructional_report = check_instructional_quality(
        lesson,
        TITLE,
        OBJECTIVE
    )

    os.makedirs("outputs", exist_ok=True)

    with open(
        "outputs/qc1_factual_report.md",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(factual_report)

    with open(
        "outputs/qc2_instructional_report.md",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(instructional_report)

    print("\nBoth quality checks completed successfully!")
    print("QC1 Report: outputs/qc1_factual_report.md")
    print("QC2 Report: outputs/qc2_instructional_report.md")

except Exception as error:
    print(f"\nQuality control failed: {error}")
