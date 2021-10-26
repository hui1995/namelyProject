from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging
bot = ChatBot('Neutral',
storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
logic_adapters=[
    'chatterbot.logic.BestMatch'
],
filters=[
'chatterbot.filters.RepetitiveResponseFilter'
],

# 用对应的数据库，neutral-database
database = 'neutral-database'
)
bot.set_trainer(ChatterBotCorpusTrainer)
bot.train("./myApp/chatterbotTest/neutral.corpus.json")
def bot(info):
    return bot.get_response(info)
