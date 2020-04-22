import discord
import youtube_dl
from discord.ext import commands
import os
tok = "NzAyMTM5MjM5MTIyNDY4OTc0.Xp7stQ.NpHjcGMxJ09WUYfR1XsqqaApoT4"
client = commands.Bot(command_prefix='!')
@client.command(pass_context=True)
async def da(ctx, arg):
    await ctx.send("хуйню базаришь")
@client.command(pass_context=True)
async def pizda(ctx):
    guild = ctx.message.guild
    voice_client = guild.voice_client
    await voice_client.disconnect()
    await ctx.send("Откинулся Аркадий")
@client.command(pass_context=True)
async def manda(ctx, url):
    channel = ctx.author.voice.channel
    voice = await channel.connect()

    await ctx.send("Зделаю дарагой ежжи")
    songthere = os.path.isfile("song.mp3")
    if songthere:
        os.remove("song.mp3")

    ydl_opts = {
        "format": "bestaudio/beat",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
client.run(tok)
