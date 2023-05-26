"""Motley Fools Earnings Transcripts Scraping Content and Store to database
21/5/23
"""
import time
import json
import pandas as pd
import sqlite3
from seleniumDriver import driver,WebDriverWait,EC,By
from copy2Gdrive import existingFile_update,service, files2upload, Gfolder_id

dbfolder = './db/'
EarningsTranscriptList = './db/EarningsTranscriptList.csv'
EarningsTranscriptDB = './db/EarningsTranscript.db'

# Scraping Every Link transcript, and use database to store: sqlite3
conn = sqlite3.connect(EarningsTranscriptDB)

def insert_file(Ticker,company,qtr,year,date,link,num_line,num_text,content):
    serialized_content = json.dumps(content)
    conn.execute("INSERT INTO files (Ticker,company,qtr,year,date,link,num_line,num_text,content) VALUES (?,?,?,?,?,?,?,?,?)", (Ticker,company,qtr,year,date,link,num_line,num_text,serialized_content))
    conn.commit()

def get_file(file_id):
    cursor = conn.execute("SELECT content FROM files WHERE id=?", (file_id,))
    result = cursor.fetchone()
    if result:
        file_content = json.loads(result[0])
        return file_content
    else:
        return None

def get_document_count():
    # Call the get_document_count function to retrieve the count
    cursor = conn.execute("SELECT COUNT(*) FROM files")
    result = cursor.fetchone()
    if result:
        document_count = result[0]
        return document_count
    else:
        return 0
    

def main():
    # Call the get_document_count function to retrieve the count
    document_count = get_document_count()
    print("Number of documents:", document_count)

    # Read the downloaded list index
    df_hist = pd.read_csv(EarningsTranscriptList)
    selected_columns = df_hist.columns
    # ['Ticker','qtr','year','link']  # Specify the desired column names

    query = f"SELECT {', '.join(selected_columns)} FROM files"  # Customize the SQL query based on the selected columns
    df_db = pd.read_sql_query(query, conn)
    df_db.rename(columns={'Name':'Company Name', 'Company':'Company Name'}, inplace=True)
    print('Original DB size:', len(df_db))

    # Using set to look for new adds
    zipcol = ['Ticker','qtr','year']
    df_hist_set = set([','.join(df_hist.loc[x,zipcol].values) for x in df_hist.index])
    df_db_set = set([','.join(df_db.loc[x,zipcol].values) for x in df_db.index])

    new_download_df=pd.DataFrame()
    newNames = df_hist_set-df_db_set
    for n in newNames:
        Ticker=n.split(',')[0]
        qtr=n.split(',')[1]
        year=n.split(',')[2]
        new_download_df = pd.concat([new_download_df,df_hist[(df_hist['Ticker']==Ticker)&(df_hist['qtr']==qtr)&(df_hist['year']==year)]])
    
    new_download_df.reset_index(drop=True, inplace=True)

    ### Scrape the content
    if len(new_download_df)>0:
        print(f'Total New names to download: {len(new_download_df)}, {new_download_df["Ticker"].values}')
        for i in range(len(new_download_df)):
            print(f'{i} - Retrieving earnings transcript for: {new_download_df.loc[i,"Ticker"]}')
            url_link = new_download_df.loc[i,'link']
            driver.get(url_link)

            transcript = '/html/body/div[8]/div[2]/div[1]/section[2]/div/div/div[1]/div[1]'
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, transcript)))
            # element = driver.find_element(By.XPATH, transcript)
            
            num_line = len(element.text.split('\n'))
            num_text = len(element.text)
            content = element.text.split('\n')

            Ticker = new_download_df.loc[i, 'Ticker']
            company = new_download_df.loc[i,'Company Name']
            qtr = new_download_df.loc[i, 'qtr']
            year = new_download_df.loc[i, 'year']
            date = new_download_df.loc[i, 'date']
            link = new_download_df.loc[i, 'link']
            
            insert_file(Ticker,company,qtr,year,date,link,num_line,num_text,content)
            time.sleep(3)
        ## Copy to G-drive
        filename = 'EarningsTranscript.db'
        file_id = files2upload[filename][0]
        mime_type = files2upload[filename][1]
        existingFile_update(service, dbfolder+filename, Gfolder_id, mime_type, file_id)
        print('Updated database copied to G-Drive')

    else:
        print('Database is already updated!')
    
    document_count = get_document_count()
    print("Final document count:", document_count)
    print('Process completed')
    conn.close()
    driver.quit()


if __name__=='__main__':
    main()
    