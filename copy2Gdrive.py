"""Copy to Gdrive"""

import os, io, csv, json
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from apiclient import errors
from requests.models import HTTPError

fileID = json.load(open('./static/fileID.json'))

gDrive_API = './key/gdrive_hackathon.json'
dbfolder = './db/'

files2upload = {'EarningsTranscriptList.csv': [fileID["ET_list"], 'text/csv'],
                'EarningsTranscript.db': [fileID["ET_db"], 'application/x-sqlite3'] }
Gfolder_id = fileID["Gfolder"]

"""Getting Google Drive Credential and get the service module running"""
SCOPES = [
    'https://www.googleapis.com/auth/drive']  # full access here if used without .file

global SERVICE_ACCOUNT_FILE, service
SERVICE_ACCOUNT_FILE = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
API_NAME = 'drive'
API_VERSION = 'v3'

if SERVICE_ACCOUNT_FILE == None:
    print('SERVICE_ACCOUNT_FILE is NONE, look into local...')
    try:
        SERVICE_ACCOUNT_FILE = gDrive_API
    except:
        print('Error in retrieving Google Authentication file')
        os.abort()

# project name
gcp_project = os.environ.get('GCP_PROJECT')

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

##################################################################################################
def existingFile_update(service, filename, Gfolder_id, mime_type, file_id):
    """Uploading to GDrive via 'update' command - processed data in memory
        - Just updating the existing pbz2 file
        - omit updating file_metadata[body] (difficult to modify), just updating contents[media_body]"""
    try:
        # file_metadata = {
        #     'name' : file_name,
        #     'parents' : [Gfolder_id]
        # }
        media = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
        service.files().update(
            # body=file_metadata,
            fileId=file_id,
            media_body=media,
            # fields='id'
        ).execute()
        print('Done! Successfully uploaded to Google Drive:', Gfolder_id+'/'+file_id)
    except errors.HttpError as error:
        print('update error to Google Drive')
        print(error)


def download_csv_Files(file_id, service, index='drop'):
    """Downloading .csv Files"""
    print('download_csv_file index:', index)
    request = service.files().get_media(fileId=file_id)
    stream = io.BytesIO()
    downloader = MediaIoBaseDownload(stream, request)
    done = False
    # Retry if we received HttpError
    for retry in range(0, 5):
        try:
            while done is False:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))

            decoded_content = stream.getvalue().decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            if index == 'drop':
                print('Dropping the first index row')
                # Dropping the first row, not index column!
                df = pd.DataFrame(my_list, columns=my_list[0]).drop(index=0)
            else:  df = pd.DataFrame(my_list, columns=my_list[0])
            return df

        except HTTPError as error:
            print('There was an API error: {}. Try # {} failed.'.format(
                error.response, retry))


def download_bytes_Files(file_id, service):
    """Download and return io.BytesIO Files"""
    request = service.files().get_media(fileId=file_id)
    stream = io.BytesIO()
    downloader = MediaIoBaseDownload(stream, request)
    done = False
    # Retry if we received HttpError
    for retry in range(0, 5):
        try:
            while done is False:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))
            return stream.getvalue()

        except HTTPError as error:
            print('There was an API error: {}. Try # {} failed.'.format(
                error.response, retry))
            return None


if __name__=='__main__':
    for k,v in files2upload.items():
        print(k,v)
        filename = dbfolder+k
        file_id = v[0]
        mime_type =  v[1]
        existingFile_update(service, filename, Gfolder_id, mime_type, file_id)
