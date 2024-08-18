import praw
import json
import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

app = FastAPI()

TOPICS = [  # Default Topics When No Topic is given!!
    "dankmemes",
    "memes",
    "AdviceAnimals",
    "MemeEconomy",
    "me_irl",
    "ComedyCemetery",
    "terriblefacebookmemes"
]

def fetch_reddit_data():
    reddit = praw.Reddit(
        client_id="B674hEW9kRJUoyALVlWNBg",
        client_secret="O9C1Y23gKFUnhmqdoZj74gSfsZJeMQ",
        user_agent="trending-meme",
    )
    # count=1
    data = []
    for subreddit in TOPICS:
        posts = reddit.subreddit(subreddit).hot(limit=5)
        # print(count)
        for post in posts:
            author=post.author.name if post.author else "[deleted]"
            post_data = {
                "groupName": "r/"+subreddit,
                "groupLink": "https://www.reddit.com/r/"+subreddit,
                "caption": post.title,
                "image": post.url,
                "likes": post.score,
                "comments":post.num_comments,
                "created": datetime.datetime.fromtimestamp(post.created).isoformat(),
                "id": post.id,
                "creator": author,
                "creatorLink":"https://www.reddit.com/user/"+author,
                "creatorImage": post.author.icon_img if post.author else None
            }
            data.append(post_data)
        # count=count+1

    return data

def update_json_file(data, filename="reddit_data.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

@app.get("/")
def main_root():
    reddit_data = fetch_reddit_data()
    # update_json_file(reddit_data)
    # data = json.dump(data, indent=2)
    return {"message": "JSON file updated successfully.","data":reddit_data}

@app.get("/reddit-data")
def read_reddit_data():
    filename = "reddit_data.json"
    if os.path.exists(filename):
        return FileResponse(filename, media_type="application/json")
    else:
        raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
