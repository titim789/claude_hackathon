"""Motley Fools Earnings Transcripts Scraping - Selected company 
select X years of history
Note: This is just to extract the links - not downloading the contents
24/5/23
"""
import time
import pandas as pd
import requests, sys
from helper.seleniumDriver import driver,By
from helper.copy2Gdrive import existingFile_update,service, files2upload, Gfolder_id

EarningsTranscriptList = './db/EarningsTranscriptList.csv'
loadMore = '//*[@id="quote-earnings-transcripts"]/button'

def get_company_historical_transcripts(ticker, pagesLoad = 1):
    # pagesLoad: Select number of pages to 'Load More', keep minimmun 1
    ticker = ticker.upper()

    ## Start testing NYSE exchange first
    exch = 'nyse'
    url = f'https://www.fool.com/quote/{exch}/{ticker}/#quote-earnings-transcripts'
    if requests.get(url).ok:
        pass
    else: exch = 'nasdaq'
    print('Exchange is:',exch)
    url = f'https://www.fool.com/quote/{exch}/{ticker}/#quote-earnings-transcripts'

    driver.get(url)
        
    for i in range(pagesLoad):
        click = driver.find_element(By.XPATH, loadMore)    
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", click)
        time.sleep(2)
        click.click()
        time.sleep(2)
        
    result_df = pd.DataFrame([], columns=['Ticker','Company Name','qtr','year','date','link','publish_date'])

    idXpath = '//*[@id="earnings-transcript-container"]//a'
    container = driver.find_elements(By.XPATH, idXpath)
    elements = [(c.text,c.get_attribute('href')) for c in container]
    for e in enumerate(elements):
        name = e[1][0].split('(')[0].rstrip()
        qtr  = e[1][0].split(')')[1].lstrip()[:2]
        year = e[1][0].split(')')[1].lstrip()[3:7]
        date = ' '.join(e[1][0].splitlines()[1].split()[-3:]).rstrip('.')
        link = e[1][1]
        pubDate = pd.Timestamp(e[1][1][47:57]).date()
        # name, qtr, year,date
        result_df = pd.concat([result_df,
                            pd.DataFrame({'Ticker':ticker,'Company Name':name,'qtr':qtr,'year':year,'date':date,'link':link,'publish_date':pubDate}, index=[e[0]])])
    
    df = pd.read_csv(EarningsTranscriptList)
    df = pd.concat([result_df, df])
    df.drop_duplicates(keep='first', inplace=True, ignore_index=True)
    df.to_csv(EarningsTranscriptList, index=False)
    filename = 'EarningsTranscriptList.csv'
    file_id = files2upload[filename][0]
    mime_type = files2upload[filename][1]
    existingFile_update(service, EarningsTranscriptList, Gfolder_id, mime_type, file_id)
    print('Updated list copied to G-Drive')    
    # driver.quit()

    # Returning the newly downloaded list to scrape content
    return result_df

if __name__=='__main__':
    cont=True
    ticker = input('Enter the ticker to scrape:').upper()
    while cont:
        result_df = get_company_historical_transcripts(ticker)
        ticker = input('Enter the ticker to continue to scrape, or <Enter> to end: ')
        if ticker=='':
            cont = False
            driver.quit()

