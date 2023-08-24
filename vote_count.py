import requests, json, csv, datetime, os
import pandas as pd, numpy as np


# Read votes file
f = open("votes_only.csv", "r")
lines = f.readlines()
f.close()

votes = {}

# count votes
for line in lines:
  person = line.split("/vote ")[1]
  print(person)
  if person not in votes:
    votes[person] = 0
  votes[person] += 1

pretty = json.dumps(votes, indent=2)
print(pretty)
