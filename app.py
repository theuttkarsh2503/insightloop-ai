# app.py
# InsightLoop.AI - Step 1: Basic UI
from backend.agent import InsightAgent
from backend.pdf_generator import generate_pdf
from backend.email_sender import send_email
from backend.db import init_db, save_report, get_recent_reports, get_report_by_query, update_rating, clear_history

import pandas as pd
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json

# Initialize database
init_db()

# Function to parse Markdown table to DataFrame
def markdown_table_to_df(table_md: str) -> pd.DataFrame:
    lines = table_md.strip().split('\n')
    if len(lines) < 3:
        return pd.DataFrame()

    # Remove header separator
    table_lines = [line for line in lines if '---' not in line]

    # Parse
    data = []
    headers = [h.strip() for h in table_lines[0].split('|')[1:-1]]
    for line in table_lines[1:]:
        if '|' in line:
            row = [cell.strip() for cell in line.split('|')[1:-1]]
            data.append(row)

    if not headers or not data:
        return pd.DataFrame()

    # Ensure all rows have the same number of columns
    if len(data[0]) != len(headers):
        return pd.DataFrame()

    return pd.DataFrame(data, columns=headers)

# Page title
st.set_page_config(page_title="InsightLoop.AI", page_icon="🔍", layout="wide")

st.title("🔍 InsightLoop.AI")
st.subheader("🚀 Autonomous Web Research & Insight Generation Agent")

st.write(
    "💡 Give me a research question, and I'll autonomously browse the web, extract insights, "
    "and generate a beautiful report for you!"
)

# Sidebar for history
st.sidebar.title("📚 Query History")
search_history = st.sidebar.text_input("Search history", placeholder="Filter queries...")
if st.sidebar.button("Clear History"):
    clear_history()
    st.sidebar.success("History cleared!")

dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=False)
if dark_mode:
    st.markdown("""
    <style>
    .stApp {
        background-color: #1e1e1e;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

recent_queries = get_recent_reports(10, search_history)
for i, past_query in enumerate(recent_queries):
    if st.sidebar.button(f"🔄 {past_query[:50]}...", key=f"history_{i}"):
        query = past_query
        st.rerun()

# Text input from user
query = st.text_area(
    "Enter your research query:",
    placeholder="e.g. Find top 10 fintech apps that failed; compare UI, UX, problems, revenue.",
    height=100
)

run_button = st.button("🚀 Run InsightLoop", type="primary")

if run_button and query.strip():
    # Add to history
    if query not in get_recent_reports(100):  # Avoid duplicates
        pass  # Will save after

    progress_bar = st.progress(0)
    status_text = st.empty()

    status_text.text("🔍 Searching the web...")
    progress_bar.progress(20)

    with st.spinner("🤖 InsightLoop is researching... This may take a minute!"):
        agent = InsightAgent(query)
        result = agent.run()

    progress_bar.progress(80)
    status_text.text("📝 Generating insights...")

    # Simulate final processing
    import time
    time.sleep(0.5)

    progress_bar.progress(100)
    status_text.text("✅ Complete!")

    st.success("🎉 Research complete! Insights generated.")

    # Save to DB
    report_id = save_report(query, result.get("insights", ""), result.get("links", []), result.get("extracted", []), result.get("comparison_table", ""))

    progress_bar.empty()
    status_text.empty()

    # Rating
    st.write("### ⭐ Rate this Report")
    rating = st.slider("How useful was this report?", 1, 5, 3, key="rating")
    if st.button("Submit Rating"):
        update_rating(report_id, rating)
        st.success("Rating saved!")

    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("🔗 Sources Found", len(result.get("links", [])))
    col2.metric("📝 Insights Length", len(result.get("insights", "")))
    col3.metric("📊 Table Generated", "Yes" if result.get("comparison_table") else "No")

    st.write("### 🔄 Steps Performed:")
    for step in result["steps"]:
        st.write("- " + step)
    st.write("### 🔗 Search Results (URLs):")
    for url in result.get("links", []):
        st.write("- " + url)
    # ==============================
    # NEW SECTION: Extracted Text
    # ==============================
    st.write("### 🧾 Extracted Text Snippets:")

    for item in result.get("extracted", []):
        st.write(f"**Source:** {item['url']}")
        st.write(item["text"][:500] + "...")
        st.markdown("---")

    st.write("### 📘 Insights:")
    st.info(result["insights"])

    # Word Cloud
    st.write("### ☁️ Word Cloud from Insights")
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(result["insights"])
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

    table_md = result.get("comparison_table", "")
    if table_md:
        st.write("### 📊 Comparison Table")
        df = markdown_table_to_df(table_md)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Table as CSV",
                data=csv,
                file_name="comparison_table.csv",
                mime="text/csv",
            )
        else:
            st.markdown(table_md)


    # ---- PDF REPORT DOWNLOAD ----
    pdf_bytes = generate_pdf(
        query=query,
        links=result.get("links", []),
        insights=result.get("insights", ""),
        extracted=result.get("extracted", []),
        comparison_table=table_md,
    )

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_bytes,
        file_name="insightloop_report.pdf",
        mime="application/pdf",
    )

    # JSON Export
    json_data = json.dumps(result, indent=4)
    st.download_button(
        label="📋 Download JSON Data",
        data=json_data,
        file_name="insightloop_report.json",
        mime="application/json",
    )

    # ---- EMAIL REPORT ----
    st.subheader("📧 Send Report via Email")
    st.info("To send emails, set EMAIL_USER and EMAIL_PASS environment variables (e.g., for Gmail, use app password).")
    email = st.text_input("Enter your email address", placeholder="user@example.com")
    if st.button("Send Report"):
        if email:
            status = send_email(email, pdf_bytes, query)
            st.success(status)
        else:
            st.error("Please enter a valid email address.")

st.markdown("---")
st.markdown("**InsightLoop.AI v1.0** - Powered by Ollama & Streamlit. Built for autonomous research.")


