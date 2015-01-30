from datetime import datetime
import sqlite3 as sql

from BaseModule import BaseModule



class User(BaseModule):

    matchers = {"!seen": "last_seen", "!greet": "force_greet_user", "!addgreeting": "add_greeting", "!dropgreeting": "remove_greeting"}
    events = { "joined": "update_last_seen_and_greet", "parted": "update_last_seen" }
    db = sql.connect('bot/modules/databases/user')
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


    def force_greet_user(self, msg):
      """ Force me to say hi to someone """
      if self.first_seen(msg.clean_contents):
        msg.reply(self.get_greeting('new'))
      else:
        greeting = self.get_greeting(msg.clean_contents)
        if greeting:
          msg.reply(greeting)

    def greet_user(self, event):
      if self.first_seen(event.author):
        msg.reply(self.get_greeting('new'))
      else:
        greeting = self.get_greeting(event.author)
        if greeting:
          msg.reply(greeting)

    def get_greeting(self, username):
      """ Retrieves greeting for a user (or generic if none found) """
      cursor = self.db.cursor()
      cursor.execute('SELECT message FROM greeting WHERE user = ? AND channel = ? ORDER BY RANDOM() LIMIT 1',(username,))
      user_greeting = cursor.fetchone()
      if user_greeting:
        return user_greeting["message"]
      else:
        return None

    def add_greeting(self, msg):
      """ Add a new greeting. Arguments are: user message """
      split_message = msg.clean_contents.split()
      user = split_message.pop(0)
      greeting = " ".join(split_message)

      cursor = self.db.cursor()
      cursor.execute('INSERT INTO "greeting" (user, message, channel) VALUES (?,?,?)', (user, greeting, msg.channel))
      self.db.commit()
      cursor.execute('SELECT id FROM "greeting" WHERE user=? ORDER BY id DESC LIMIT 1',(user,))
      last_id = cursor.fetchone()
      last_id = last_id["id"]

      if last_id:
        msg.reply("Hey, {sender}, I'll remember this the next time I see {user} (#{id})".format(sender=msg.author,user=user, id=id))
      else:
        msg.reply("Oops, crap, I already forgot what you said ...")


    def remove_greeting(self, msg):
      """ Removes a greeting identified by its ID. IDs are shown when greetings are added or posted """
      greeting_id = re.search(r'(\d+)',msg.contents)

      if greeting_id:
        greeting_id = greeting_id.group(1)
      else:
        msg.reply("I'm so sorry, but I don't think I even remember that one! :(")
        return

      cursor = self.db.cursor()
      cursor.execute("DELETE FROM greeting WHERE id=?",(greeting_id,))
      if cursor.commit():
        msg.reply("Okay, okay, fine! I get it ... I won't say that again, alright?")

    def first_seen(self, user):
      """
      Checks if the user has ever been seen before the last 10 sec
      """
      cursor = self.db.cursor()
      cursor.execute("SELECT first_seen FROM user WHERE user = ?",(user.lower(),))
      results = cursor.fetchone()
      if results:
        if results["first_seen"]:
          diff = datetime.now() - datetime.strptime(results["first_seen"], "%Y-%m-%d %H:%M:%S")
          if diff.seconds < 10 and diff.days < 1:
            return True
      return False

    ##
    ## Last seen and user timestamps
    ##
    def last_seen(self,message):
      """
      Updates timestamp for when a user last joined or parted a channel
      """
      cursor = self.db.cursor()
      cursor.execute("SELECT * FROM user WHERE user = ?",(message.clean_contents.lower(),))
      results = cursor.fetchone()
      if results:
        message.reply("I last saw {user} {time}".format(user=message.author,time=self.how_long_ago(results["timestamp"])))
      return message


    def update_last_seen_and_greet(self,event):
      """
      Updates last seen time for a user when (s)he joined or parted
      """
      cursor = self.db.cursor()
      cursor.execute("INSERT OR REPLACE INTO user (user,first_seen) VALUES(?,(SELECT first_seen FROM user WHERE user = ? LIMIT 1))", (event.author.lower(),event.author.lower()))
      self.db.commit()
      self.greet_user(event)
      return None

    def how_long_ago(self, date):
      """
      Turn a past date into how long ago it was, i.e 2 hours ago, 1 hour ago, yesterday.
      Provide either a timestamp or a past date
      """

      now = datetime.now()

      if type(date) is int:
        difference = now - datetime.fromtimestamp(date)
      elif isinstance(date,datetime):
        difference = now - date
      elif not date:
        difference = 0
      else:
        difference = now - datetime.strptime(date, "%Y-%m-%d %H:%M:%S")


      if difference.days < 0:
        return '... I dont even know who I am anymore'

      if difference.days == 0:
        if difference.seconds < 10:
          return "just now"
        elif difference.seconds < 60:
          return str(difference.seconds) + " seconds ago"
        elif difference.seconds < 120:
          return "a minute ago"
        elif difference.seconds < 3600:
          return str(difference.seconds/60) + " minutes ago"
        elif difference.seconds < 7200:
          return "an hour or so ago"
        elif difference.seconds < 86400:
          return str(difference.seconds/3600) + " hours ago"
      if difference.days == 1:
        return "yesterday"
      if difference.days < 7:
        return str(difference.days) + " days ago"
      if difference.days < 31:
        return str(difference.days/7) + " weeks, " + str(difference.days % 7) + " days ago"
      if difference.days < 365:
        return str(difference.days/30) + " months, " + str(difference.days % 30) + " days ago"
      return str(difference.days/365) + " years ago"

    def initialize_database(self):
      cursor = self.db.cursor()
      cursor.execute('CREATE TABLE IF NOT EXISTS "user" ("user" TEXT PRIMARY KEY NOT NULL, "first_seen" INTEGER NOT NULL DEFAULT (CURRENT_TIMESTAMP), "timestamp" INTEGER NOT NULL DEFAULT (CURRENT_TIMESTAMP));')
      cursor.execute('CREATE TABLE IF NOT EXISTS "greeting" ("id" INTEGER PRIMARY KEY AUTOINCREMENT, "user" TEXT NOT NULL, "message" TEXT NOT NULL, "channel" TEXT NOT NULL);')
      self.db.commit()
