import re
import pandas as pd
from google import genai
import json

#Initialize genai client 
client = genai.Client()

FILE_PATH = 'C:\\Users\\WELCOME\\Downloads\\HDFS_2k.log'
#W_FILE_PATH = 'C:\\Users\\WELCOME\\Downloads\\HDFS_2k_Modified.log'

#Function to clean up the log 
def cleanup(line):
     clean=[]
     print("Method called")
     cleaned = re.sub(r"blk_-?\d+", "BLOCKID", line)
     cleaned_ip = re.sub(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", "IP", cleaned)
     NUM=re.sub(r"size \d+", "size NUM", cleaned_ip)
     d=re.sub(r"/mnt/hadoop/dfs/data/current/subdir\d{1,2}", "/mnt/hadoop/dfs/data/current/subdir", NUM)
     clean=d.split(":")
     #print("Cleaned Data", cleaned)
     #with open(W_FILE_PATH, "w", encoding='utf-8') as FILE:
         # print("Inside file")
          #FILE.write(cleaned_ip)
     return clean[1]

def explain_anomaly(log_template):
     prompt = f"""
     You are a senior Site Reliability Engineer. Analyze this rare log template flagged as an anomaly:
     "{log_template}"

     Respond strictly in JSON format with these exact keys:
     - "root_cause": Clear technical explanation of the event.
     - "business impact": How this impacts the system or users.
     - "remediation_steps": A List of steps an engineer should take.
     """
     #call model
     try:
          response = client.models.generate_content(
          model='gemini-2.5-flash',
          contents=prompt,
          config=genai.types.GenerateContentConfig(
               response_mime_type="application/json"
          )
     )
     except genai.errors.APIError as e:
          print(f"API Failed: {e}. Retrying...")
     return response.text


Cleaned_List = []
with open(FILE_PATH, "r", encoding='utf-8') as FILE:
     
     for line in FILE:
          newline=line.strip()
          print(newline)
          returned = cleanup(newline)
          Cleaned_List.append(returned)
print(Cleaned_List)

df=pd.DataFrame(Cleaned_List, columns=['Template'])
cdf=df['Template'].value_counts()
cdf.to_csv('Anomaly_Report.csv', index=True)
anomalies = cdf[cdf < 25]

analysis_dict = []
for template in anomalies.index:
     print("Analyzing Anomaly: {template}")
     raw_json_response=explain_anomaly(template)
     analysis=json.loads(raw_json_response)
     print(analysis)
     print("-" * 50)
     analysis_dict.append(analysis)
     
report_df=pd.DataFrame(analysis_dict)
report_df.to_csv('LLM_Report.csv', index=False)