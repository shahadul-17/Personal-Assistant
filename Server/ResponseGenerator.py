import os
import random
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
    
    greetings = [ 'hello', 'hello sir' 'hey', 'hi', 'greetings', "what's up" ]
    howAreYouResponses = [ "i'm good sir", 'i am feeling good', 'feeling better sir', 'my system is working fine sir' ]

    callByNameResponses = [ 'yes sir?', 'yes', 'tell me sir, how can I help you?' ]

    def getWords(self, sentence):
        return sentence.split(' ')
    
    def isGreeting(self, words):
        for word in words:
            if word in self.greetings:
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
        return datetime.now().strftime("%I:%M %p")
    
    def getCurrentSystemDate(self):
        return datetime.now().strftime("%d-%B-%Y")
    
    def calculate(self, words):
        result = 0.0
        operator = ''

        for word in words:
            if word == 'calculate':
                continue
            elif word == '+' or word == '-':
                operator = word
                
                continue
            else:
                if operator == '+':
                    result += float(word)
                elif operator == '-':
                    result -= float(word)
        
        return str(result)

    def getResponse(self, sentence):
        response = ''
        sentence = sentence.lower()
        words = self.getWords(sentence)

        # _textBlob = TextBlob(sentence) -> to extract all the parts of speech...

        if self.isGreeting(words):
            response += random.choice(self.greetings)
        
        response += ', '

        if sentence.__contains__('calculate') and (sentence.__contains__('+') or sentence.__contains__('-')):
            response += self.calculate(words)
        elif self.isWhQuestion(sentence) == (True, self.whQuestions[0]) or self.isAsking(words):
            if sentence.__contains__("'s") or sentence.__contains__('is') or sentence.__contains__('the'):
                if sentence.__contains__('time') and (sentence.__contains__('date') or sentence.__contains__('day')):
                    response += random.choice(self.dayResponses) + self.getCurrentSystemDate() + ' and ' + random.choice(self.timeResponses) + self.getCurrentSystemTime()
                elif sentence.__contains__('time'):
                    response += random.choice(self.timeResponses) + self.getCurrentSystemTime()
                elif sentence.__contains__('date') or sentence.__contains__('day'):
                    response += random.choice(self.dayResponses) + self.getCurrentSystemDate()
        elif sentence.__contains__(self.name):
            response += random.choice(self.callByNameResponses)
        
        return response + '\r\n'