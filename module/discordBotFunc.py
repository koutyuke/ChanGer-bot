import discord
from requests import post, request
from dotenv import load_dotenv
from flask import Flask,jsonify,request as FlaskRequest
from discord import Guild,Member,VoiceChannel,VoiceState


def channel_create(channel:VoiceChannel) -> dict:
  guild:Guild = channel.guild
  guildId = guild.id
  type = "create"
  channelId = channel.id
  data = {
    "guildId":guildId,
    "type":type,
    "data":{
      "channelId":channelId
    }
  }
  return data

def channel_delete(channel:VoiceChannel):
  guild:Guild = channel.guild
  guildId = guild.id
  type = "delete"
  channelId = channel.id
  data = {
    "guildId":guildId,
    "type":type,
    "data":{
      "channelId":channelId
    }
  }
  return data


def voice_state(before:VoiceState,after:VoiceState,user:Member):
  
  beforeChannel = before.channel
  afterChannel = after.channel
  voiceType = "connect" if beforeChannel is None else ("disconnect" if afterChannel is None else "change")

  beforeId = None if voiceType == "connect" else before.channel.id
  afterId = None if voiceType == "disconnect" else after.channel.id
  
  data = {
    "guildId":user.guild.id,
    "type":voiceType,
    "data":{
      "beforeChannelId":beforeId,
      "afterChannelId":afterId,
      "userId":user.id
    }
  } 
  return data