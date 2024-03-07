# This example requires the 'message_content' intent.
from discord.ext import tasks, commands
import dbhidden
import discord
import dblist
import random
import pickle
from datetime import datetime
import schedule
import time
import os

@tasks.loop(hours=24)
async def checkblacklist():
    for guild in client.guilds:
        if guild.id in blacklist:
            to_leave=client.get_guild(guild.id)
            await to_leave.leave()
            print('left',guild)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

myfilepath=os.path.dirname(os.path.abspath(__file__))
holidaypath=os.path.join(myfilepath, 'holidays.pkl')
#print(holidaypath)
#abspath=pathlib.Path("holidays.pkl").absolute()
#print(abspath)

with open(holidaypath, 'rb') as f:
    holidays = pickle.load(f)
    print(holidays)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}, listing current guilds:')
    checkblacklist.start()
    
    for guild in client.guilds:
        print(guild, guild.id)
        #blacklist sort of 
        if guild.id in blacklist:
            to_leave=client.get_guild(guild.id)
            await to_leave.leave()
            print('left',guild)

blacklist=[1053161232535912478, #"Cyberland", supery spammy
           1070550154417021029, #"Club 57", spammy
           899144844381917254, #Bot Repo, spammy
           ]

canieligible=[]

def getdatesuffix(myDate):
    date_suffix = ["th", "st", "nd", "rd"]

    if myDate % 10 in [1, 2, 3] and myDate not in [11, 12, 13]:
        return date_suffix[myDate % 10]
    else:
        return date_suffix[0]

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    imsonly=["i'm","im"]

    global knockknock
    global knockknockwho
    global knockknockindex

    try:
        adj=""
        for word in dblist.adj:
            #print ('checking',word,'against',message.content)
            if word in message.content.lower():
                adj=word
                print('found',adj,'in',message.content,'from',message.guild, 'with guild id', message.guild.id)
                break
        if len (adj)>0:
            imsadj=["i'm "+adj,"im "+adj]
            if any(word in message.content.lower() for word in imsadj):
                print('found',word,'in ',message.content)
                sendmsg="Hi "+adj+", I'm Dad!"
                print('sending himessage',sendmsg)
                await message.cahnnel.send(sendmsg)


            #messageparts=message.content.split()
            #print('checking',adj,'with messageparts',messageparts)
            #listitem=0
            #for part in messageparts:
           #     nextpart=messageparts[listitem+1]
            #    #print ('checking',part,'listitem',listitem,'parts+1',nextpart)
             #   listitem+=1
              #  if (part.lower() in imsonly) and (nextpart == adj):
               #     sendmsg="Hi "+nextpart.lower()+", I'm Dad!"
                #    print('sending himessage',sendmsg)
                   # await message.channel.send(sendmsg)
                  #  #print('sentmessage')
                   # break

    except:
        print("im error handled")


    jokes=dblist.jokes

    try:
        if  ("dad" in message.content.lower()) and ("joke" in message.content.lower()) and ("knock" not in message.content.lower()):
            print('found joke in',message.content)
            sendjoke=random.choice(jokes)
            print('sending joke',sendjoke)
            await message.channel.send(sendjoke)

    except:
        print("joke error handled")


    love=("love you dadbot", "love you dad")
    try:
        if  any(word in message.content.lower() for word in love):
            print('found love you in',message.content)
            print('sending thanks')
            await message.channel.send("thanks")

    except:
        print("thanks error handled")


    hello=("hello there")
    try:
        if  hello == message.content.lower():
            print('found hello there in',message.content)
            await message.channel.send("general kenobi")

    except:
        print("hello there error handled")


    thanksdad=["thanks dad","thanks dadbot"]
    try:
        if any(word in message.content.lower() for word in thanksdad):
            print('found thanks in',message.content,'from user',message.author)
            await message.reply(random.choice(dblist.welcome)+", "+str(message.author.name))

    except:
        print("welcome error handled")

    hidad=["hi dad","hello dad","hey dad"]

    author=None
    greetings=dblist.greetings

    try:
        if  any(word in message.content.lower() for word in hidad):
            print('found hidad in',message.content,'from user',message.author)
            #himessage=message
            sendhi=random.choice(greetings)
            author=str(message.author.name)
            await message.reply(sendhi+", "+author,mention_author=True)

    except:
        print("hi dad error handled")

    implaying=["i'm playing", "im playing"]

    try:
        if  any(word in message.content.lower() for word in implaying):
            print('found implaying in',message.content,'from user',message.author)
            author=str(message.author.name)
            await message.reply("Are you winning, "+author+"?",mention_author=True)

    except:
        print("i'm playing error handled")

    agua=dblist.agua

    try:
        if  "big iron" in message.content.lower():
            print('found bigiron in',message.content)
            #wait message.reply("aguaholder",mention_author=True)
            await message.channel.send(agua)

    except:
        print("bigiron error handled")



    try:
        if  "saturdays are made for dads" in message.content.lower():
            print('found saturday in',message.content)
            await message.reply("and Dad's car!")

    except:
        print("saturday error handled")
    
    try:
        if ("can i" in message.content.lower()) and ("knock" not in message.content.lower()):
            print('found cani in',message.content)
            canieligible.append(message.author.name)
            await message.channel.send("I don't know, can you?")

    except:
        print("cani error handled")

    mays=("may i", "may we", "can you", "can we", "will you", "are you")
    nos=dblist.no

    try:
        if  (any(word in message.content.lower() for word in mays)) and (message.author.name in canieligible) and ("knock" not in message.content.lower()):
            print('found mayi in',message.content)
            canieligible.remove(message.author.name)
            await message.channel.send(random.choice(nos))

    except:
        print("mayi error handled")   

    whatday=("what day is it today","wdiit")         

    try:
        if  (any(word in message.content.lower() for word in whatday)) and ("dad" in message.content.lower()):
            print('found what day in',message.content)
            today=datetime.now()
            todayholidays=holidays[today.strftime("%B")+' '+str(today.day)+getdatesuffix(today.day)+', '+str(today.year)]
            await message.channel.send(random.choice(todayholidays))

    except:
        print("wdiitd error handled")

    knockknocklist=("knockknock","knock-knock","knock knock")

    try:
        if (any(word in message.content.lower() for word in knockknocklist) and ("dad" in message.content.lower())):
            print('initiating knock knock cycle')
           # print('knockknockvar preinit',knockknock)
            knockknock=True
           # print('knockknockvar postinit',knockknock)
            await message.channel.send('Knock knock')
    except:
        print('knock knock initiation error handled')
        
    whosthere=("whos there", "who's there", "whose there")

    knockknockinitlist=dblist.knockknockinit

    try:
        if  (any(word in message.content.lower() for word in whosthere) and knockknock):
             #print('knockknockvar prewhosethere',knockknock)
             knockknockinit=random.choice(knockknockinitlist)
             knockknockwho=knockknockinit+' who'
             knockknockindex=knockknockinitlist.index(knockknockinit)
             print('knockknockwho',knockknockwho,'knockknockindex',knockknockindex)
             await message.channel.send(knockknockinit)
    except:
        print('knock knock first response error handled')

    knockknockresponselist=dblist.knockknockresp
#(knockknockwho != None) and 
    try:
        #print('-------------------------------knockknockwho',knockknockwho,'knockknockindex',knockknockindex,'knockknockbool',knockknock)
        #print('knockknockwho',knockknockwho)
        #print('message',message.content.lower())
        #print(knockknockwho,knockknock)
        if  (knockknockwho != None) and (knockknockwho.lower() in message.content.lower()) and knockknock:
             #print('pass2')
             #print('knockknockvar presendresponse',knockknock)
             await message.channel.send(knockknockresponselist[knockknockindex])
             knockknock=False
             knockknockwho=None
             knockknockindex=None
             print('closed knock knock cycle')
             #print('knockknockvar postsendrespose',knockknock)

    except:
        print('knock knock final response error handled')
                        
knockknock = False
knockknockwho=None
knocknockindex=None

client.run(dbhidden.token)