from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
import os
from parse_db import Parse_TT

#Parsing pdf to get timetable csv file for each batch
Parse_TT(r"TT_Batchwise_Even SEM-2025-26.pdf")


#load env
load_dotenv()
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
csv_dir = "database/TT_data"


# use engine to do the CRUD operations
db = create_engine(
    url=f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)


for file in os.listdir(csv_dir):
    file_name = "tt"
    csv_path = os.path.join(csv_dir, file)

    df = pd.read_csv(csv_path)

    df.to_sql(
        name= file_name,
        con=db,
        if_exists="replace",
        index=True
    )
    print(f"Inserted {file_name}")