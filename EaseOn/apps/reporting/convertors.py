import os
from pathlib import Path
import pandas as pd 
import numpy as np 
  
def csv_to_xlsx(file_path):
    df_new = pd.read_csv(file_path)
    path = Path(file_path)
    file_name=path.name.split('.')[0]
    destination = "{}.xlsx".format(os.path.join(path.parent,file_name))
    GFG = pd.ExcelWriter(destination) 
    df_new.to_excel(GFG, index = False) 
    GFG.save() 
    return destination

def csv_to_HTML(file_path):
    df_new = pd.read_csv(file_path)
    path = Path(file_path)
    file_name=path.name.split('.')[0]
    destination = "{}.html".format(os.path.join(path.parent,file_name))
    df_new.to_html(destination)
    return destinationß
