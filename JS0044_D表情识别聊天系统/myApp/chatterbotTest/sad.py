from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging
bot = ChatBot('Sad',
storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
logic_adapters=[
    'chatterbot.logic.BestMatch'
],
filters=[
'chatterbot.filters.RepetitiveResponseFilter'
],

# 需要对应数据库 sad-database
database = 'sad-database'
)
bot.set_trainer(ChatterBotCorpusTrainer)
bot.train("./myApp/chatterbotTest/sad.corpus.json")
def bot(info):
    return bot.get_response(info)
