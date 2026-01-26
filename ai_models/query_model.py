from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate 
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
import os 
from datetime import datetime,date

#Load env variables
load_dotenv()


current_date = date.today().strftime("%A, %d-%m-%Y")
current_time = datetime.now().strftime("%H:%M")

#Prompt template
query_sys_message = """
You are an expert MySQL query generator for USAR (University School of Automation and Robotics) timetable system.

TASK:
Convert a natural-language question into valid MySQL SELECT query/queries.
The queries you generate will be used to retrieve information about classes, teachers, timing etc. from the database. Try to get all the data the user might want through the question

Todays day and date(day-month-year): {current_date}
Current time: {current_time}

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

For timings of class check the column names,
For days check the 'days' column or index`

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


def get_query(user_query, max_retries=3):
    query_model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2
    )

    query_template = ChatPromptTemplate.from_messages([
        ("system", query_sys_message),
        ("human", "{user_query}")
    ])

    error_msg = ""
    for attempt in range(max_retries):
        # Include error from previous attempt
        current_query = user_query
        if error_msg:
            current_query = f"{user_query}\n\nPrevious query failed with error: {error_msg}\nPlease generate a corrected query."
        
        prompt = query_template.invoke(
            {"current_date":current_date,"current_time":current_time,"user_query": current_query})
        response = query_model.invoke(prompt)
        sql_query = response.content.strip()
        
        # Remove markdown code blocks if present
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

        result = check_query(sql_query)

        if not isinstance(result, str):  # success
            return result
        else:
            error_msg = result

    raise RuntimeError(f"Failed to generate valid SQL query after {max_retries} retries. Last error: {error_msg}")


def check_query(generated_query):
    # Basic SQL injection protection
    dangerous_keywords = ['DROP', 'DELETE', 'INSERT', 'UPDATE', 'ALTER', 'CREATE', 'TRUNCATE']
    query_upper = generated_query.upper()
    
    for keyword in dangerous_keywords:
        if keyword in query_upper:
            raise ValueError(f"Dangerous SQL keyword detected: {keyword}")
    
    password = os.getenv("PASSWORD")
    engine = create_engine(
        f"mysql+mysqlconnector://root:{password}@localhost/timetable"
    )

    try:
        return pd.read_sql(sql=generated_query, con=engine)
    except Exception as error:
        return str(error)