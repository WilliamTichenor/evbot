import math
import os
import re
import discord
from dotenv import load_dotenv

# data = [docs = [original, BOW, length], totalBOW = {BOW}]
def loadDocs():
    data = [[]]
    file = open("ParkourCivilizationTranscript.txt", "r", encoding='utf-8')
    totalbow = {}
    for s in file.read().split("\n"):
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
            if w in bow:
                totalbow[w] += 1
            else: 
                totalbow[w] = 1
        doc.append(bow)
        doc.append(len(s.split()))
        data[0].append(doc)
    data.append(totalbow)
    return data

def convertBOW(s):
    s = s.lower()
    s = s.replace('-',' ')
    s = s.replace('/',' ')
    s = s.replace('+',' ')
    s = re.sub(r'[^a-z0-9\s]', '', s)
    bow = {}
    for w in s.split():
        if w in bow:
            bow[w] += 1
        else: 
            bow[w] = 1
    return bow


if __name__ == "__main__":

    data = loadDocs()
    #print(data)
    numdocs = len(data[0])
    avgdl = sum(x[2] for x in data[0])/numdocs
    print(avgdl)
    k1 = 1.5
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
        print(querybow)

        for doc in data[0]:
            for w in list(querybow.keys()):
                for i in range(1,querybow[w]): # run the query word for the number of times it appears!
                    pass # TODO
            #calculate BM25 score
            idf = math.log((numdocs) / ())

        await message.channel.send(message.content)


    client.run(TOKEN)