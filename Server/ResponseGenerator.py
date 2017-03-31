import os
import random
import string

from datetime import datetime
from Utilities import Utilities
from Weather import Weather

class ResponseGenerator:

    name = 'maya'
    weather = Weather()

    whQuestions = [ 'what', 'who', 'why', 'where', 'when', 'which', 'whom', 'whose', 'how' ]
    askingKeywords = [ 'tell me' ]

    timeDateKeywords = [ 'time', 'date', 'day' ]
    dayResponses = [ 'sir, today is ', 'today is ' ]
    timeResponses = [ 'sir, it is ', "it's ", 'it is ' ]
    
    greetings = [ 'hello', 'hello sir', 'hey', 'hi', 'greetings', "what's up" ]
    howAreYouResponses = [ "i'm good sir", 'i am feeling good', 'feeling better sir', 'my system is working fine sir' ]

    callByNameResponses = [ 'yes sir?', 'yes', 'tell me sir, how can I help you?' ]

    def getWords(self, sentence):
        return sentence.split(' ')
    
    def isSelf(self, words):
        _list = [ 'you', 'your' ]

        for word in words:
            if word in _list:
                return True

    def isGreeting(self, sentence):
        for word in self.greetings:
            if sentence.__contains__(word):
                return True

    def isWhQuestion(self, sentence):
        isWhQuestion = False

        for whQuestion in self.whQuestions:
            if sentence.__contains__(whQuestion):
                isWhQuestion = True

                break
        
        return isWhQuestion, whQuestion
    
    def isAsking(self, words):
        for word in words:
            if word in self.askingKeywords:
                return True
    
    def getCurrentSystemTime(self):
        return datetime.now().strftime(Utilities.getValueFromConfigurationFile("time-format"))
    
    def getCurrentSystemDate(self):
        return datetime.now().strftime(Utilities.getValueFromConfigurationFile("date-format"))
    
    def hasNumbers(self, sentence):
        return any(char.isdigit() for char in sentence)

    def calculate(self, words):
        i = 0
        result = 0.0
        operator = ''
        _list = [ "sir, if I'm not mistaken, the result should be ", "the result is " ]

        for word in words:
            if word == '+' or word == '-' or word == 'x' or word == 'into' or word == '/' or word == 'divided' or word == 'by' or word == 'over':
                operator = word
            else:
                try:
                    if i == 0:
                        result = float(word)
                    elif operator == '+':
                        result += float(word)
                    elif operator == '-':
                        result -= float(word)
                    elif operator == 'x' or operator == 'into':
                        result *= float(word)
                    elif operator == '/' or operator == 'divided' or operator == 'by' or 'over':
                        result /= float(word)
                    
                    i += 1
                except:
                    continue
        
        return str(result)

    def getResponse(self, sentence):        # major modification needs to be done...
        response = None
        sentence = sentence.lower()
        words = self.getWords(sentence)

        if self.isGreeting(words):
            response = random.choice(self.greetings)
        elif self.hasNumbers(sentence) and (sentence.__contains__('+') or sentence.__contains__('-') or sentence.__contains__('into') or sentence.__contains__('x') or sentence.__contains__('/') or sentence.__contains__('divided') or sentence.__contains__('by') or sentence.__contains__('over')):
            response = self.calculate(words)
        elif sentence.__contains__('time') and (sentence.__contains__('date') or sentence.__contains__('day')):
            response = random.choice(self.dayResponses) + self.getCurrentSystemDate() + ' and ' + random.choice(self.timeResponses) + self.getCurrentSystemTime()
        elif sentence.__contains__('time'):
            response = random.choice(self.timeResponses) + self.getCurrentSystemTime()
        elif sentence.__contains__('date') or sentence.__contains__('day'):
            response = random.choice(self.dayResponses) + self.getCurrentSystemDate()
        elif sentence.__contains__(self.name):
            response = random.choice(self.callByNameResponses)
        elif sentence.__contains__('weather'):
            response = self.weather.getWeatherStatus("Dhaka, BD")
        elif sentence.__contains__('temperature'):
            response = self.weather.getTemperature("Dhaka, BD")
        elif sentence.__contains__('humidity'):
            response = self.weather.getHumidity("Dhaka, BD")
        elif sentence.__contains__('wind'):       # needs to be fixed...
            response = self.weather.getWindInformation("Dhaka, BD")
        elif sentence.__contains__('sunrise') or sentence.__contains__('sunshine') or (sentence.__contains__('sun') and (sentence.__contains__('rise') or sentence.__contains__('shine'))):
            _list = [ 'rise', 'shine' ]
            
            response = 'Sun will ' + random.choice(_list) + ' at ' + self.weather.getSunriseTime("Dhaka, BD")
        elif sentence.__contains__('sunset') or (sentence.__contains__('sun') and sentence.__contains__('set')):
            _list = [ 'set' ]
            
            response = 'Sun will ' + random.choice(_list) + ' at ' + self.weather.getSunsetTime("Dhaka, BD")
        elif self.isSelf(words):
            response = 'True'       # needs to be implemented...
        else:
            response = sentence
        
        return response