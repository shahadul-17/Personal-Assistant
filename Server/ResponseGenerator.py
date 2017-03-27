import os
import random
import re
import string

os.environ['NLTK_DATA'] = os.getcwd() + '/nltk_data'

from datetime import datetime
from textblob import TextBlob

class ResponseGenerator:
    name = 'maya'

    whQuestions = [ 'what', 'who', 'why', 'where', 'when', 'which', 'whom', 'whose', 'how' ]
    askingKeywords = [ 'tell me' ]

    timeDateKeywords = [ 'time', 'date', 'day' ]
    dayResponses = [ 'sir, today is ', 'today is ' ]
    timeResponses = [ 'sir, it is ', "it's ", 'it is ' ]
    
    greetings = ['hello\n', 'hello sir\n', 'hey\n', 'hi\n', 'greetings\n', "what's up\n"]
    howAreYouResponses = ["i'm good sir", 'i am feeling good', 'feeling better sir', 'my system is working fine sir']

    callByNameResponses = ['yes sir?', 'yes', 'tell me sir, how can I help you?']

    def getWords(self, sentence):
        return sentence.split(' ')
    
    def isGreeting(self, sentence):
        if self.greetings.__contains__(sentence):
            return True
        return False

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
        return datetime.now().strftime("%I:%M %p")
    
    def getCurrentSystemDate(self):
        return datetime.now().strftime("%d-%B-%Y")
    
    def hasNumbers(self, sentence):
        return any(char.isdigit() for char in sentence)

    def calculate(self, words):
        i = 0
        result = 0.0
        operator = ''

        for word in words:
            if word == '+' or word == '-' or word == 'x' or word == 'into' or word == '/' or word == 'divided' or word == 'by' or word == 'over':
                operator = word

            else:
                try:
                    if operator == '+':
                        result += float(word)
                    elif operator == '':
                        result = float(word)
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
    
    def checkDatabase(self, _textBlob):     # finds appropriate keyword to respond...
        for x in os.walk(".\\data\\"):
            for fileName in x[2]:
                for word in _textBlob.words:
                    if word == fileName:
                        return str(x[0] + '\\' + fileName)
    
    def getInformation(self, path, _textBlob):
        information = ''

        with open(path) as file:
            for line in file:
                line = line.strip()

                _lineTextBlob = TextBlob(line)

                for keyword in set(_lineTextBlob.words):
                    if _textBlob.__contains__(keyword.lower()):
                        information += line
                
        return information
    
    def getResponse(self, sentence):
        response = ''
        sentence = sentence.lower()
        if self.isGreeting(sentence):
            response += random.choice(self.greetings)
        words = self.getWords(sentence)
        _textBlob = TextBlob(sentence)

        # response += self.getInformation(self.checkDatabase(_textBlob), _textBlob)

        response += response

        if self.hasNumbers(sentence) and (sentence.__contains__('+') or sentence.__contains__('-') or sentence.__contains__('into') or sentence.__contains__('x') or sentence.__contains__('/') or sentence.__contains__('divided') or sentence.__contains__('by') or sentence.__contains__('over')):
            response += self.calculate(words)
        elif sentence.__contains__('time') and (sentence.__contains__('date') or sentence.__contains__('day')):
            response += random.choice(self.dayResponses) + self.getCurrentSystemDate() + ' and ' + random.choice(self.timeResponses) + self.getCurrentSystemTime()
        elif sentence.__contains__('time'):
            response += random.choice(self.timeResponses) + self.getCurrentSystemTime()
        elif sentence.__contains__('date') or sentence.__contains__('day'):
            response += random.choice(self.dayResponses) + self.getCurrentSystemDate()
        elif sentence.__contains__(self.name):
            response += random.choice(self.callByNameResponses)
        
        return response