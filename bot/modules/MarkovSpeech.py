from BaseModule import BaseModule
import sqlite3 as sql
import random

class MarkovSpeech(BaseModule):

    matchers = {"^!speak": "generate_sentence"}
    db = sql.connect('bot/modules/databases/markovspeechnew')
    db.row_factory = sql.Row

    def __init__(self, args):
        """
          Initialize the class as a subclass of BaseModule
          and call parent constructor with the defined matchers.
          These will be turned into regex-matchers that redirect to
          the provided function name
        """
        super(self.__class__,self).__init__(self)
        self.initialize_database()


    def generate_sentence(self,msg):
        """
        Generates a sentence by fetching a word based on the provided word,
        or picking one at random if none is provided
        """
        i = 0
        sentence = msg.clean_contents.strip().split()
        print(sentence)
        while len(sentence)<350:
          if i == 0 and not len(sentence):
            word = self.get_word(None,1)
          elif(i == 0) and len(sentence) > 0:
            word = self.get_word(sentence[-1],1)
          elif(i > 0):
            word = self.get_word(sentence[-1])

          if not word or (type(word) is str and word.strip().endswith(('.', '!', '?'))) or (type(word) is list and word[-1].strip().endswith(('.','!','?'))):
            break
          elif type(word) is list:
            sentence.extend(word)
          else:
            sentence.append(word)
          i += 1
        msg.reply(" ".join(sentence))
        return sentence

    def get_word(self,wrd, first=0):
      """
      Retrieve a word from the database. If parameter wrd is not supplied,
      and parameter first is False or 0, this function returns None.
      If wrd is supplied but first is 1 or True, wrd is discarded and a new
      word will be picked from the database based on its weight.
      """
      if not wrd and not first:
        return None

      cursor = self.db.cursor()
      if first or not wrd:
        cursor.execute('select RANDOM()*occurance as choice,w1.word as first_word,w2.word as second_word,occurance from sequence join word as w1 on w1.id=first join word as w2 on w2.id=second WHERE first_word=1 ORDER BY choice DESC LIMIT 1;')
        result = cursor.fetchone()
        return [result["first_word"].encode('utf-8'),result["second_word"].encode('utf-8')]
      elif wrd and not first:
        cursor.execute("select RANDOM()*occurance as choice,w1.word,w2.word as wrd,occurance from sequence join word as w1 on w1.id=first join word as w2 on w2.id=second WHERE w1.word=? ORDER BY choice DESC LIMIT 1;",(wrd,))
      else:
        cursor.execute("select RANDOM()*occurance as choice,w1.word,w2.word as wrd,occurance from sequence join word as w1 on w1.id=first join word as w2 on w2.id=second WHERE w1.word=? ORDER BY choice DESC LIMIT 1;",(wrd,))

      result = cursor.fetchone()
      if result:
        print(result["wrd"])
        return result["wrd"].encode('utf-8')
      else:
        return None


    def initialize_database(self):
      cursor = self.db.cursor()
      cursor.execute('CREATE TABLE IF NOT EXISTS "sequence" ("first" INTEGER NOT NULL, "second" INTEGER NOT NULL, "occurance" INTEGER DEFAULT(1));')
      cursor.execute('CREATE TABLE IF NOT EXISTS "word" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "word" TEXT NOT NULL UNIQUE);')

      self.db.commit()

    def insert_word_pair(self, first,second,first_pair=False):
      cursor = self.db.cursor()


      cursor.execute("SELECT occurance FROM sequence WHERE first=(SELECT id FROM word WHERE word=? LIMIT 1) AND second=(SELECT id FROM word WHERE word=? LIMIT 1) and first_word = ?", (first, second, first_pair))
      if not cursor.fetchone():
        cursor.execute("INSERT INTO sequence (first,second,first_word) VALUES ((SELECT id FROM word WHERE word=? LIMIT 1), (SELECT id FROM word WHERE word=? LIMIT 1),?)",(first,second,first_pair))
      else:
        cursor.execute("UPDATE sequence SET occurance=occurance+1 WHERE first=(SELECT id FROM word WHERE word=? LIMIT 1) AND second=(SELECT id FROM word WHERE word=? LIMIT 1) AND first_word=?", (first,second,first_pair))
      self.db.commit()

    def raw(self, msg):
        """ Process messages and learn """
        cursor = self.db.cursor()
        words = [(single,) for single in msg.contents.split()]
        # Add the words if it doesnt exist
        cursor.executemany("INSERT OR IGNORE INTO word (word) VALUES (?)",words)

        for index,word in enumerate(words):
          if index == 0:
            continue
          if index == 1:
            self.insert_word_pair(words[index-1][0],words[index][0],1)
          else:
            self.insert_word_pair(words[index-1][0],words[index][0],0)
