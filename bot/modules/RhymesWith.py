from BaseModule import BaseModule
import nltk
import random
from twisted.python import log

class RhymesWith(BaseModule):

    matchers = [{"regex": "!rhyme", "function": "rhyme",
                 "description": "Returns a random word that rhymes with a given word"}
                ]

    def __init__(self, args):
        """
          Initialize the class as a subclass of BaseModule
          and call parent constructor with the defined matchers.
          These will be turned into regex-matchers that redirect to
          the provided function name
        """
        super(self.__class__,self).__init__(self)

    def rhyme(self,msg):
        """ Gives a random word that rhymes with msg.contents """
        log.msg("Trying to find a word that rhymes with {}".format(msg.clean_contents))
        entries = nltk.corpus.cmudict.entries()
        syllables = [(word, syl) for word, syl in entries if word == msg.clean_contents]
        rhymes = []
        for (word, syllable) in syllables:
             rhymes += [word for word, pron in entries if pron[-3:] == syllable[-3:]]
        rhyme = random.choice(rhymes)

        log.msg("Found {nrhymes} words that rhyme with {mess} and chose {rhyme}".format(nrhymes=len(rhymes), mess=msg.clean_contents, rhyme=rhyme))
        msg.reply(rhyme.encode('utf-8'))
        return rhyme.encode('utf-8')
