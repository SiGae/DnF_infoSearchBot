import telebot
import infoSearchBot_private as private
import urllib.request
import json


bot = telebot.TeleBot(private.botApiToken)


infoLoad = False


@bot.message_handler(commands=['ping'])
def check_activate(message):
    bot.reply_to(message, "정상 작동 중 입니다.")


@bot.message_handler(commands=['info'])
def SearchCharName(message):
    text = message.text.replace("/info ","").split()
    charServer = text[0]
    charName = text[1]
    charInfoOrigin = 'https://api.neople.co.kr/df/servers/{0}/characters?characterName={1}&limit=50&wordType=<wordType>&apikey={2}'.format(charServer, charName, private.dnfApiToken)
    urlOpen = urllib.request.urlopen(charInfoOrigin)
    infoJSON = json.load(urlOpen)

    infoLoad = True
    characterId = infoJSON.rows[0]['characterId']
    characterName = infoJSON.rows[0]['characterName']
    level = infoJSON.rows[0]['level']
    jobId = infoJSON.rows[0]['jobGrowId']
    jobGrowId = infoJSON.rows[0]['jobGrowId']
    jobName = infoJSON.rows[0]['jobName']
    jobGrowName = infoJSON.rows[0]['jobGrowName']

    text = "캐릭터이름 : {0}\n레벨 : {1}\n직업 : {2}\n전직 : {3}".format(characterName, level, jobName, jobGrowName)


    bot.reply_to(message, text)

bot.polling()