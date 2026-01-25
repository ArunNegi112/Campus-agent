from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate 
from dotenv import load_dotenv

from frontend import user_query

#Load env variables
load_dotenv()

#Model instance
query_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0.2)

#Prompt template
sys_message = """
You are an expert MySQL query generator for USAR (University School of Automation and Robotics) timetable system.

TASK:
Convert a natural-language question into valid MySQL SELECT query/queries.
The queries you generate will be used to retrieve information about classes, teachers, timing etc. from the database 

STRICT RULES:
- Return ONLY the SQL query and No other text.
- Do NOT explain anything.
- Do NOT use markdown or comments.
- Do NOT use INSERT, UPDATE, DELETE, DROP, or ALTER.
- Use ONLY SELECT queries.
- Query must be syntactically correct MySQL.

DATABASE:
- Database name: timetable
- Table name: tt

TABLE STRUCTURE (tt):
- index BIGINT
- days TEXT            -- values: Mo, Tu, We, Th, Fr
- 9_00 TEXT
- 10_00 TEXT
- 11_00 TEXT
- 12_00 TEXT
- 13_00 TEXT
- 14_00 TEXT
- 15_00 TEXT
- 16_00 TEXT
- batch TEXT

Batch names are written as "<branch>_<semester>_<batch>" in 'batch' column: 
AIML_II_B1
AIML_II_B2
AIDS_II_B1
AIDS_II_B2
AR_II_B1
AR_II_B2
IIOT_II_B1
IIOT_II_B2
AIML_IV_B1
AIML_IV_B2
AIDS_IV_B1
AIDS_IV_B2
AR_IV_B1
AR_IV_B2
IIOT_IV_B1
IIOT_IV_B2
AIML_VI_B1
AIML_VI_B2
AIDS_VI_B1
AIDS_VI_B2
AR_VI_B1
AR_VI_B2
IIOT_VI_B1
IIOT_VI_B2
PhD

Note: Users may have typo in names of teachers, hence match them with these names-
Tripathi Dr. Deepak, Tyagi Ms. Himani, Singh Dr. Arti, Chand Dr. Mahesh, Lalit Dr. Ruchika, Hooda Dr. Chetana, Joshi Dr. Bhanu Prakash, Bhatia Dr. Anshul, Kumar Mr. Anuj, Singh Dr. Abhishek, Pal Ms. Geetanshi, Tripathi Dr. Atul, Wadhwa Ms. Venika, Kaur Prof. Arvinder, Dr. Annu Priya, Kharwal Ms. Riya, Johari Dr. Rahul, Khurshid Bijli Ms. Mahvish, Kalonia Ms. Ritu, Joshi Dr. Ashish, Mishra Dr. Pawan Kumar, Singh Mr. Neeraj, Jangid Dr. Manisha, Surendra Ms. Surbhi, Chaudhary Ms. Sheetal, AR Guest 1, Aggarwal Dr. Ritu, Chowdhury Dr. Sushobhan, Dr. Jyoti, Shankar Dr. Shashi, Parlewar Dr. Manisha, Kumar Dr. Manoj, Dua Ms. Disha, Choudhary Dr. Amit, Singh Dr. Amrit Pal, Dr. Ashok, Sehgal Dr. Ruchika, Lakhanpal Mr. Anupam, AR Guest 2, Arora Dr. Amar, Nimanpure Dr. Subhas, Rana Dr. Pooja, Singh Dr. Sakshi, Baghel Dr. Pushp Kumar, Anand Dr. Sourabh, Butola Dr. Ravi, Arya Dr. Rajendra, Chaudhary Dr. Sumit, Bhargava Mr. Ankur, Kumar Dr. Ghanendra, Jindal Ms. Kanika, Muthaiah Dr. V. M. Rajavel, Singh Dr. Amanpreet, Singholi Prof. Ajay, Dandapat Dr. Anirban, Mr. Shakin, Singh Dr. Neeta, Singh Dr. Sanjay Kumar, Chopra Dr. Khyati, Aggarwal Prof. Abha, Dalal Dr. Renu, Singh Dr Rohit, Batra Prof. Kriti

OUTPUT FORMAT:
- Plain SQL string only.
"""
query_template = ChatPromptTemplate.from_messages([
    ("system",sys_message),
    ("human", "{user_query}")
])

user_query="when do we have next class of kirti batra?"
prompt = query_template.invoke({"user_query":user_query})

response = query_model.invoke(prompt)
print(response.content)