# Automated Log Analyzer & AI Error Summarizer 

A Python-based data pipeline that ingests raw production logs, cleans and aggregates repetitive templates using regular expressions and leverages the Gemini API to automatically generate root-cause analysis and remediation steps for critical system anomalies.

## Key Features
* **Regex Log Parsing:** Automatically strips timestamps, IPs, and specific block IDs to isolate core log messages.
* **Volume Aggregation:** Calculates baseline frequencies for all log templates to identify normal system behavior.
* **Anomaly Detection:** Filters out high-frequency operational chatter to isolate rare errors (templates appearing fewer than 25 times).
* **AI-Powered Enrichment:** Sends anomalous templates to the Gemini LLM to extract root causes, business impacts, and actionable remediation steps in structured JSON.

## Data Pipeline Architecture
1. **Ingestion & Cleanup:** Reads raw log files line-by-line and applies regex cleaning.
2. **Aggregation:** Generates an initial summary dataset (`Anomaly_Report.csv`) tracking total counts per unique log template.
3. **Filtering:** Screens for low-frequency anomalies based on user-defined thresholds.
4. **Enrichment:** Utilizes GenAI to produce a final executive report (`LLM_Report.csv`) containing technical insights for on-call engineers.

## Setup & Installation
1. Clone this repository:
   ```bash
   git clone [https://github.com/Dayanidhi29/LogIntelligenceProject.git](https://github.com/Dayanidhi29/LogIntelligenceProject.git)
2.Set up your virtual environment and install dependencies (Pandas, Google GenAI).
3.Configure your Gemini API Key.
4.Run the application: python main.py