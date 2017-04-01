import pandas as pd

planets = pd.read_excel('../data/MovieData/PlannetData.xlsx')
print(planets.head())

def KeyWords(self, wordlist):
    fields = ['Name']
    df = planets
