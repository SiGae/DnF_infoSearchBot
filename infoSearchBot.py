import telebot
import infoSearchBot_private as private
import urllib.request
import urllib.parse
import json
import ssl


bot = telebot.TeleBot(private.botApiToken)


infoLoad = False


def remove_none(text):
    if text is None:
        return ""
    else:
        return text

def FindServerName(serverName) -> str:
    findServerName = {
        '카인':'cain',
        '안톤':'anton',
        '힐더': 'hillder',
        '프레이': 'prey',
        '카시야스': 'casillas',
        '디레지에': 'diregie',
        '바칼': 'bakal',
        '시로코': 'sirocos',
    }
    getServer = findServerName[serverName]

    return getServer


@bot.message_handler(commands=['ping'])
def check_activate(message):
    bot.reply_to(message, "정상 작동 중 입니다.")

@bot.message_handler(commands=['auc'])
def SearchAuction(message):
    searchItem = message.text.replace("/auc ", "")
    print(searchItem)
    print(1)
    url = 'https://api.neople.co.kr/df/auction?sort=unitPrice:asc&'
    print(3)
    param = urllib.parse.urlencode({

        'itemName': searchItem,
        'limit': 5,
        'wordType': 'full',
        'apikey': private.dnfApiToken
    })

    ssl._create_default_https_context = ssl._create_unverified_context

    print(2)
    print(url + param)
    urlOpen = urllib.request.urlopen(url + param)
    # print(1)
    infoJSON = json.loads(urlOpen.read().decode('utf-8'))

    k = 0
    while k < 5:
        a = '이름 : {}\n'.format(infoJSON['rows'][k]['itemName'])
        a += '개당 가격 : {}\n'.format(infoJSON['rows'][k]['unitPrice'])
        a += '총액 : {}\n'.format(infoJSON['rows'][k]['currentPrice'])
        a += '수량 : {}\n'.format(infoJSON['rows'][k]['count'])
        k += 1
        bot.send_message(message.chat.id, a)
    i = 0

@bot.message_handler(commands=['search'])
def SearchCharName(message):
    text = message.text.replace("/search ", "").split()
    print(text)
    charServer = FindServerName(text[0])
    charName = text[1]
    charInfoOrigin = 'https://api.neople.co.kr/df/servers/{}/characters?'.format(charServer)
    param = urllib.parse.urlencode({
        'characterName': charName,
        'limit': 50,
        'wordType': 'match',
        'apikey': private.dnfApiToken
    })

    ssl._create_default_https_context = ssl._create_unverified_context

    print(charInfoOrigin + param)
    urlOpen = urllib.request.urlopen(charInfoOrigin + param)
    print(1)
    infoJSON = json.loads(urlOpen.read())
    print(2)

    infoLoad = True
    characterId = infoJSON['rows'][0]['characterId']
    characterName = infoJSON['rows'][0]['characterName']
    level = infoJSON['rows'][0]['level']
    jobId = infoJSON['rows'][0]['jobGrowId']
    jobGrowId = infoJSON['rows'][0]['jobGrowId']
    jobName = infoJSON['rows'][0]['jobName']
    jobGrowName = infoJSON['rows'][0]['jobGrowName']

    text = "캐릭터이름 : {0}\n레벨 : {1}\n직업 : {2}\n전직 : {3}".format(characterName, level, jobName, jobGrowName)


    bot.reply_to(message, text)


@bot.message_handler(func=lambda Alwaystrue: True)
def always(message):
    print(message, end='\n\n')

bot.polling()
