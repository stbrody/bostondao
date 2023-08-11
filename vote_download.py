import requests, json, csv, datetime
import pandas as pd, numpy as np

# Call query
url = "https://api.telegram.org/bot6049950094:AAHAd2wke2a5HLzWAWZZMQ7SFYY-U7kx_z4/getUpdates"
r = requests.get(url = url)
data = r.json()
data = data["result"]
#print(data)

# Setup empty dictionary
data_dict = {
    "update_id":[],
    "message_id":[],
    "from_id":[],
    "first_name":[],
    "last_name":[],
    "username":[],
    "date":[],
    "text":[],
    "vote":[]
}

# parse data into flat dictionary
for i in data:
  if "message" not in i.keys():
    pass
  else:
    vote = False
    data_dict["update_id"].append(i["update_id"])
    data_dict["message_id"].append(i["message"]["message_id"])
    data_dict["from_id"].append(i["message"]["from"]["id"])
    data_dict["first_name"].append(i["message"]["from"]["first_name"])
    if "last_name" in i["message"]["from"].keys():
      data_dict["last_name"].append(i["message"]["from"]["last_name"])
    else:
      data_dict["last_name"].append("")
    if "username" not in i["message"]["from"].keys():
      data_dict["username"].append("")
    else:
      data_dict["username"].append(i["message"]["from"]["username"])
    data_dict["date"].append(i["message"]["date"])
    # handle error for when photos are sent and there is no "text" param
    if "text" in list(i["message"].keys()):
      if "/nominate" in i["message"]["text"]:
        vote = True
      data_dict["text"].append(i["message"]["text"])
      data_dict["vote"].append(vote)
    else:
      data_dict["text"].append("")
      data_dict["vote"].append(vote)

df = pd.DataFrame.from_dict(data_dict)

dt = "{y}-{m}-{d} {H}:{M}".format(
    y = datetime.datetime.today().year,
    m = datetime.datetime.today().month,
    d = datetime.datetime.today().day,
    H = datetime.datetime.today().hour,
    M = datetime.datetime.today().minute)

df.to_csv("nominations {}.csv".format(dt))

