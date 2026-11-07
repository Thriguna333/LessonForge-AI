
from research.research_engine import conduct_research

query = "HTTP requests and responses in web development"

print("Starting research...")

results = conduct_research(query)

for source, items in results.items():
    print(f"\n{'=' * 45}")
    print(f"{source.upper()}")
    print(f"{'=' * 45}")

    if not items:
        print("No results found.")
        continue

    for index, item in enumerate(items, 1):
        print(f"\n{index}. {item.get('title')}")

        if item.get("url"):
            print("URL:", item["url"])

        if item.get("snippet"):
            print("Snippet:", item["snippet"][:200])

print("\nResearch completed!")
