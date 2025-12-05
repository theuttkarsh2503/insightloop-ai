<p align="center">
  <img src="https://img.shields.io/badge/AI-Agentic-blue?style=for-the-badge&logo=spark" />
  <img src="https://img.shields.io/badge/Web%20Scraping-Automated-green?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Report-Auto--Generated-orange?style=for-the-badge&logo=adobeacrobatreader" />
  <img src="https://img.shields.io/badge/Python-3.10+-yellow?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/LLM-Powered-purple?style=for-the-badge&logo=openai" />
</p>

<p align="center">
  <img width="100%" src="https://dummyimage.com/1200x260/0f172a/ffffff&text=InsightLoop.AI+-+Autonomous+Web+Research+Agent" />
</p>

<h1 align="center">🔍 InsightLoop.AI</h1>
<p align="center">Autonomous Web Research & Insight Generation Agent</p>


🚀 **InsightLoop.AI – Autonomous Web Research Agent**

**Give it a question. It explores the web, extracts structured insights, and delivers a PDF report — autonomously.**

InsightLoop.AI is an **agentic AI-powered autonomous research system** that takes any user query, browses the web, extracts structured information, analyzes content, builds comparison tables, generates a polished PDF report, and emails it — all without human intervention.

Built by **Team Code Wode** for the hackathon under the theme:
**Agentic AI & Autonomous Systems**

---

🧠 **Why InsightLoop.AI?**

Today’s research process is:

* Time-consuming
* Manual (search → read → extract → summarize)
* Requires expertise
* Easily biased or incomplete
* Slow to produce structured reports

**InsightLoop.AI automates the entire loop**, transforming raw queries into professional, structured insights in minutes.

---

# ⚡ **Core Features**

✅ **1. Autonomous Task Planning**

LLM agent divides the user query into actionable sub-tasks and executes them sequentially.

✅ **2. Web Search & Crawling**

Automatically searches the internet using APIs, retrieves relevant links, and fetches webpage contents.

✅ **3. AI-Powered Knowledge Extraction**

InsightLoop.AI extracts:

* Key facts
* Numeric values
* Entity attributes
* Trends & patterns
* Quotations & summaries

✅ **4. Data Aggregation & Insight Generation**

Combines extracted data across sources, removes duplicates, and builds simplified insight summaries.

✅ **5. Automatic PDF Report**

Generates:

* Executive summary
* Comparison tables
* Insight analysis
* Clean formatted research report

✅ **6. Email Delivery**

Delivers the final PDF report directly to the user’s inbox.

---

# 🎯 **Example Use Case**

**Query:**

> “Find top 10 fintech apps that failed; compare UI, UX, problems, revenue.”

**InsightLoop.AI autonomously:**

* Identifies 10 failed fintech apps
* Extracts 8–10 attributes from multiple sources
* Builds a comparison table
* Summarizes common failure reasons
* Generates a PDF report
* Emails it to the user

No manual searching required.

---

# 🏗️ **Architecture Overview**

```
User Query
      ↓
Agentic Planner (LLM)
      ↓
Web Search Tool → URL Fetcher → HTML Extractor
      ↓
LLM Data Extractor (Structured Outputs)
      ↓
Data Aggregator → Insight Engine
      ↓
PDF Generator
      ↓
Email Delivery System
```

InsightLoop.AI runs this loop automatically until the task is completed.

---

# 🔧 **Tech Stack**

### **Backend**

* Python
* FastAPI / Flask

### **Frontend**

* Streamlit or simple HTML interface

### **AI Models**

* OpenAI GPT / Groq LLM

### **Tools & Libraries**

* **Search:** SerpAPI, Bing Web Search API
* **Scraping:** Requests, BeautifulSoup
* **Agents:** Custom Planning & Tool Execution Loop
* **PDF:** ReportLab / FPDF
* **Email:** SMTP, SendGrid
* **Database (Optional):** Firebase / MongoDB

---

# 📁 **Folder Structure**

```
insightloop-ai/
│
├── backend/
│   ├── main.py
│   ├── agent.py
│   ├── search_tool.py
│   ├── crawler.py
│   ├── extractor.py
│   ├── aggregator.py
│   ├── pdf_generator.py
│   └── email_sender.py
│
├── frontend/
│   └── app.py
│
├── requirements.txt
└── README.md
```

---

# 📊 **Impact**

**1. Productivity**

* Reduces 5 hours of research → 5 minutes
* Automates analyst-level work
* Produces consistent, unbiased reports

**2. Business Value**

* Useful for founders, researchers, analysts, investors
* Rapid competitive & market research
* Trend and failure analysis

**3. Scalability**

* Works across any domain: fintech, edtech, health, politics
* Can be deployed as SaaS or API

**4. Innovation**

* Agentic decision-making
* Web-crawling + AI extraction + PDF generation
* More than a chatbot — a true autonomous system

---

🗺️ **Future Enhancements**

* Multi-agent collaboration (research + summarizer + verifier)
* Automatic charts & visual insights
* Real-time dashboard for saved reports
* Citation detection & source scoring
* Voice queries & mobile app
* Enterprise API integration

---

👨‍💻 **Team – Code Wode**

* Prakhar Batwal
* Yuvraj Dwivedi
* Uttkarsh

---

🏁 **Conclusion**

InsightLoop.AI transforms messy, time-consuming web research into a **fast, autonomous, insight-rich workflow** powered by agentic AI.

It completes the entire loop:
**Query → Web Search → Extraction → Insights → PDF → Email**

> ⚡ **InsightLoop.AI — Where questions turn into insights, automatically.**
