import os
import numpy as np
import camelot
import pandas as pd


def Parse_TT(pdf_path):
    os.makedirs('database/TT_data', exist_ok=True)
    list_dfs = camelot.read_pdf(pdf_path, flavor='lattice', pages='all')

    dfs = []

    for idx in range(len(list_dfs)):
        df = list_dfs[idx].df.copy()  
        # Batch name
        batch_name = str(df.iloc[0, 0]).replace(" ","").replace("-","_")
        df = df.drop(index=0)  
        
        # Replace empty with nan
        df = df.replace(to_replace="", value=np.nan)  
        
        # Get days out
        days = df.iloc[:, 0].copy()  
        for i in range(1, len(days)):
            if pd.isna(days.iloc[i]) or days.iloc[i] == '':
                days.iloc[i] = days.iloc[i-1]
        
        # Make time as column names 
        new_cols = ['days','9_00','10_00','11_00','12_00','13_00','14_00','15_00','16_00'] 
        df.columns = new_cols
        df = df.drop(index=df.index[0])  
        
        # Set days as index
        df.index = days.iloc[1:] 
        df.index.name='days' 
        df = df.drop(columns='days')
        
        # Format the text
        df = df.map(lambda x: x.replace("\n", " ") if isinstance(x, str) else x)
        
        #Add batch_name column
        df['batch']=batch_name

        #append to dfs
        dfs.append(df)
    
    result = pd.concat(dfs,axis=0)
    
    result.to_csv("database/TT_data/tt.csv",index=True)