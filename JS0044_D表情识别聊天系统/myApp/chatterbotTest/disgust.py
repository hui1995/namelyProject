from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging
bot = ChatBot('Disgust',
storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
logic_adapters=[
    'chatterbot.logic.BestMatch'
],
filters=[
'chatterbot.filters.RepetitiveResponseFilter'
],

# 修改对应数据库名字 disgust-database
database = 'disgust-database'
)
bot.set_trainer(ChatterBotCorpusTrainer)
bot.train("./myApp/chatterbotTest/disgust.corpus.json")
def bot(info):
    return bot.get_response(info)
