import discord
from discord.ext import commands
from discord.commands import Option
import pymongo
from pymongo import MongoClient
from datetime import datetime
import pandas
from URCommPR.config import mongoClient, botToken

# DB Credentials
client = MongoClient(mongoClient)
db = client.voting
collection = db.VoteResults

# Initialize Bot
guild = discord.Guild
bot = commands.Bot(".", intents=discord.Intents(guilds=True, messages=True), slash_commands=True, case_insensitive=True)

# Set Date/Time For Later User
now = datetime.now()
# mm/dd/YY H:M:S
dt_string = now.strftime("%m/%d/%Y %H:%M:%S")

# Notify Bot Connection and Presence
@bot.event
async def on_ready():
    print(f'{bot.user} is online!')
    await bot.change_presence(activity=discord.Game(name="Counting Votes"))

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)} ms')

###Voting Command###

@bot.slash_command(guild_ids=[879461344322138173], description="Community Power Rankings Vote")
async def vote(ctx,
    league:Option(str, "Enter your league abbreviation"),
    team1:Option(str, "Team #1"),
    team2:Option(str, "Team #2"),
    team3:Option(str, "Team #3"),
    team4:Option(str, "Team #4"),
    team5:Option(str, "Team #5"),
    team6:Option(str, "Team #6"),
    team7:Option(str, "Team #7"),
    team8:Option(str, "Team #8"),
    team9:Option(str, "Team #9"),
    team10:Option(str, "Team #10")
):
    await ctx.respond("Thank you for participating in the Community Power Rankings for %s! You voted for: 1. %s, 2. %s, 3. %s, 4. %s, 5. %s, 6. %s, 7. %s, 8. %s, 9.%s, 10. %s" % (league.upper(), team1.upper(),team2.upper(),team3.upper(),team4.upper(),team5.upper(),team6.upper(),team7.upper(),team8.upper(),team9.upper(),team10.upper()))
    user = ctx.author
    dict = []
    dict = {
        "Submitted On:":dt_string,
        "User":str(user),
        "League":league.upper(),
        "Team 1":team1.upper(),
        "Team 2":team2.upper(),
        "Team 3":team3.upper(),
        "Team 4":team4.upper(),
        "Team 5":team5.upper(),
        "Team 6":team6.upper(),
        "Team 7":team7.upper(),
        "Team 8":team8.upper(),
        "Team 9":team9.upper(),
        "Team 10":team10.upper()
    }
    
    collection.insert_many([dict])
    print("%s vote submitted by " + str(user) % (league.upper()))

# Bot Run
bot.run = bot.run(botToken)
