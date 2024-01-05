################################################
#
# https://www.youtube.com/watch?v=vQQEaSnQ_bs
#
################################################


import os
import pickle
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


credentials = None

# token.pickle stores the user's credentials from previously successful logins
if os.path.exists('token.pickle'):
    print('Loading Credentials From File...')
    with open('token.pickle', 'rb') as token:
        credentials = pickle.load(token)

# If there are no valid credentials available, then either refresh the token or log in.
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print('Refreshing Access Token...')
        credentials.refresh(Request())
    else:
        print('Fetching New Tokens...')
        flow = InstalledAppFlow.from_client_secrets_file('./client_secret.json',
            scopes=['https://www.googleapis.com/auth/youtube.readonly'])
        # https://www.googleapis.com/auth/youtube -> administra cuenta
        # https://www.googleapis.com/auth/youtube.readonly -> permite ver la cuenta
        flow.run_local_server(port=8090, prompt='consent')
        credentials = flow.credentials

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as f:
            print('Saving Credentials for Future Use...')
            pickle.dump(credentials, f)


print(credentials.to_json())

youtube = build ("youtube", "v3", credentials = credentials)
# request = youtube.channels().list(part = "contentDetails", forUsername="dekkard79")
# request = youtube.playlistItems().list(part="status, contentDetails", playlistId ="PL3ZjZ6QcaRe9dBEnTTXcP2SOBorxwBObN", maxResults=50)
# request = youtube.channels().list(part="contentDetails", mine = True,  maxResults=50)
# response = request.execute()  

#using nextToken to get pages
playlist_items = []
next_page_token = None

while True:
    request = youtube.playlistItems().list(
        part='snippet, contentDetails',
        playlistId="PL3ZjZ6QcaRe9dBEnTTXcP2SOBorxwBObN",
        maxResults=50,  # Maximum number of results per page (you can adjust this)
        pageToken=next_page_token if next_page_token else ''
    )
    response = request.execute()
    playlist_items.extend(response['items'])
    next_page_token = response.get('nextPageToken')

    if not next_page_token:
        break


# print(response)
# playlist_id de mis subidas: UU5VFigY67iOXHxtnaspn2Rg

list_of_videos = []

for item in playlist_items:
    channel = item["snippet"]["videoOwnerChannelTitle"]
    video_title = item["snippet"]["title"]
    video_id = item["contentDetails"]["videoId"]
    link = f"https://youtu.be/{video_id}"
    # print(f"Title: {playlist_title} | Id: {playlist_id}")
    list_of_videos.append({"channel": channel, "video_title": video_title, "video_id":video_id, "link": link})
    
print(f"Total of {len(playlist_items)} items")
df = pd.DataFrame(list_of_videos)
print(df)
df.to_csv('data.csv', index=False)


