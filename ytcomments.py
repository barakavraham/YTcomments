import requests
import json

YOUTUBE_DATA_API_KEY = "Enter your API KEY here"
YOUTUBE_VIDEO_ID = input("Enter video ID: ")
AUTHOR_NAME = input("Enter username: ")
COMMENTS_THREADS_API_LINK = f'https://www.googleapis.com/youtube/v3/commentThreads?key={YOUTUBE_DATA_API_KEY}&textFormat=plainText&part=snippet&videoId={YOUTUBE_VIDEO_ID}&maxResults=100'
comments = requests.get(COMMENTS_THREADS_API_LINK)
comments = json.loads(comments.text)
author_comments = []
all_comments_counter = 0

print("Loading comments...")
while(True):
    for comment in comments["items"]:
        all_comments_counter += 1
        author_comment = comment["snippet"]["topLevelComment"]["snippet"]
        if author_comment["authorDisplayName"] == AUTHOR_NAME:
            author_comments.append(f'{author_comment["authorDisplayName"]}: \n\n{author_comment["textDisplay"]}')
        if comment["snippet"]["totalReplyCount"] != 0:
            REPLIES_API_LINK = f'https://www.googleapis.com/youtube/v3/comments?part=snippet&parentId={comment["id"]}&key={YOUTUBE_DATA_API_KEY}'
            replies = json.loads(requests.get(REPLIES_API_LINK).text)
            for reply in replies["items"]:
                all_comments_counter += 1
                if reply["snippet"]["authorDisplayName"] == AUTHOR_NAME:
                    author_comments.append(f'{reply["snippet"]["authorDisplayName"]}: \n\n{reply["snippet"]["textDisplay"]}')
    print(f'{all_comments_counter} comments as been checked...')
    try:
        nextPageToken = comments["nextPageToken"]
        COMMENTS_THREADS_API_LINK = f'https://www.googleapis.com/youtube/v3/commentThreads?key={YOUTUBE_DATA_API_KEY}&textFormat=plainText&part=snippet&videoId={YOUTUBE_VIDEO_ID}&maxResults=100&pageToken={nextPageToken}'
        comments = json.loads(requests.get(COMMENTS_THREADS_API_LINK).text)
    except:
        break
for comment in author_comments:
    f = open(f'{AUTHOR_NAME} - {YOUTUBE_VIDEO_ID}.txt', "a")
    f.write('----------------------------------------------------------------------------------------\n')
    f.write(comment + "\n")
    f.close()
