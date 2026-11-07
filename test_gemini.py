from config import generate_response

try:
    print("Connecting to Gemini...")

    response = generate_response(
        "Explain what Artificial Intelligence is in three simple sentences."
    )

    print("\nGemini Response:")
    print(response)

    print("\nGemini connection successful!")

except Exception as error:
    print(f"\nConnection failed: {error}")