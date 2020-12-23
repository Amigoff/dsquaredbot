import discord
import youtube_dl
from discord.ext import commands
import sys
import asyncio
import socket
from random import randint
import random
from gtts import gTTS
import requests
import datetime
from recognizer import recorgnize
from config import *
from logger import logger
from copy import copy


logger = logger('BOT')

socket.gethostbyname("")
path = os.getcwd()
print(path)
sys.path.append(f'{path}/ffmpeg')
lst = []
lst1 = []
count = 0

intents = discord.Intents.default()
intents.members = True


client = commands.Bot(command_prefix='~', intents=intents)

RECORDING = {}
PLAYING_DATE = None


def load_opus_lib(opus_libs=OPUS_LIBS):
    """Загрузка opus"""
    if discord.opus.is_loaded():
        return True

    for opus_lib in opus_libs:
        try:
            discord.opus.load_opus(opus_lib)
            return 0
        except OSError as e:
            logger.error(f'error os: {e}')
    return 1


if load_opus_lib():
    logger.warning('Can not load opus')
else:
    logger.info('OPUS LOADED')


@client.command(pass_context=True, alias=['а'])
async def a(ctx, *arg):
    """Обработка сообщений по префиксу 'a'"""
    global mes
    global golos
    global t
    global tt
    global RECORDING

    # Превращение аргументов в строку (замена имени бота на "")
    arg_str = ' '.join(arg).lower().replace("{} ".format(NAME), '')
    target = arg[-1]

    if "сыграй" in arg_str:
        url = arg[1:]
        if len(arg) == 2:
            await manda(ctx, url[0])
        else:
            await manda(ctx, url)

    elif "фсо" in arg_str or ('всё' in arg_str and 'пока' in arg_str):
        RECORDING = {}
        await pizda(ctx)

    elif "побазарим" in arg_str:
        await da(ctx)

    elif "подкрути" in arg_str:
        url = arg[-1]
        await v(ctx, url)

    elif "очисти" in arg_str:
        await clean(ctx)

    elif "паехали" in arg_str:
        await resume_playing(ctx)

    elif "стопэ" in arg_str:
        await pause_playing(ctx)

    elif "хватит" in arg_str:
        await stop_playing(ctx)

    elif 'рулетка' in arg_str:
        await random4ik(ctx)

    elif str(arg_str) == 'расскажи чё на районе':
        await information(ctx, 'Москва, Алексеевская')

    elif 'расскажи' in arg_str:
        if target == 'расскажи':
            target = None
        await information(ctx, target or 'Москва, Красная площадь', 12)

    elif str(arg_str) == 'погода на районе':
        await weather(ctx, 'Москва, Алексеевская')

    elif arg_str == 'погода':
        await weather(ctx, target or 'Москва')

    elif str(arg_str) == 'пробки на районе':
        await traffic(ctx, 'Москва, Алексеевская')

    elif arg_str == 'пробки':
        await traffic(ctx, target or 'Красная площадь', 12)

    elif 'вероятность' in str(arg).lower():
        await posib(ctx, arg)

    elif 'скажи' in str(arg).lower():
        await skaji(ctx, arg)

    elif 'кто' in str(arg).lower():
        await who(ctx, arg)

    elif 'когда' in str(arg).lower():
        await when(ctx, arg)

    elif "анальная рулетка" in str(arg).lower():
        await anal(ctx)

    elif "или" in str(arg):
        await choose(ctx, arg)

    elif "голосование" in str(arg).lower():
        t = ""
        for k in arg[1:-int(arg[-1]) - 1]:
            t += " "
            t += str(k)
        await vibori(ctx, arg[-int(arg[-1]) - 1:-1])

    elif "голосую" in str(arg).lower():
        if str(arg[-1]).lower() in golos:
            golos[str(arg[-1]).lower()] += 1
            await mes.delete()
            stroka = "Голосование" + str(t)
            for item in tt:
                stroka += "\n"
                stroka += str(item + ": " + str(golos[item]))
            mes = await ctx.send(stroka)
        else:
            await ctx.send("Нет такого варианта")
    else:
        return 1
    return 0
   

@client.command(pass_context=True)
async def vibori(ctx, arg):
    global golos
    global mes
    global t
    global tt
    global lst1
    global voice
    golos = {}
    stroka = "Голосование" + str(t)
    s_arg = ""
    for k in arg:
        s_arg += k 
        s_arg += " "
    tt = s_arg.split()
    for item in tt:
        golos[str(item)] = 0
        stroka += "\n"
        stroka += str(item + ": " + str(golos[item]))

    embed = get_embed(title='ГОЛОСОВАНИЕ', description=stroka, color=discord.Colour(COLOR_BLUE))
    mes = await ctx.send(embed=embed)
    try:
        channel = ctx.author.voice.channel
        voice = await channel.connect()
    except:
        pass
    lst1.append("https://youtu.be/XjuWHekyRtA")
    try:
        await play(ctx)
    except:
        pass 


@client.command(pass_context=True)
async def choose(ctx, arg):
    list = ""
    for i in arg:
        list += " " + i
    lt = list.split("или")    
    sl = choice(lt)
    await ctx.send(sl)


@client.command(pass_context=True)
async def start_recognizion(ctx, *args):

    async def create_tasks():
        loop = asyncio.get_event_loop()

        task1 = loop.create_task(recognizion(ctx, start=True, time_delta=0, loop=loop))
        task2 = loop.create_task(recognizion(ctx, start=False, time_delta=3, loop=loop))

        await task1
        await task2

    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_tasks())


async def recognizion(ctx, start=True, time_delta=0, loop=None):
    global NAME

    await asyncio.sleep(time_delta)

    if start:
        await say(ctx, "Начинаем, ежжи, рад тебя снова видеть")

    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()
    
    if start and RECORDING.get(ctx.author.mention):
        await say(ctx, 'Уже распознаю твою речь, брат, э. Стопаю')
        RECORDING.pop(ctx.author.mention)
        return

    RECORDING[ctx.author.mention] = True
    
    wave_file = datetime.datetime.now().strftime("%y%m%d_%H%M%S") + '.wav'
    
    while ctx.voice_client or RECORDING.get(ctx.author.mention):
        open(wave_file, 'a').close()
        if True:
            ctx.voice_client.listen(discord.UserFilter(discord.WaveSink(str(wave_file)), ctx.author))
        else:
            # TODO: Проверить работоспособность
            ctx.voice_client.listen(discord.WaveSink(str(wave_file)))

        await asyncio.sleep(5)
        ctx.voice_client.stop_listening()
        # await say(ctx, "Ща распознаем, что ты сказал, долбоёб!")
        try:
            result = recorgnize(wave_file)
            await ctx.send("- {}".format(result))
            if f"{NAME} " in result.lower():

                await ctx.send('Выполняю')

                # TODO: Транслит команд
                if 'сено' in result:
                    await CENA(ctx)
                    return
                loop = asyncio.get_event_loop()

                task_message_handler = loop.create_task(a(ctx, *result.split()))

        except Exception as e:
            if "{}".format(e):
                ctx.send('Ошибка: {}'.format(e))
            else: 
                await say(ctx, 'Ошибка {}, брат'.format(e))
    RECORDING[ctx.author.mention] = False
    
    
@client.command(pass_context=True)
async def anal(ctx, arg=None):
    global lst1
    global voice
    try:
        channel = ctx.author.voice.channel
        voice = await channel.connect()
    except:
        pass
    num = randint(0, 6)
    spisAk = ["https://www.youtube.com/watch?v=idJKsVao0Kk", "https://www.youtube.com/watch?v=VWxjcQjHA7o",
             "https://www.youtube.com/watch?v=NqX7GsLaOJM", "https://www.youtube.com/watch?v=MnnXemPKR7w", "https://www.youtube.com/watch?v=vHjY3okumj4"
             "https://www.youtube.com/watch?v=KTfyGVI9Yxc"]
    vid = spisAk[num]
    lst1.append(vid)
    await play(ctx)


@client.command(pass_context=True)
async def alah(ctx, arg=None):    
    global lst1
    global voice
    try:
        channel = ctx.author.voice.channel
        voice = await channel.connect()
    except:
        pass
    lst1.append("https://www.youtube.com/watch?v=tW9YEa7-zTI")
    await play(ctx)
    

@client.command(pass_context=True)
async def vader(ctx, arg=None):    
    global lst1
    global voice
    try:
        channel = ctx.author.voice.channel
        voice = await channel.connect()
    except:
        pass
    lst1.append("https://www.youtube.com/watch?v=U49RgwMSHc0")
    await play(ctx)


@client.command(pass_context=True)
async def goroskop(ctx, arg=None):
    start = ['Всё будет хорошо', "Всё будет плохо", 'Вы умрёте', "Вы будете жить", 'Завтра вы умрёте',
             'Аллах Агбар']
    mid = ['вас ждёт успех', 'вас ждёт победа', 'вас ждёт поражение', '100%', 'деньги придут к вам', 'вы потеряете 100 рублей на дороге']
    el = 'скоро вы получите {} по {}'.format(randint(2, 5), choice(['математике', "физике", "русскому", "обществу", "какой-то херне"]))
    p = randint(1, 4)
    if p == 1:
        await ctx.send(el)
    elif p == 2:
        member = '{}'.format(choice(ctx.guild.members).mention)
        texts = ['Отрежет вам яйца', "Съест вас", "Отдаст вам долг", "Решит за вас домашку", "и вы решите сбежать вместе",
                 "прыгнет с 11 этажа", "скажет вам что-то важное"]
        await ctx.send('{} {}'.format(member, choice(texts)))
    else:
        await ctx.send(choice(start) + ' ' + choice(mid))


@client.command(pass_context=True)
async def posib(ctx, arg=None):
    # arg = arg.lower().replace('вероятность', '').replace('что', '').replace(',', '')
    await ctx.send('{}%'.format(randint(0, 100)))

    
@client.command(pass_context=True)
async def skaji(ctx, arg=None):
    # await ctx.send('{}'.format(['Да, Аллах говорит, что будет так' if randint(0, 1) else 'Нет'][0]))
    await say(ctx, str(arg))


@client.command(pass_context=True)
async def who(ctx, arg=None):
    member = '{}'.format(choice(ctx.guild.members).mention)
    await ctx.send(member)


@client.command(pass_context=True)
async def when(ctx, arg=None):
    if randint(0, 100) > 50:
        start_date = datetime.date.today().replace(day=1, month=1, year=2021).toordinal()
        end_date = datetime.date.today().replace(day=31, month=12, year=2050).toordinal()
        random_day = datetime.date.fromordinal(random.randint(start_date, end_date))
        await ctx.send('Это произойдёт {}'.format(random_day.isoformat()))
    else:
        start_date = datetime.date.today().replace(day=1, month=1, year=2021).toordinal()
        end_date = datetime.date.today().replace(day=31, month=12, year=2021).toordinal()
        random_day = datetime.date.fromordinal(random.randint(start_date, end_date))
        await ctx.send('Скоро. А именно: {}'.format(random_day.isoformat()))


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
    members = channel.members

    async def a():
        loop = asyncio.get_event_loop()

        task1 = loop.create_task(set_nicknames('AND HIS NAME IS JOHN SENO', members))
        task2 = loop.create_task(play(ctx))

        await task1
        await task2

    loop = asyncio.get_event_loop()
    loop.run_until_complete(a())


async def set_nicknames(new, members):
    N = 15
    old_name = {}
    for member in members:
        old_name[member.id] = {'old_name': member.name, 'error': 0}
    for _ in range(0, 10):
        for i in range(len(new) - N + 1):
            for member in members:
                if not old_name[member.id]['error']:
                    try:
                        await member.edit(nick=new[i:i + N])
                    except:
                        old_name[member.id]['error'] = 1
                        continue

    for member in members:
        if not old_name[member.id]['error']:
            await member.edit(nick=old_name[member.id]['old_name'])


@client.command(pass_context=True)
async def da(ctx):
    logger.info('Вызвана команда "побазарим"')
    await ctx.send("Без баб")


@client.command(pass_context=True)
async def random4ik(ctx):
    global voice
    logger.info("Играем в рулетку!")
    channel = ctx.author.voice.channel

    try:
        voice = await channel.connect()
    except:
        pass
    logger.info('Channel members: {}'.format(channel.members))
    random_user = choice(channel.members)

    guild = ctx.message.guild
    logger.info('MEMBERS GUILD: {}'.format(guild.members))

    kick_channel = await guild.create_voice_channel(name='kick')

    await ctx.send("Выигрывает {}! Нахуй с пляжа, петушок".format(random_user.display_name))
    await random_user.edit(voice_channel=kick_channel)
    await kick_channel.delete()
    await say(ctx, 'Ха-ха, бля')


@client.command(pass_context=True)
async def say(ctx, *arg):
    global voice
    global PLAYING_DATE
    arg_str = ' '.join(arg)
    logger.info('Говорю {}'.format(arg_str))
    try:
        channel = ctx.author.voice.channel
        voice = await channel.connect()
    except Exception as e:
        logger.error(f'ОШИБКА ПОЛУЧЕНИЯ VOICE: {e}')
    
    logger.debug(': {}'.format(arg_str))
    
    if not isinstance(arg_str, str):
        tts = gTTS(arg_str, lang='ru')
    else:
        tts = gTTS(str(arg_str), lang='ru')
    
    filename = datetime.datetime.now().strftime("%y%m%d_%H%M%S") + '.mp3'
    tts.save(filename)
        
    try:
        if voice.is_playing():
            if not PLAYING_DATE:
                PLAYING_DATE = datetime.datetime.now()

            voice.stop()
            timestamp = datetime.datetime.now() - PLAYING_DATE
            voice.play(discord.FFmpegPCMAudio(filename))
            while voice.is_playing():
                await asyncio.sleep(1)

            await play(ctx, timestamp)
        else:
            voice.play(discord.FFmpegPCMAudio(filename))
            while voice.is_playing() or voice.is_paused():
                await asyncio.sleep(1)
    except Exception as e:
        logger.warning('err', e)
    os.remove(filename)


@client.command(pass_context=True)
async def weather(ctx, city=None):

    if not city:
        city = 'Moscow'

    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                       params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': whether_api_key})
    data = res.json()
    logger.debug(data)
    if data['cod'] != 200:
        return await say(ctx, "Ошибка вышла, не могу узнать текущую погоду")

    data = res.json()
    conditions = data['weather'][0]['description']
    temp = round(data['main']['temp'])
    temp_min = round(data['main']['temp_min'])
    temp_max = round(data['main']['temp_max'])
    if city == 'Moscow':
        city = 'Москва'
    text = "Сейчас в {} {}. Температура {} градус.".format(city, conditions, temp)
    if temp_min != temp_max:
        text += "Максимально будет {}, минимально {} градусов.".format(temp_max, temp_min)
    text += 'Скорость ветра {} метров в секунду'.format(data['wind']['speed'])
    return await say(ctx, text)


@client.command(pass_context=True)
async def information(ctx, *args):
    await weather(ctx, args[-1])
    await traffic(ctx, *args)


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


@client.command(pass_context=True)
async def traffic(ctx, *args):
    if represents_int(args[-1]):
        zoom = args[-1]
        place = ' '.join(args[:-1])
    else:
        zoom = 13
        place = ' '.join(args)

    if not place:
        place = 'Moscow'

    x1, y1, x2, y2 = fetch_coordinates(place)
    x = (x1 + x2) / 2
    y = (y1 + y2) / 2
    filename = load_map_by_coords(x, y, zoom=zoom)
    await say(ctx, 'Отправляю карту пробок...')
    await ctx.send(file=discord.File(filename))


def load_map_by_coords(x, y, zoom=16, typ="map,trf"):
    """Получение карты по координатам"""
    ll = str(x) + "," + str(y)
    map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}".format(ll=ll, z=zoom, type=typ)
    response = requests.get(map_request)
    if not response:
        logger.warning("Ошибка выполнения запроса:")
        logger.warning(map_request)
        logger.warning("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запись полученного изображения в файл.
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        logger.warning("Ошибка записи временного файла:", ex)
    return map_file


def fetch_coordinates(place):
    """Получение координат места на карте"""
    base_url = "https://search-maps.yandex.ru/v1/"
    params = {"text": str(place), 'type': 'geo', "apikey": yandex_api_key, "format": "json", 'lang': 'ru-RU'}
    response = requests.get(base_url, params=params)
    # print(response.json())
    response_data = response.json()['properties']['ResponseMetaData']['SearchResponse']
    lon1, lat1 = response_data['boundedBy'][0]
    lon2, lat2 = response_data['boundedBy'][1]
    return lon1, lat1, lon2, lat2


@client.command(pass_context=True)
async def pizda(ctx):
    try:
        logger.info('Вызвана команда "пизда"')
        guild = ctx.message.guild
        voice_client = guild.voice_client
        await voice_client.disconnect()
        await ctx.send("Мусора прижали")
    except Exception as e:
        await ctx.send(f'Ошибочка бля {e}')


async def play(ctx, timestamp=None):
    global lst
    global lst1
    global count
    global voice
    global PLAYING_DATE
    count = 1

    if not timestamp:
        timestamp = datetime.timedelta(seconds=0)

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
            video_link = lst1[0]
            logger.info(f"Пытаюсь сыграть: {video_link}")
            if not str(video_link).startswith("http"):
                arg = " ".join(video_link)
                logger.debug(arg)
                video_link = "ytsearch: " + arg

            info = ydl.extract_info(video_link, download=False)
            logger.info(str(info))

            # Если у нас играет плейлист (т.е. трек был найден через поиск),
            # то берём первое найденное видео
            if info.get('_type') == 'playlist':
                info = info['entries'][0]

            URL = info['formats'][0]['url']

        ffmpeg_options = copy(FFMPEG_OPTIONS)

        # Если timestamp != default, то играем с timestamp
        if timestamp.seconds != 0:
            ffmpeg_options['options'] += f'-ss {timestamp.seconds}'
        else:
            PLAYING_DATE = datetime.datetime.now()

        voice.play(discord.FFmpegPCMAudio(URL, **ffmpeg_options))

        dur = info["duration"] / 60 or "Стрим"
        if dur != 'Стрим':
            dur = str(round(dur, 2)) + 'мин.'

        text = "Играю: " + info['title'] + f'\nДлительность: {dur}\n\n'

        embed = get_embed(title='Проигрывание музыки', color=discord.Colour(COLOR_GREEN), description=text)
        await ctx.send(embed=embed)

        while voice.is_playing() or voice.is_paused():
            await asyncio.sleep(1)

        try:
            lst1.pop(0)
            lst.pop(0)
        except Exception as e:
            pass
    count = 0    


def get_embed(title, color=discord.Colour(COLOR_BLUE), description=''):
    embed = discord.Embed(
        title=title,
        colour=color,
        description=description,
    )
    return embed


@client.command(pass_context=True)
async def manda(ctx, url):
    global ydl_opts
    global count
    global lst1
    global songthere
    lst1.append(url)
    if len(lst1) > 1:
        text = Phrases().get_phrase_playing_music('queue', len(lst1) - 1)
        embed = get_embed(title='Проигрывание музыки', color=discord.Colour(COLOR_YELLOW), description=text)
        await ctx.send(embed=embed)
    else:
        text = Phrases().get_phrase_playing_music('ok', len(lst1) - 1)
        embed = get_embed(title='Проигрывание музыки', color=discord.Colour(COLOR_GREEN), description=text)
        await ctx.send(embed=embed)

    global voice
    try:
        channel = ctx.author.voice.channel
        logger.info('Вызвана команда "манда"')
        voice = await channel.connect(timeout=10.0)
    except Exception as e:
        logger.error('Error: {}'.format(e))

    if count == 0:
        logger.info(lst1)
        await play(ctx)
    else:
        pass  


@client.command(pass_context=True)
async def clean(ctx):
    global lst1
    global lst
    lst = []
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.remove(file)
    lst1 = []
    await ctx.send("Проведена чистка среди офицеров")
    await ctx.send("Длина очереди " + str(len(lst1)))

    
@client.command(pass_context=True)
async def pause_playing(ctx):
    global voice
    try:
        voice.pause()
    except:
        pass


async def resume_playing(ctx):
    global voice
    try:
        voice.resume()
    except:
        pass


async def stop_playing(ctx):
    global voice
    try:
        voice.stop()
    except:
        pass
    await clean(ctx)

    
@client.command(pass_context=True)
async def info(ctx):
    embed = get_embed(title='Шпора', color=discord.Colour(COLOR_BLUE), description='')
    embed.add_field(name="Обращайся дорогой", value="Тут список того, что я умею", inline=False)
    embed.add_field(name="!a сыграй <ссылка> (или) <поиск по названию>", value="Воспроизведение музыки", inline=False)
    embed.add_field(name="!a фсо давай (или) всё пока", value="Отключение от голосового канала",
                    inline=False)
    embed.add_field(name="!a очисти",
                    value="Очистка очереди проигрывания музыки",
                    inline=False)
    embed.add_field(name="!a стопэ",
                    value="Пауза музыки", inline=False)
    embed.add_field(name="!a хватит", value="Остановить воспроизведение",
                    inline=False)
    embed.add_field(name="!a побазарим",
                    value="Побазарить за жизнь", inline=False)
    embed.add_field(name="!a расскажи чё на районе",
                    value="Рассказать ситуацию на райончике", inline=False)
    embed.add_field(name="!a расскажи <Город>",
                    value="Рассказать ситуацию где-то ещё", inline=False)
    embed.add_field(name="!a погода <Город>",
                    value="Рассказать про погоду", inline=False)
    embed.add_field(name="!a пробки <Город>",
                    value="Рассказать про пробки", inline=False)
    embed.add_field(name="!a голосование <вариант1> <вариант2>",
                    value="Запустить голосование", inline=False)
    embed.add_field(name="!a голосую <вариант>",
                    value="Проголосовать в созданном голосовании", inline=False)
    embed.add_field(name="!a кто <описание>",
                    value="Сказать, кто", inline=False)
    embed.add_field(name="!a когда <описание>",
                    value="Сказать, когда произойдёт что-то", inline=False)
    embed.add_field(name="!a вероятность <описание>",
                    value="Вычислить вероятность", inline=False)
    embed.add_field(name="!anal",
                    value="Анальная рулетка", inline=False)
    embed.add_field(name="!CENA",
                    value="Джон Сина", inline=False)
    embed.add_field(name="!vader",
                    value="Вэйдер", inline=False)

    await ctx.send(embed=embed)

client.run(tok)
