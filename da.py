import discord
import youtube_dl
from discord.ext import commands
import sys
import os
import asyncio
import socket
from random import choice
from gtts import gTTS

socket.gethostbyname("")
path = os.getcwd()
print(path)
sys.path.append(f'{path}/ffmpeg')
lst = []
lst1 = []
count = 0

intents = discord.Intents.default()
intents.members = True

tok = "NzAyMTM5MjM5MTIyNDY4OTc0.Xp7sHw.tb7X4XSUcMthvgiVEz_7hN1Vrn0"
client = commands.Bot(command_prefix='!', intents=intents)

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
    if str(arg) == 'рулетка':
        await random4ik(ctx)


@client.command(pass_context=True)
async def v(ctx, arg):
    global voice
    voice.source.volume = float(arg)


@client.command(pass_context=True)
async def CENA(ctx):    
    global lst1
    global voice
    lst1.append("https://www.youtube.com/watch?v=-cZ7ndjhhps&t=13s")
    try:
        channel = ctx.author.voice.channel
        voice = await channel.connect()
    except:
        pass
    await play()


@client.command(pass_context=True)
async def da(ctx):
    print('Вызвана команда "да"')
    await ctx.send("С дном рождения, пидарас")


@client.command(pass_context=True)
async def random4ik(ctx):
    global voice
    print("Играем в рулетку!")
    channel = ctx.author.voice.channel

    try:
        voice = await channel.connect()
    except:
        pass
    print('Channel members: {}'.format(channel.members))
    random_user = choice(channel.members)

    guild = ctx.message.guild
    print('MEMBERS GUILD: {}'.format(guild.members))

    kick_channel = await guild.create_voice_channel(name='kick')

    await ctx.send("Выигрывает {}! Нахуй с пляжа, петушок".format(random_user.display_name))
    await random_user.edit(voice_channel=kick_channel)
    await kick_channel.delete()
    await say(ctx, 'Ха-ха, бля')


@client.command(pass_context=True)
async def say(ctx, arg):
    channel = ctx.author.voice.channel
    print('Вызвана команда "манда"')
    try:
        voice = await channel.connect()
    except:
        voice = channel

    tts = gTTS(arg, lang='ru')
    tts.save('answer.mp3')

    voice.play(discord.FFmpegPCMAudio('answer.mp3'))
    while voice.is_playing() or voice.is_paused():
        await asyncio.sleep(1)


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
    while len(lst1) > 0:
        ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ur = lst1[0]
            print(ur)
            print("Тут ссылка")
            ydl.download([ur])
            for file in os.listdir("./"):
                print(f'Тут файл: {file}')
                if file.endswith(".mp3"):
                    lst.append(str(file)) 
        voice.play(discord.FFmpegPCMAudio(lst[0]))
        while voice.is_playing() or voice.is_paused():
            await asyncio.sleep(1) 
        os.remove(lst1[0])
        del lst1[0]              
    count = 0    
    
    
@client.command(pass_context=True)
async def manda(ctx, url, vol=0.3):
    global ydl_opts
    global count
    global lst1
    global songthere
    lst1.append(url)
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
        print(lst1)
        await play()
    else:
        pass  

@client.command(pass_context=True)
async def clean(ctx):
    global lst1
    lst1 = []
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
