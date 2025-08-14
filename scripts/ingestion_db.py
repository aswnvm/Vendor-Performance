import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

logging.basicConfig(
    filename = "./assets/logs/ingestion_db.log",
    level = logging.DEBUG,
    format = "%(asctime)s - %(levelname)s - %(message)s",
    filemode = "a"
)

engine = create_engine('sqlite:///inventory.db')

def ingest_db(df, table_name, engine):
    '''This function ingests dataframe into db tables'''
    df.to_sql(table_name, con=engine, if_exists = 'replace', index = False)
    
def load_raw_data():
    '''This function loads the CSVs as dataframe and ingests into db'''
    start_time = time.time()
    for file in os.listdir('./assets/data'):
        if '.csv' in file:
            df = pd.read_csv('./assets/data/'+file)
            logging.info(f'Ingesting {file} in db')
            ingest_db(df, file[:-4], engine)
    end_time = time.time()
    total_time =  (end_time - start_time)/60
    logging.info("--------Ingestion Complete----------")
    logging.info(f"\nTotal Time Taken: {total_time} minutes")
    
if __name__ == '__main__':
    load_raw_data()