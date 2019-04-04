import json
from elasticsearch import Elasticsearch, helpers


def build_dataset(dataset_filepath):

    data = json.load(open(dataset_filepath))
    
    video = data["meta"]["title"]
    video_id = data["meta"]["broadcast_id"]
    
    comments = []

    for comment in data["comments"]:

        id_ = comment["_id"]

        text = comment["message"]["body"]
        timestamp = comment["created_at"]
        
        user = comment["commenter"]["display_name"]
        user_id = comment["commenter"]["_id"]
        
        is_action = comment["message"]["is_action"]
        source = comment["source"]
        state = comment["state"]
        
        badges = []
        emotes = []

        emotes = [ x["text"] for x in comment["message"]["fragments"] if "emoticon" in x ]

        if "user_badges" in comment["message"]:
            badges = [ x["_id"] for x in comment["message"]["user_badges"] ]

        comments.append({
            "id": id_,
            "user": user,
            "user_id": user_id,
            "video": video,
            "video_id": video_id,
            "text": text,
            "timestamp": timestamp,
            "emotes": emotes,
            "badges": badges,
            "is_action": is_action,
            "state": state,
            "source": source
        })

    return comments


INDEX = "twitch_chatlogs"
DOC_TYPE = "message"

def ingest(dataset_filepaths, es_server, reset=False):

    es = Elasticsearch(es_server)


    if reset:
        if es.indices.exists(index=INDEX):
            es.indices.delete(index=INDEX)

    if not es.indices.exists(index=INDEX):
        es.indices.create(index=INDEX)
 

    docs = []

    for dataset_filepath in dataset_filepaths:
        print(dataset_filepath)
        comments = build_dataset(dataset_filepath)

        for comment in comments:
            docs.append({
                "_index": INDEX,
                "_type": DOC_TYPE,
                "_id": comment["id"],
                "_source": comment
            })

        helpers.bulk(es, docs)

        

