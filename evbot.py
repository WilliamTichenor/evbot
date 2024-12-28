import math
import os
import re
import random
import discord
from dotenv import load_dotenv

# data = [docs = [original, BOW, length], totalBOW = {BOW}]
def loadDocs():
    data = [[]]
    file = open("ParkourCivilizationTranscript.txt", "r", encoding='utf-8')
    totalbow = {}
    for s in file.read().split("\n"):
        if not s:
            continue
        doc = []
        if (s and (s[0] == '"' or s[0] == '“' or s[0] == '“')):
            s = s.strip('”')
            s = s.strip('“')
            s = s.strip('"')
        s = s.replace('-',' ')
        s = s.replace('—',' ')
        doc.append(s)
        s = s.lower()
        s = re.sub(r'[^a-z0-9\s]', '', s)
        bow = {}
        for w in s.split():
            if w in bow:
                bow[w] += 1
            else: 
                bow[w] = 1
        for key in list(bow.keys()):
            if w in totalbow:
                totalbow[w] += 1
            else: 
                totalbow[w] = 1
        doc.append(bow)
        doc.append(len(s.split()))
        data[0].append(doc)
    data.append(totalbow)
    return data

def convertBOW(s):
    # bow = [{BOW}, len]
    bowlen = 0
    s = s.lower()
    s = s.replace('-',' ')
    s = s.replace('/',' ')
    s = s.replace('+',' ')
    s = re.sub(r'[^a-z0-9\s]', '', s)
    bow = {}
    for w in s.split():
        bowlen += 1
        if w in bow:
            bow[w] += 1
        else: 
            bow[w] = 1
    return [bow, bowlen]


if __name__ == "__main__":

    random.seed()
    data = loadDocs()
    #print(data)
    numdocs = len(data[0])
    avgdl = sum(x[2] for x in data[0])/numdocs
    print(avgdl)
    k1 = 1.3
    b = .75

    load_dotenv("secrets.env")
    TOKEN = os.getenv('DISCORD_TOKEN')

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        print(message.content)
        querybow = convertBOW(message.content)
        #print(querybow)

        scores = {}
        for doc in data[0]:
            score = 0
            for w in list(querybow[0].keys()):
                for i in range(0,querybow[0][w]): # run the query word for the number of times it appears!
                    #calculate iteration of BM25 score
                    nqi = data[1][w] if w in data[1] else 0
                    idf = math.log(((numdocs-nqi+.5) / (nqi+.5)) + 1)
                    tf = doc[1][w] if w in doc[1] else 0
                    score += (idf * tf * (k1+1) / (tf + k1 * (1 - b + (b * doc[2] / avgdl))))
            if querybow[1]<=5:
                factor = (1/20)*querybow[1]+0.8
            else:
                factor = 20/(querybow[1]+16)
            scores[doc[0]] = (random.random()/2.5+0.8) * score * factor
        scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
        print(dict(list(scores.items())[0]))

        if len(scores) > 0 and scores[list(scores)[0]] > (random.random()/2+0.75) * 24.0:
            await message.channel.send(list(scores)[0])


    client.run(TOKEN)