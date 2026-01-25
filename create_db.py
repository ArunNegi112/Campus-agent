import mysql.connector
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
import os
from parse_tt import Parse_TT

#Parsing pdf to get timetable csv file for each batch
Parse_TT(r"C:\Users\Arun\Documents\Documents\Campus chatbot\TT_Batchwise_Even SEM-2025-26.pdf")


#load env
load_dotenv()
db_password = os.getenv("PASSWORD")
#build connection
csv_dir = "TT_data"


#Create database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=db_password
)

cur = conn.cursor()
cur.execute(operation="CREATE DATABASE IF NOT EXISTS timetable")
conn.commit()
cur.close()
conn.close()


# so i used connector only to create database and then will use engine to actually do the CRUD operations
db = create_engine(
    url=f"mysql+mysqlconnector://root:{db_password}@localhost/timetable"
)


for file in os.listdir(csv_dir):
    file_name = str(file).split(".")[0]
    csv_path = os.path.join(csv_dir, file)

    df = pd.read_csv(csv_path)

    df.to_sql(
        name= file_name,
        con=db,
        if_exists="replace",
        index=True
    )
    print(f"Inserted {file_name}")



