import asyncio
import discord
from discord import Guild,Member,VoiceChannel

async def move_callback(user:Member,channel:VoiceChannel)->None:
  await user.move_to(channel=channel)

async def move(
  loop:asyncio.AbstractEventLoop,
  dataList:list[dict[str,str]],
  guild:Guild,
) -> None:  
  for data in dataList:
    channel:VoiceChannel = guild.get_channel(int(data["channelId"]))
    if channel is None:continue
    for userId in data["userIds"]:
      user:Member = guild.get_member(userId)
      if user is None:continue
      asyncio.run_coroutine_threadsafe(
        move_callback(user=user,channel=channel),
        loop=loop
      )
      
def guildInfo(guild:Guild)->dict:
  guildId = guild.id
  icon = guild.icon

  channels = [{
    "channelId":channel.id,
    "channelName":channel.name,
    "joinMember":[member.id for member in channel.members],
  } for channel in guild.voice_channels]

  guildMemberIds = [member.id for member in guild.members]
  canMove = [member.id for channel in guild.voice_channels for member in channel.members]
  notMove = [member for member in guildMemberIds if not member in canMove]
      
  data = {
    "guildId":guildId,
    "iconUrl":f"https://cdn.discordapp.com/icons/{guildId}/{icon}.webp",
    "channels":channels,
    "canMoveMember":canMove,
    "notMoveMember":notMove,
    "allMember":guildMemberIds
  }
  return data

def userInfo(guild:Guild,userId:int)->dict:
  user:Member = guild.get_member(userId)
  userNick = user.nick
  userName = user.name
  iconUrl = f"https://cdn.discordapp.com/avatars/{userId}/{user.avatar}.webp"

  data = {
    "userId":userId,
    "userName":userName,
    "userNick":userNick,
    "iconUrl":iconUrl
  }
  return data

def channelInfo(guild:Guild,channelId:int) -> dict:
  channel:discord.abc.GuildChannel = guild.get_channel(channelId)
  if not channel.type == discord.ChannelType.voice:
    return {"guildId":None}
  channelName = channel.name
  guildId = guild.id
  join = [member.id for member in channel.members]
  data = {
    "guildId":guildId,
    "channelId":channelId,
    "channelName":channelName,
    "join":join
  }
  return data