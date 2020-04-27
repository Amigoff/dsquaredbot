import discord
import youtube_dl
from discord.ext import commands
import sys
import os
path = os.getcwd()
print(path)
sys.path.append(f'{path}/ffmpeg')

tok = "NzAyMTM5MjM5MTIyNDY4OTc0.XqA3pw.Y7-YPukENatknfDO0raXiyV5NiU"
client = commands.Bot(command_prefix='!')

OPUS_LIBS = ['libopus.so.0.5.3', 'libopus-0.x86.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']


def load_opus_lib(opus_libs=OPUS_LIBS):
    if discord.opus.is_loaded():
        return True

    for opus_lib in opus_libs:
        try:
            discord.opus.load_opus(opus_lib)
            return
        except OSError as e:
            print('error os', e)

        #raise RuntimeError('Could not load an opus lib. Tried %s' % (', '.join(opus_libs)))

load_opus_lib()
print('opus_loaded')

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
    try:
        channel = ctx.author.voice.channel
        voice = await channel.connect()
        print('Вызвана команда "манда"')
        await ctx.send("Зделаю дарагой ежжи")
        songthere = os.path.isfile("song.mp3")
        if songthere:
            os.remove("song.mp3")

        ydl_opts = {
            "format": "bestaudio/best",
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
        try:        
            voice.play(discord.FFmpegPCMAudio("song.mp3"))
        except Exception as e:
            print('Error', e)
    except Exception as e:
        print('Error', e)
        try:
            await ctx.send(f'уа уа Ошибочка бля {e}')
        except:
            pass    
    
client.run(tok)
