from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate 
from dotenv import load_dotenv

from frontend import user_query

#Load env variables
load_dotenv()

#Model instance
query_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0)

#Prompt template
system_message = """
You are an AI assistant for Campus Chatbot.

Your task is to convert natural-language questions into valid MySQL SELECT queries.
Return ONLY SQL queries. Do not explain anything.

Database:
- Database name: timetable
- MySQL dialect

Tables:
- Tables follow the naming pattern:
  <branch>_<semester>_<batch>
  Example: aids_ii_b1, aiml_iv_b2, ar_vi_b1
- All table names are lowercase.
- Exception: phd (single table)

Table names:
aids_ii_b1
aids_ii_b2
aids_iv_b1
aids_iv_b2
aids_vi_b1
aids_vi_b2
aiml_ii_b1
aiml_ii_b2
aiml_iv_b1
aiml_iv_b2
aiml_vi_b1
aiml_vi_b2
ar_ii_b1
ar_ii_b2
ar_iv_b1
ar_iv_b2
ar_vi_b1
ar_vi_b2
iiot_ii_b1
iiot_ii_b2
iiot_iv_b1
iiot_iv_b2
iiot_vi_b1
iiot_vi_b2
phd

Schema (same for all tables):
- Column `days` stores one of: 'Mo', 'Tu', 'We', 'Th', 'Fr'
- All other columns represent class timings and MUST be backtick-quoted:
  `9.00`, `10.00`, `11.00`, `12.00`, `13.00`, `14.00`, `15.00`, `16.00`

Rules:
- Always generate valid MySQL SQL.
- Always backtick-quote time columns.
- Never invent tables or columns.
- Use WHERE clauses only with valid values.
- Prefer SELECT with specific columns when possible.
- Do not use UPDATE, DELETE, INSERT, DROP.
- Output SQL only. No text.

Example:
User question: "What class does AR II B1 have on Monday at 10?"
Correct SQL:
SELECT `10.00`
FROM ar_ii_b1
WHERE days = 'Mo';

Note: Users may have typo in names of teachers, hence match them with these names-
Tripathi Dr. Deepak, Tyagi Ms. Himani, Singh Dr. Arti, Chand Dr. Mahesh, Lalit Dr. Ruchika, Hooda Dr. Chetana, Joshi Dr. Bhanu Prakash, Bhatia Dr. Anshul, Kumar Mr. Anuj, Singh Dr. Abhishek, Pal Ms. Geetanshi, Tripathi Dr. Atul, Wadhwa Ms. Venika, Kaur Prof. Arvinder, Dr. Annu Priya, Kharwal Ms. Riya, Johari Dr. Rahul, Khurshid Bijli Ms. Mahvish, Kalonia Ms. Ritu, Joshi Dr. Ashish, Mishra Dr. Pawan Kumar, Singh Mr. Neeraj, Jangid Dr. Manisha, Surendra Ms. Surbhi, Chaudhary Ms. Sheetal, AR Guest 1, Aggarwal Dr. Ritu, Chowdhury Dr. Sushobhan, Dr. Jyoti, Shankar Dr. Shashi, Parlewar Dr. Manisha, Kumar Dr. Manoj, Dua Ms. Disha, Choudhary Dr. Amit, Singh Dr. Amrit Pal, Dr. Ashok, Sehgal Dr. Ruchika, Lakhanpal Mr. Anupam, AR Guest 2, Arora Dr. Amar, Nimanpure Dr. Subhas, Rana Dr. Pooja, Singh Dr. Sakshi, Baghel Dr. Pushp Kumar, Anand Dr. Sourabh, Butola Dr. Ravi, Arya Dr. Rajendra, Chaudhary Dr. Sumit, Bhargava Mr. Ankur, Kumar Dr. Ghanendra, Jindal Ms. Kanika, Muthaiah Dr. V. M. Rajavel, Singh Dr. Amanpreet, Singholi Prof. Ajay, Dandapat Dr. Anirban, Mr. Shakin, Singh Dr. Neeta, Singh Dr. Sanjay Kumar, Chopra Dr. Khyati, Aggarwal Prof. Abha, Dalal Dr. Renu, Singh Dr Rohit, Batra Prof. Kriti
"""

template = ChatPromptTemplate.from_messages([
        ('system',system_message),
        ('user',"The question is: {user_query}")]
)

prompt = template.invoke({"user_query":user_query})

sql_query = 