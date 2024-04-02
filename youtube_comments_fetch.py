import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd

def fetch_comments(video_id, developer_key):
    comments = []
    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=developer_key)

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100
    )

    while request is not None:
        try:
            response = request.execute()
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                public = item['snippet']['isPublic']
                comments.append([
                    comment['authorDisplayName'],
                    comment['publishedAt'],
                    comment['likeCount'],
                    comment['textOriginal'],
                    public
                ])
            request = youtube.commentThreads().list_next(request, response)
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
            break

    return comments

def main():
    video_id = "XPcfJ48h3yA"
    developer_key = "AIzaSyB9xuZlVvkEWV8aKvPeE_hzx31MhPKbJPQ"
    comments = fetch_comments(video_id, developer_key)

    df = pd.DataFrame(comments, columns=['author', 'updated_at', 'like_count', 'text', 'public'])
    print(df.info())

if __name__ == "__main__":
    main()
