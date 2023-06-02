"""Motley Fools Earnings Transcripts Scraping 
15/5/23
"""
import time
import pandas as pd
from helper.seleniumDriver import driver,WebDriverWait,EC,By
from helper.copy2Gdrive import existingFile_update,service, files2upload, Gfolder_id

########################
# Select number of pages to 'Load More', keep minimmun 1
pagesLoad = 1
#######################

EarningsTranscriptList = './db/EarningsTranscriptList.csv'

url = 'https://www.fool.com/earnings-call-transcripts/'
loadMore = '/html/body/div[8]/div[2]/div[1]/section[2]/div/div/div[1]/div/div/button'

def scrape_earningsList():
    driver.get(url)
    wait = WebDriverWait(driver, 2)

    ### Run to click 'Load More' 10x ###
    for i in range(pagesLoad):
        # element = driver.find_element(By.XPATH, loadMore)    
        element= wait.until(EC.element_to_be_clickable((By.XPATH, loadMore)))#.get_attribute("href")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element)
        time.sleep(2)
        element.click()
        time.sleep(2)

    # Get all the link addresses after clicking x times
    # Find <a> tags
    css_selector = 'a'
    linkList = driver.find_elements(By.CSS_SELECTOR, css_selector)
    # VOXX International Corporation (VOXX) Q4 2023 Earnings Call Transcript
    # VOXX earnings call for the period ending March 31, 2023.

    # Download the historical file and concat
    df = pd.read_csv(EarningsTranscriptList)
    df['publish_date'] = pd.to_datetime(df['publish_date']).apply(lambda x: x.date())
    original_df_length = len(df)
    print('Length of historical records:',original_df_length)
    columnNames=['Ticker','Company Name','qtr','year','date','link','publish_date']
    for i in linkList:
        if 'Earnings Call Transcript' in i.text:
            lines = i.text.splitlines()
            line0 = lines[0].split()
            tickerIndex = [line0.index(x) for x in line0 if '(' in x][0]
            companyName = ' '.join(line0[:tickerIndex])
            periodQ = line0[tickerIndex+1]
            periodY = line0[tickerIndex+2]

            line1 = lines[1].split()
            ticker = line1[0]
            date = ' '.join(line1[-3:]).replace('.','')
            href = i.get_attribute("href")
            publish_date = pd.Timestamp(str(href)[47:57]).date()

            df = pd.concat([pd.DataFrame([ticker,companyName,periodQ,periodY,date,href,publish_date],index=columnNames).T, df])

    print('Total number of links:', len(linkList))
    df.drop_duplicates(keep='first', inplace=True, ignore_index=True)
    df.sort_values(by='publish_date', ascending=False, inplace=True)
    newLength = len(df)
    print('New Length:',newLength)

    if original_df_length == newLength:
        print('List is updated!')
    else:
        print('Updating list and save...')
        df.to_csv(EarningsTranscriptList, index=False)
    filename = 'EarningsTranscriptList.csv'
    # Create mirror image to G-Drive
    file_id = files2upload[filename][0]
    mime_type = files2upload[filename][1]
    existingFile_update(service, EarningsTranscriptList, Gfolder_id, mime_type, file_id)
    print('Updated list copied to G-Drive')
    driver.quit()
    print('Completed scrapeList')
    return df

if __name__=='__main__':
    df = scrape_earningsList()
