import ollama

# Load model (assuming llama3.2 is pulled)
model_name = "llama3.2"


def summarize_query_with_context(query: str, extracted_items: list[str]) -> str:
    """
    Summarize extracted web text using Ollama (local LLM).
    If Ollama fails → fallback manual summary is returned.
    """

    combined_text = "\n\n".join(extracted_items)
    combined_text = combined_text[:15000]  # avoid overloading

    prompt = f"""
You are InsightLoop.AI, an autonomous research assistant.

User query:
{query}

Web content (raw extracted text):
{combined_text}

Your task:
- Summarize the research into 6–10 bullet points
- Extract patterns, reasons, comparisons
- Give a clean structured answer
- Limit to ~300 words
"""

    # Try Ollama with retries
    for attempt in range(2):
        try:
            response = ollama.generate(model=model_name, prompt=prompt)
            out = (response.get('response', '') or "").strip()
            if len(out) > 10:
                return out
        except Exception:
            continue

    # FALLBACK SUMMARY (always returns something)
    fallback_bullets = []
    for text in extracted_items[:6]:
        if not text or text.startswith("Error fetching") or text.startswith("Error during extraction"):
            continue
        short = text.replace("\n", " ").strip()
        short = short[:200] + "..." if len(short) > 200 else short
        fallback_bullets.append(f"• {short}")

    if not fallback_bullets:
        return "No insights could be generated."

    return "Fallback Summary (Ollama unavailable):\n" + "\n".join(fallback_bullets)



def generate_comparison_table(query: str, extracted_items: list[str]) -> str:
    """
    Ask Ollama to create a markdown comparison table.
    On error → returns empty string.
    """

    combined_text = "\n\n".join(extracted_items)
    combined_text = combined_text[:15000]

    prompt = f"""
You are InsightLoop.AI, an autonomous web research assistant.

User query:
{query}

Web content (raw extracted text from multiple pages):
{combined_text}

Your task:
- If the query is about comparing companies, apps, tools, products, or failures,
  generate a clear, professional markdown table with a title.
- Columns should be relevant (e.g., Name, Category, Features, Pros, Cons, Notes).
- Use short, crisp phrases in each cell.
- Make the table visually appealing with proper alignment.
- Output ONLY the markdown table with a brief title.
- If you cannot create a table, output an empty string.
"""

    try:
        response = ollama.generate(model=model_name, prompt=prompt)
        table = (response.get('response', '') or "").strip()

        # Validate it's actually a table
        if "|" not in table:
            return ""

        return table

    except Exception:
        return ""
