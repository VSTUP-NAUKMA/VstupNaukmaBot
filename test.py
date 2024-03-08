import pickle

with open('bot.pickle', 'rb') as file:
    data = pickle.load(file)

print(data)

