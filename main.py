import discord
import os
import time
import threading
from httplib2 import Response
from requests import post, request
from dotenv import load_dotenv
from flask import Flask,jsonify,request as FlaskRequest
from discord import Guild,Member
from module.flaskFunc import move,guildInfo, userInfo,channelInfo

intents = discord.Intents.all()
client = discord.Client(intents=intents)
loop = client.loop

app = Flask(__name__)

load_dotenv()
print(os.environ["DISCORD_TOKEN"])

def bot ():
  global client 
  
  @client.event
  async def on_ready():
    await client.change_presence(activity=discord.Game(name="ChanGer",type=discord.ActivityType.playing))
    print("logged in\n")
    
  @client.event
  async def on_guild_channel_create(channel):
    if channel.type == discord.ChannelType.voice:
      data = {
        "guildId":channel.guild.id,
        "type":"create",
        "data":{
          "channelId":channel.id,
        }
      }
      print(data)
    
  @client.event
  async def on_guild_channel_delete(channel):
    if channel.type == discord.ChannelType.voice:
      data = {
        "guildId":channel.guild.id,
        "type":"delete",
        "data":{
          "channelId":channel.id,
        }
      }
      print("hoge")
      
  @client.event
  async def on_voice_state_update(member,before,after):
    print("h")
    if before.channel != after.channel:
      print(before,after) 
      beforeId = before.channel.id
      afterId = after.channel.id
      
  @client.event
  async def on_message(message):
    if not message.author.bot:
      print("put url") 
    
    
  client.run(os.environ["DISCORD_TOKEN"])
    
def api():
  global client,loop,app
  
  time.sleep(4)
    
  @app.route('/moveChannel',methods=['GET'])
  async def moveChannel():
    guildId = FlaskRequest.args.get("guildId",type=int)
    datas:list[dict[str,str]] = eval(FlaskRequest.args.get("data"))
    guild:Guild = client.get_guild(guildId)
    
    if guild is None:return jsonify({"response":404})
    await move(
      loop=loop,
      dataList=datas,
      guildId=guild,
    )
    return jsonify({"response":200})

  @app.route('/getGuild',methods=['GET'])
  async def getGuild() -> Response:
    guildId = FlaskRequest.args.get("guildId",type=int)
    guild:Guild = client.get_guild(guildId)
    if guild is None: return jsonify({"guildId":None})
    data = guildInfo(guild=guild)
    return jsonify(data)
    
  @app.route('/getUser',methods=['GET'])
  async def getUser() -> Response:
    guildId = FlaskRequest.args.get("guildId",type=int)
    userId = FlaskRequest.args.get("userId",type=int)
    guild:Guild = client.get_guild(guildId)
    if guild is None: return jsonify({"guildId":None})
    data = userInfo(guild=guild,userId=userId)    
    return jsonify(data)

  @app.route('/getChannel',methods=['GET'])
  async def getChannel():
    guildId = FlaskRequest.args.get("guildId",type=int)
    channelId = FlaskRequest.args.get("channelId",type=int)
    guild:Guild = client.get_guild(guildId)
    if guild is None: return jsonify({"guildId":None})
    data = channelInfo(guild=guild,channelId=channelId)
    
    return jsonify(data)
  
  
  app.run(
    # host="localhost",
    # port=3001
  )  
  

thread_bot = threading.Thread(target=bot)
thread_api = threading.Thread(target=api) 

if __name__  == "__main__":
  thread_bot.start()
  thread_api.start()
  thread_bot.join()
  thread_api.join()