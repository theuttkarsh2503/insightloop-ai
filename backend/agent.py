# agent.py
# InsightLoop.AI - Agent Skeleton

from backend.search_tool import search_web
from backend.crawler import fetch_page
from backend.extractor import extract_information
from backend.llm_summarizer import summarize_query_with_context, generate_comparison_table





class InsightAgent:
    def __init__(self, query):
        self.query = query
        self.steps = []

    def log(self, message):
        self.steps.append(message)

    def run(self):
        self.log("Step 1: Planning the task...")

        self.log("Step 2: Searching the web...")
        search_results = search_web(self.query)
        self.log(f"Found {len(search_results)} relevant links.")
        self.log("Step 3: Crawling webpages...")
        pages = []
        for url in search_results:
            html = fetch_page(url)
            pages.append({"url": url, "html": html})
        self.log("Step 4: Extracting information...")
        extracted_texts = []
        for page in pages:
            text = extract_information(page["html"])
            extracted_texts.append({"url": page["url"], "text": text})
        self.log("Step 5: Generating AI summary from extracted data...")
        snippets = [item["text"] for item in extracted_texts]
        summary = summarize_query_with_context(self.query, snippets)

        self.log("Step 6: Building comparison table (if applicable)...")
        comparison_table = generate_comparison_table(self.query, snippets)

        self.log("Step 7: (Future) Generating PDF report...")
        self.log("Step 8: (Future) Sending report via email...")


        return {
            "status": "success",
            "query": self.query,
            "steps": self.steps,
            "links": search_results,
            "raw_pages": pages,
            "extracted": extracted_texts,
            "insights": summary,
            "comparison_table": comparison_table,
        }


