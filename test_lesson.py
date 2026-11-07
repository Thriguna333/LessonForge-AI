
import os
from research.research_engine import conduct_research
from generation.lesson_generator import generate_lesson

title = "HTTP Requests and Responses"

objective = """
Explain how GET and POST requests work
and distinguish between 2xx, 4xx and 5xx
HTTP response status codes.
"""

try:
    print("Step 1: Collecting research...")
    research = conduct_research(title)

    print("Step 2: Generating lesson using Gemini...")
    lesson = generate_lesson(title, objective, research)

    # Create outputs folder automatically if missing
    os.makedirs("outputs", exist_ok=True)

    # Save generated lesson
    with open(
        "outputs/generated_lesson.md",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(lesson)

    print("\nLesson generated successfully!")
    print("Saved at: outputs/generated_lesson.md")

except Exception as error:
    print(f"\nLesson generation failed: {error}")
