import discord
import youtube_dl
from discord.ext import commands
import sys
import os
import time

path = os.getcwd()
print(path)
sys.path.append(f'{path}/ffmpeg')

tok = "NzAyMTM5MjM5MTIyNDY4OTc0.Xp__5Q.HCQ_UQLz-2irr6xGt0_L9-NNkn4"
client = commands.Bot(command_prefix='!')


@client.command(pass_context=True)
async def da(ctx, arg):
    print('Вызвана команда "да"')
    await ctx.send("хуйню базаришь")


@client.command(pass_context=True)
async def pizda(ctx):
    try:
        print('Вызвана команда "пизда"')
        guild = ctx.message.guild
        voice_client = guild.voice_client
        await voice_client.disconnect()
        await ctx.send("Откинулся Аркадий")
    except Exception as e:
        await ctx.send(f'Ошибочка бля {e}')


@client.command(pass_context=True)
async def manda(ctx, url):
    # try:
    print('Вызвана команда "манда"')
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
        print(f'Тут файл: {file}')
        if file.endswith(".mp3"):
            name = file
            os.rename(file, "song.mp3")

    user = ctx.message.author
    voice_channel = user.voice.voice_channel
    channel = None
    # only play music if user is in a voice channel
    if voice_channel != None:
        # grab user's voice channel
        channel = voice_channel.name
        await client.say('User is in channel: ' + channel)
        # create StreamPlayer
        vc = await client.join_voice_channel(voice_channel)
        player = vc.create_ffmpeg_player('song.mp3', after=lambda: print('done'))
        player.start()
        while not player.is_done():
            await time.sleep(1)
        # disconnect after the player has finished
        player.stop()
        await vc.disconnect()
    # voice.play(discord.FFmpegPCMAudio("song.mp3"))
    # except Exception as e:
    #     await ctx.send(f'уа уа Ошибочка бля {e}')
client.run(tok)
