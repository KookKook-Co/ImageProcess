from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
import os.path, io, pickle, ImageProcessing as ip
from matplotlib import pyplot as plt
# import cv2
# from matplotlib import pyplot as plt

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

class Storage:
    def __init__(self):
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('drive', 'v3', credentials=creds)
    
    def downloadImage(self, file_id):
        # param: file id
        # return: numpy array image
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            # print("Download %d%%." % int(status.progress() * 100))
        with open('temp.png', 'wb') as f:
            f.write(fh.getvalue())
        imgList = ip.loadImgs(['temp.png'])
        if os.path.exists('temp.png'):
            os.remove('temp.png')
        return imgList[0]
        

s = Storage()
image = s.downloadImage('13G26jjHpXZRQmBj2drAkKRRAa1OjmGuA')
plt.imshow(image)
plt.title('temp')
plt.show()