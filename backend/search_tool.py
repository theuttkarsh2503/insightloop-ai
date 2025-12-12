# search_tool.py
# Real web search using Tavily

from tavily import TavilyClient
import os

# Make sure to set key in environment variable or hardcode temporarily
client = TavilyClient(api_key="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")

def search_web(query):
    try:
        results = client.search(query=query, max_results=5)

        urls = []
        for item in results.get("results", []):
            urls.append(item["url"])

        return urls
    
    except Exception as e:
        return [f"Error during search: {e}"]
