# coding: utf-8
import pandas as pd

# print(pd.__version__)

df = pd.read_csv('NBAPlayers.txt',sep='\t')

df.replace({'Player':{'Curly Armstrong':'allen'}})
print(df.head())
