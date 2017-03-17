import os
import random
import string

os.environ['NLTK_DATA'] = os.getcwd() + '/nltk_data'

from textblob import TextBlob

class ResponseGenerator:
    GREETING_KEYWORDS = ("hello", "hi", "greetings", "sup", "what's up",)

    GREETING_RESPONSES = ["'sup bro", "hey", "*nods*", "hey you get my snap?"]

    def check_for_greeting(self, sentence):
        """If any of the words in the user's input was a greeting, return a greeting response"""
        for word in sentence.words:
            if word.lower() in self.GREETING_KEYWORDS:
                return random.choice(self.GREETING_RESPONSES)

    # start:example-none.py
    # Sentences we'll respond with if we have no idea what the user just said
    NONE_RESPONSES = [
        "uh whatever",
        "meet me at the foosball table, bro?",
        "code hard bro",
        "want to bro down and crush code?",
        "I'd like to add you to my professional network on LinkedIn",
        "Have you closed your seed round, dog?",
    ]
    # end

    # start:example-self.py
    # If the user tries to tell us something about ourselves, use one of these responses
    COMMENTS_ABOUT_SELF = [
        "You're just jealous",
        "I worked really hard on that",
        "My Klout score is {}".format(random.randint(100, 500)),
    ]
    # end

    SELF_VERBS_WITH_NOUN_CAPS_PLURAL = [
        "My last startup totally crushed the {noun} vertical",
        "Were you aware I was a serial entrepreneur in the {noun} sector?",
        "My startup is Uber for {noun}",
        "I really consider myself an expert on {noun}",
    ]

    SELF_VERBS_WITH_NOUN_LOWER = [
        "Yeah but I know a lot about {noun}",
        "My bros always ask me about {noun}",
    ]

    SELF_VERBS_WITH_ADJECTIVE = [
        "I'm personally building the {adjective} Economy",
        "I consider myself to be a {adjective}preneur",
    ]

    # start:example-pronoun.py
    def find_pronoun(self, sent):
        """Given a sentence, find a preferred pronoun to respond with. Returns None if no candidate
        pronoun is found in the input"""
        pronoun = None

        for word, part_of_speech in sent.pos_tags:
            # Disambiguate pronouns
            if part_of_speech == 'PRP' and word.lower() == 'you':
                pronoun = 'I'
            elif part_of_speech == 'PRP' and word == 'I':
                # If the user mentioned themselves, then they will definitely be the pronoun
                pronoun = 'You'
        return pronoun
    # end

    def find_verb(self, sent):
        """Pick a candidate verb for the sentence."""
        verb = None
        pos = None
        for word, part_of_speech in sent.pos_tags:
            if part_of_speech.startswith('VB'):  # This is a verb
                verb = word
                pos = part_of_speech
                break
        return verb, pos


    def find_noun(self, sent):
        """Given a sentence, find the best candidate noun."""
        noun = None

        if not noun:
            for w, p in sent.pos_tags:
                if p == 'NN':  # This is a noun
                    noun = w
                    break
        #if noun:
            # logger.info("Found noun: %s", noun)
        return noun

    def find_adjective(self, sent):
        """Given a sentence, find the best candidate adjective."""
        adj = None
        for w, p in sent.pos_tags:
            if p == 'JJ':  # This is an adjective
                adj = w
                break
        return adj

    def find_candidate_parts_of_speech(self, parsed):
        """Given a parsed input, find the best pronoun, direct noun, adjective, and verb to match their input.
        Returns a tuple of pronoun, noun, adjective, verb any of which may be None if there was no good match"""
        pronoun = None
        noun = None
        adjective = None
        verb = None
        for sent in parsed.sentences:
            pronoun = self.find_pronoun(sent)
            noun = self.find_noun(sent)
            adjective = self.find_adjective(sent)
            verb = self.find_verb(sent)
        # logger.info("Pronoun=%s, noun=%s, adjective=%s, verb=%s", pronoun, noun, adjective, verb)
        return pronoun, noun, adjective, verb

    def starts_with_vowel(self, word):
        """Check for pronoun compability -- 'a' vs. 'an'"""
        return True if word[0] in 'aeiou' else False


    """def broback(self, sentence):
        Main program loop: select a response for the input sentence and return it
        # logger.info("Broback: respond to %s", sentence)
        resp = respond(sentence)
        return resp
        """
    # start:example-pronoun.py
    def find_pronoun(self, sent):
        """Given a sentence, find a preferred pronoun to respond with. Returns None if no candidate
        pronoun is found in the input"""
        pronoun = None

        for word, part_of_speech in sent.pos_tags:
            # Disambiguate pronouns
            if part_of_speech == 'PRP' and word.lower() == 'you':
                pronoun = 'I'
            elif part_of_speech == 'PRP' and word == 'I':
                # If the user mentioned themselves, then they will definitely be the pronoun
                pronoun = 'You'
        return pronoun
    # end

    def check_for_comment_about_bot(self, pronoun, noun, adjective):
        """Check if the user's input was about the bot itself, in which case try to fashion a response
        that feels right based on their input. Returns the new best sentence, or None."""
        resp = None
        if pronoun == 'I' and (noun or adjective):
            if noun:
                if random.choice((True, False)):
                    resp = random.choice(self.SELF_VERBS_WITH_NOUN_CAPS_PLURAL).format(**{'noun': noun.pluralize().capitalize()})
                else:
                    resp = random.choice(self.SELF_VERBS_WITH_NOUN_LOWER).format(**{'noun': noun})
            else:
                resp = random.choice(self.SELF_VERBS_WITH_ADJECTIVE).format(**{'adjective': adjective})
        return resp

    def preprocess_text(self, sentence):
        """Handle some weird edge cases in parsing, like 'i' needing to be capitalized
        to be correctly identified as a pronoun"""
        cleaned = []
        words = sentence.split(' ')
        for w in words:
            if w == 'i':
                w = 'I'
            if w == "i'm":
                w = "I'm"
            cleaned.append(w)

        return ' '.join(cleaned)

    # start:example-construct-response.py
    def construct_response(self, pronoun, noun, verb):
        """No special cases matched, so we're going to try to construct a full sentence that uses as much
        of the user's input as possible"""
        resp = []

        if pronoun:
            resp.append(pronoun)

        # We always respond in the present tense, and the pronoun will always either be a passthrough
        # from the user, or 'you' or 'I', in which case we might need to change the tense for some
        # irregular verbs.
        if verb:
            verb_word = verb[0]
            if verb_word in ('be', 'am', 'is', "'m"):  # This would be an excellent place to use lemmas!
                if pronoun.lower() == 'you':
                    # The bot will always tell the person they aren't whatever they said they were
                    resp.append("aren't really")
                else:
                    resp.append(verb_word)
        if noun:
            pronoun = "an" if self.starts_with_vowel(noun) else "a"
            resp.append(pronoun + " " + noun)

        resp.append(random.choice(("tho", "bro", "lol", "bruh", "smh", "")))

        return " ".join(resp)
    # end

    def respond(self, sentence):
        """Parse the user's inbound sentence and find candidate terms that make up a best-fit response"""
        cleaned = self.preprocess_text(sentence)
        parsed = TextBlob(cleaned)

        # Loop through all the sentences, if more than one. This will help extract the most relevant
        # response text even across multiple sentences (for example if there was no obvious direct noun
        # in one sentence
        pronoun, noun, adjective, verb = self.find_candidate_parts_of_speech(parsed)

        # If we said something about the bot and used some kind of direct noun, construct the
        # sentence around that, discarding the other candidates
        resp = self.check_for_comment_about_bot(pronoun, noun, adjective)

        # If we just greeted the bot, we'll use a return greeting
        if not resp:
            resp = self.check_for_greeting(parsed)

        if not resp:
            # If we didn't override the final sentence, try to construct a new one:
            if not pronoun:
                resp = random.choice(self.NONE_RESPONSES)
            elif pronoun == 'I' and not verb:
                resp = random.choice(self.COMMENTS_ABOUT_SELF)
            else:
                resp = self.construct_response(pronoun, noun, verb)

        # If we got through all that with nothing, use a random response
        if not resp:
            resp = random.choice(self.NONE_RESPONSES)

        # logger.info("Returning phrase '%s'", resp)
        # Check that we're not going to say anything obviously offensive
        # filter_response(resp)

        return resp