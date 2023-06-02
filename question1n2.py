"""Question 1 & 2 Prompts """
import anthropic
import json, sys
import sqlite3
import datetime, time
import pandas as pd
from bs4 import BeautifulSoup
import pprint
pp = pprint.PrettyPrinter(indent=4)

dbfolder = './db/'
EarningsTranscriptList = './db/EarningsTranscriptList.csv'
EarningsTranscriptDB = './db/EarningsTranscript.db'
q1_DB = './db/question1.json'
conn = sqlite3.connect(EarningsTranscriptDB)

#### Anthropic ####
claude_key_kl = json.load(open('../Keys/claude_key_kl.json'))['claude_key_kl']
client = anthropic.Client(api_key=claude_key_kl)
human = json.load(open('./static/prompts.json'))

def get_document_count():
    # Call the get_document_count function to retrieve the count
    cursor = conn.execute("SELECT COUNT(*) FROM files")
    result = cursor.fetchone()
    if result:
        document_count = result[0]
        return document_count
    else:
        return 0
    
document_count = get_document_count()
print("Number of documents:", document_count)

query = f"SELECT * FROM files"  # Customize the SQL query based on the selected columns
df_db = pd.read_sql_query(query, conn)
Q1_DB_hist = json.load(open(q1_DB, 'r'))

def count_tokens(string: str, text=''):
    num_tokens = anthropic.count_tokens(string)
    print(f"{text} number of tokens: {num_tokens}")
    return num_tokens

def get_previous_qtr_date(dateStr):
    # Get previous quarter end date
    mth = int(dateStr[4:6])
    if mth in [9,12]:
        prevQtr = f'{dateStr[:4]}0{str(mth-3)}30'
    elif mth ==6:
        prevQtr = f'{dateStr[:4]}0{str(mth-3)}31'
    else: #mth=3
        prevQtr = f'{str(int(dateStr[:4])-1)}1231'
    prevQtrStr = datetime.datetime.strftime(pd.Timestamp(prevQtr), '%B %d, %Y')
    return prevQtrStr, prevQtr

def promptInstance(files, dateStr, qtrSelect):
    fileDateStr = datetime.datetime.strftime(pd.Timestamp(dateStr), '%B %d, %Y')
    cur_file = files[files['date']==fileDateStr].squeeze()
    print('cur_file',cur_file['date'])
    if qtrSelect=='2':
        # Get previous quarter end date
        prevQtrStr,prevQtr = get_previous_qtr_date(dateStr)
        prev_file = files[files['date']==prevQtrStr].squeeze()
        print('prev_file',prev_file['date'])
        prev_textStr = prev_file['content']
        fileID_prev = cur_file['Ticker']+prevQtr
        # Start Strings
        prev_start_idx = max(prev_textStr.find('Stock Advisor returns as of'),prev_textStr.find('See the 10 stocks'),prev_textStr.find('Prepared Remarks'))
        count_tokens(prev_textStr[prev_start_idx:], 'Previous Qtr')
    else:
        fileID_prev = ''

    company = cur_file['company']
    qtr = cur_file['qtr']
    year = cur_file['year']
    cur_textStr = cur_file['content']
    fileID = cur_file['Ticker']+dateStr

    # Start Strings
    cur_start_idx = max(cur_textStr.find('Stock Advisor returns as of'),cur_textStr.find('See the 10 stocks'),cur_textStr.find('Prepared Remarks'))
    
    # Combining 2 questions - sunsetting this
    # prompt=f"{anthropic.HUMAN_PROMPT} {human['q1a']}{company} for period {fileDateStr} : <current>{cur_textStr[cur_start_idx:]}</current> \
    #         \n\n {human['q1b']} <previous> {prev_textStr[prev_start_idx:] } </previous>. \n\n{human['s1a']} {human['q1c']} {human['q1c2']} \
    #         {human['q1d']} {human['q1e']} {human['q1f']} {human['q1g']} {human['q1h']} {human['q2a']} {human['q2b']} {human['q2c']} {anthropic.AI_PROMPT}"
    
    # Question 1current
    prompt1c=f"{anthropic.HUMAN_PROMPT} {human['q1a']}{company} for period ended {qtr} {year} : <current>{cur_textStr[cur_start_idx:]}</current> \
            \n\n {human['s1b']} \n\n{human['q1c']} {human['q1c2']} {human['q1d']} {human['q1e']} {human['q1f']} {human['q1g']} {human['q1h']} {human['q1h2']}\
            {anthropic.AI_PROMPT}"
    if qtrSelect=='2':
        # Question 1previous
        prompt1p=f"{anthropic.HUMAN_PROMPT} {human['q1b']}{company} : <previous>{prev_textStr[prev_start_idx:]}</previous> \
                \n\n {human['s1b']} \n\n{human['q1c']} {human['q1c2']} {human['q1d']} {human['q1e']} {human['q1f']} {human['q1g']} {human['q1h']} {human['q1h2']}\
                {anthropic.AI_PROMPT}"    
    else: prompt1p=''
    # Question 2 - sunsetting this
    # prompt2=f"{anthropic.HUMAN_PROMPT} {human['s2a']} <previous> {prev_textStr[prev_start_idx:] } </previous>. {human['s2b']} {human['q2a']} \
    #         {human['q2b']} {human['q2c']}  {anthropic.AI_PROMPT}"
    
    # Question 2combined 
    prompt2c=f"{anthropic.HUMAN_PROMPT} {human['s2a2']}{company}. {human['s2b']} {human['q2a']} {human['q2b']} {human['q2c']}  {anthropic.AI_PROMPT}"        
        
    count_tokens(cur_textStr[cur_start_idx:], 'Current Qtr')
    num_tokens = count_tokens(prompt1c+prompt1p+prompt2c, 'prompt Total')
    
    if num_tokens>=100000:
        print('Total number of tokens exceeded the model limit!\nStopping the process now.')
        sys.exit()
        
    return fileID, fileID_prev, prompt1c, prompt1p, prompt2c


def ClaudeAPI(prompt, max_tokens=10000, model="claude-v1.3-100k"):
    # Calling API
    resp = client.completion(
        prompt = prompt,
        stop_sequences = [anthropic.HUMAN_PROMPT],
        model = model,
        max_tokens_to_sample = max_tokens,
    )
    return resp
    
def response_to_db(response1,response2, fileID):
    # response1 - question1
    # response2 - question2
    tags = ['financials','catalyst','qa','rating','overall','title','compfin','change','rate2','reasons']
    
    html = f"""{response1} {response2}"""
    soup = BeautifulSoup(html, 'html.parser')

    tagsDict={}
    for t in tags:
        if soup.find(t) is not None:
            tagsDict[t] = soup.find(t).text.strip()
        
    if fileID not in Q1_DB_hist.keys():
        Q1_DB_hist[fileID] = tagsDict
    else:
        addPairs = [x for x in tagsDict.keys() if x not in Q1_DB_hist[fileID].keys()]
        for k in addPairs:
            Q1_DB_hist[fileID][k] = tagsDict[k]

    pp.pprint(Q1_DB_hist[fileID])
    ### Save to json db
    with open(q1_DB, 'w') as f:
        json.dump(Q1_DB_hist, f)
        print('Records save to: ', q1_DB)

    return Q1_DB_hist[fileID]

######## INPUT ###########
def input_module():
    ticker = input('Enter the Ticker: ').upper()
    qtrSelect = input('Enter <1> or <2> quarters (2:current & previous) to run, <Enter> for default 2: ')
    if qtrSelect=='':
        qtrSelect='2'
    dateStr = input('Enter the requested quarter end date in <YYYYmmdd> format, <Enter> for default 20230331: ')
    if dateStr=='':
        dateStr='20230331'
    print('Available Models: "claude-v1.3-100k", "claude-v1-100k", "claude-instant-v1-100k"')
    modelSelect = "claude-v1.3-100k"

    return ticker,dateStr,qtrSelect,modelSelect

def main(ticker,dateStr,qtrSelect,modelSelect):
    files = df_db[(df_db['Ticker']==ticker)]
    print(files)
    fileID,fileID_prev,prompt1c,prompt1p,prompt2c = promptInstance(files,dateStr,qtrSelect)

    print(f'Running on model: {modelSelect}')
    # Run the stated quarter first
    start_time = time.time()
    resp_1c = ClaudeAPI(prompt1c, 10000, modelSelect)['completion']
    time1 = time.time()
    print(f'Elapsed time for Claude: {(time1-start_time):.2f} seconds')

    if qtrSelect=='1':
        resp_ques2=''
        resp2json = response_to_db(resp_1c,resp_ques2, fileID)
        print(f'Claude response saved for: {fileID}')

    elif qtrSelect=='2':
        # Check if Claude had already analysed previous quarter 
        if fileID_prev in Q1_DB_hist.keys():
            resp_1p = Q1_DB_hist[fileID_prev]
            print('Previous qtr output from Claude already existed, proceed to compare')
        else:
            # No previous saved Claude response
            start_time = time.time()
            resp_1p = ClaudeAPI(prompt1p, 10000, modelSelect)['completion']
            time1 = time.time()
            print(f'Elapsed time for Claude: {(time1-start_time):.2f} seconds')
            # Save previous quarter
            resp_ques2=''
            resp2json = response_to_db(resp_1p,resp_ques2, fileID_prev)
            print(f'Claude response saved for: {fileID_prev}')

        # Taking an API break
        time.sleep(10)
        # Combining previous and current to compare
        print('Running next question ...')
        comboPrompt = prompt1c+resp_1c+prompt1p+resp_1p+prompt2c
        count_tokens(comboPrompt)
        start_time = time.time()
        resp_combo = ClaudeAPI(comboPrompt, 10000, modelSelect)['completion']
        time1 = time.time()
        print(f'Elapsed time for Claude: {(time1-start_time):.2f} seconds')
        resp2json = response_to_db(resp_1c,resp_combo, fileID)

        print(f'Completed for {ticker} on the 2 questions')

if __name__=='__main__':
    ticker,dateStr,qtrSelect,modelSelect = input_module()
    main(ticker,dateStr,qtrSelect,modelSelect)