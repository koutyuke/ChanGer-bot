import asyncio
import string
import discord
import flask
import os
import time
import threading
from pprint import pprint

from dotenv import load_dotenv
from flask import Flask

intents = discord.Intents.all()
client = discord.Client(intents=intents)
loop = client.loop

load_dotenv()
print(os.environ["DISCORD_TOKEN"])

def bot ():
  global client 
  
  @client.event
  async def on_ready():
    print("logged in\n")
    
  client.run(os.environ["DISCORD_TOKEN"])
  
def api():
  global client,loop
  time.sleep(4)
  
  async def move_voice():
    global client,loop
    guild = client.get_guild(854266006738305050)
    members = guild.members
    channel = guild.get_channel(854266006738305054)
    pprint(channel)
    
    for member in members:
      if member.name == "こうちゅけ":
        # async with client:
        await member.move_to(channel) ##問題
        return 200
    return 500
    
  app = Flask(__name__)
  @app.route('/')
  def hello():
    user = client.get_guild(854266006738305050)
    pprint(user.members)
    return str(user.name) 
  
  @app.route('/hoge')
  async def move():
    user = client.get_user(687588356875354126) 
    pprint(user)
    return user.name
  
  @app.route('/fuga')
  async def fuga():
    global client
    send_fut = asyncio.run_coroutine_threadsafe(move_voice(),loop=loop)
    data=send_fut.result()
    return str(data)
  
  app.run()  
  
  
  
thread_bot = threading.Thread(target=bot)
thread_api = threading.Thread(target=api) 


if __name__  == "__main__":
  thread_bot.start()
  thread_api.start()
  thread_bot.join()
  thread_api.join()