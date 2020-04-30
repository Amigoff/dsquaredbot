import discord
import youtube_dl
from discord.ext import commands
import sys
import os
import asyncio
path = os.getcwd()
print(path)
sys.path.append(f'{path}/ffmpeg')
lst = []
count = 0


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
    global count
    global voice
    count = 1
    while len(lst) > 0:
        urp = lst[0]
        songthere = os.path.isfile("song.mp3")
        if songthere:
            os.remove("song.mp3")   
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([urp])
        for file in os.listdir("./"):
            print(f'Тут файл: {file}')
            if file.endswith(".mp3"):
                name = file
                os.rename(file, "song.mp3")        
             
        voice.play(discord.FFmpegPCMAudio("song.mp3"))
        while voice.is_playing() or voice.is_paused():
            await asyncio.sleep(1)
        try:    
            lst.remove(urp)
        except:
            pass
    count = 0    
    
    
@client.command(pass_context=True)
async def manda(ctx, url, vol=0.3):
    global ydl_opts
    global count
    global lst
    global songthere
    lst.append(url)
    if len(lst) > 1:
        await ctx.send("Добавлено в очередь")
        await ctx.send("Длина очереди " + str(len(lst) - 1))
    else:
        await ctx.send("Зделаю дарагой ежжи")
    global voice
    try:
        channel = ctx.author.voice.channel
        print('Вызвана команда "манда"')
        songthere = os.path.isfile("song.mp3")
        voice = await channel.connect()
    except Exception as e:
        print('Error', e)

    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }
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
async def help(ctx):
    await ctx.send("Префикс: !a \n
                  Проигрывание музыки: сыграй \n
                  Отключение от голосового канала: фсо давай \n
                  Очистка очереди проигрывания: очисти \n
                  Пауза: стопэ \n
                  Снять с паузы: паехали \n
                  Остановить воспроизведение: хватит \n
                  Побазарить за жизнь: побазарим \n
                  Обращайся дарагой")
    
client.run(tok)
