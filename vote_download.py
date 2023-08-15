import requests, json, csv, datetime, os
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

# Read when the last recorded message was
starting_message_time = 0
if os.path.isfile("last_message_time.txt"):
  f = open("last_message_time.txt", "r")
  starting_message_time = int(f.read())
  f.close()

print("Filtering data to only messages newer than " + datetime.datetime.fromtimestamp(starting_message_time).isoformat())

# parse data into flat dictionary
new_msg_count = 0
for i in data:
  if "message" not in i.keys():
    pass
  else:
    if (i["message"]["date"] <= starting_message_time):
      continue
    new_msg_count += 1
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
      if "/vote" in i["message"]["text"]:
        vote = True
      data_dict["text"].append(i["message"]["text"])
      data_dict["vote"].append(vote)
    else:
      data_dict["text"].append("")
      data_dict["vote"].append(vote)

if not data_dict["date"]:
  print("no new data found")
  quit()

# write new data to CSV
df = pd.DataFrame.from_dict(data_dict)

now = datetime.datetime.today()

date_format = "{y}-{m}-{d}T{H}:{M}:{S}".format(
    y = now.year,
    m = now.month,
    d = now.day,
    H = now.hour,
    M = now.minute,
    S = now.second)

csv_filename = "votes-{}.csv".format(date_format)
df.to_csv(csv_filename)

print("Wrote " + str(new_msg_count) + " new message to " + csv_filename)

# Update recorded timestamp of last observed message
last_message_time = data_dict["date"][-1]

f = open("last_message_time.txt", "w")
f.write(str(last_message_time))
f.close()

print("Recorded " + datetime.datetime.fromtimestamp(last_message_time).isoformat() + " as last message time")

