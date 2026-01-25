import os
import numpy as np
import camelot
import pandas as pd

def Parse_TT(pdf_path):
    os.makedirs('TT_data', exist_ok=True)
    list_dfs = camelot.read_pdf(pdf_path, flavor='lattice', pages='all')
    batch_names = []
    
    for idx in range(len(list_dfs)):
        df = list_dfs[idx].df.copy()  
        
        # Batch name
        batch_name = str(df.iloc[0, 0]).replace(" ","").replace("-","_")
        batch_names.append(batch_name)
        df = df.drop(index=0)  
        
        # Replace empty with nan
        df = df.replace(to_replace="", value=np.nan)  
        
        # Get days out
        days = df.iloc[:, 0].copy()  
        for i in range(1, len(days)):
            if pd.isna(days.iloc[i]) or days.iloc[i] == '':
                days.iloc[i] = days.iloc[i-1]
        
        # Make time as column names 
        new_cols = ['days'] + df.iloc[0, 1:].tolist()
        df.columns = new_cols
        df = df.drop(index=df.index[0])  
        
        # Set days as index
        df.index = days.iloc[1:] 
        df.index.name='days' 
        df = df.drop(columns='days')
        
        # Format the text
        df = df.map(lambda x: x.replace("\n", " ") if isinstance(x, str) else x)
        
        # Save as csv file
        file_name = f"TT_data/{batch_name.lower()}.csv"
        df.to_csv(file_name, index=True)

        print("Created: ", file_name)
    