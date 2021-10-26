from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging
bot = ChatBot('Surprised',
storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
logic_adapters=[
    'chatterbot.logic.BestMatch'
],
filters=[
'chatterbot.filters.RepetitiveResponseFilter'
],

# 修改成对应的数据库 surprised-database
database = 'surprised-database'
)
bot.set_trainer(ChatterBotCorpusTrainer)
bot.train("./myApp/chatterbotTest/surprised.corpus.json")

def bot(info):
    return bot.get_response(info)


