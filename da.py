import discord
import youtube_dl
from discord.ext import commands
import sys
import os
import asyncio
import socket
socket.gethostbyname("")
path = os.getcwd()
print(path)
sys.path.append(f'{path}/ffmpeg')
lst = []
lst1 = []
count = 0


tok = "NzAyMTM5MjM5MTIyNDY4OTc0.Xp7sHw.tb7X4XSUcMthvgiVEz_7hN1Vrn0"
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
async def a(ctx, arg, url="0.3", vol=0.3):
    if str(arg) == "сыграй":
        await manda(ctx, url, vol)
    if str(arg) == "фсо" and str(url) == "давай":
        await pizda(ctx)
    if str(arg) == "побазарим":
        await da(ctx)
    if str(arg) == "подкрути":
        await v(ctx, url)
    if str(arg) == "очисти":
        await clean(ctx)
    if str(arg) == "паехали":
        await r(ctx)
    if str(arg) == "стопэ":
        await p(ctx)
    if str(arg) == "хватит":
        await st(ctx)
@client.command(pass_context=True)
async def v(ctx, arg):
    global voice
    voice.source.volume = float(arg)
    

@client.command(pass_context=True)
async def da(ctx):
    print('Вызвана команда "да"')
    await ctx.send("хуйню базаришь")


@client.command(pass_context=True)
async def pizda(ctx):
    try:
        print('Вызвана команда "пизда"')
        guild = ctx.message.guild
        voice_client = guild.voice_client
        await voice_client.disconnect()
        await ctx.send("Мусора прижали")
    except Exception as e:
        await ctx.send(f'Ошибочка бля {e}')
       
async def play():
    global lst
    global lst1
    global count
    global voice
    count = 1
    while len(lst) > 0:
        ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([lst1[0])
            for file in os.listdir("./"):
                print(f'Тут файл: {file}')
                if file.endswith(".mp3"):
                    lst.append(str(file)) 
        voice.play(discord.FFmpegPCMAudio(lst[0]))
        while voice.is_playing() or voice.is_paused():
            await asyncio.sleep(1) 
        os.remove(lst[0])
        del lst[0]
        del lst1[0]              
        count = 0    
    
    
@client.command(pass_context=True)
async def manda(ctx, url, vol=0.3):
    global ydl_opts
    global count
    global lst1
    global songthere
    if len(lst1) > 1:
        await ctx.send("Добавлено в очередь")
        await ctx.send("Длина очереди " + str(len(lst1) - 1))
    else:
        await ctx.send("Зделаю дарагой ежжи")
    global voice
    try:
        channel = ctx.author.voice.channel
        print('Вызвана команда "манда"')
        voice = await channel.connect()
    except Exception as e:
        print('Error', e)

    if count == 0:
        await play()
    else:
        pass  

@client.command(pass_context=True)
async def clean(ctx):
    global lst
    lst = []
    await ctx.send("Проведена чистка среди офицеров")
    await ctx.send("Длина очереди " + str(len(lst)))
@client.command(pass_context=True)
async def p(ctx):
    global voice
    try:
        voice.pause()
    except:
        pass

async def r(ctx):
    global voice
    try:
        voice.resume()
    except:
        pass

async def st(ctx):
    global voice
    try:
        voice.stop()
    except:
        pass
@client.command(pass_context=True)
async def info(ctx):
    await ctx.send("Префикс: !a\
                  \nПроигрывание музыки: сыграй\
                  \nОтключение от голосового канала: фсо давай\
                  \nОчистка очереди проигрывания: очисти\
                  \nПауза: стопэ\
                  \nСнять с паузы: паехали\
                  \nОстановить воспроизведение: хватит\
                  \nПобазарить за жизнь: побазарим\
                  \nОбращайся дарагой")    
    
client.run(tok)
