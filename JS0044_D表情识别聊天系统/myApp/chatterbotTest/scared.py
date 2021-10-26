from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging
bot = ChatBot('Scared',
storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
logic_adapters=[
    'chatterbot.logic.BestMatch'
],
filters=[
'chatterbot.filters.RepetitiveResponseFilter'
],

# 换成对应语料库
database = 'scared-database'
)
bot.set_trainer(ChatterBotCorpusTrainer)
bot.train("./myApp/chatterbotTest/scared.corpus.json")
def bot(info):
    return bot.get_response(info)

