import sqlite3 as sql
from BaseModule import BaseModule


class User(BaseModule):

    matchers = {"!seen": "last_seen"}
    events = { "joined": "update_last_seen", "parted": "update_last_seen" }
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

    def update_last_seen(self,event):
      """Updates last seen time for a user when (s)he joined or parted"""
      cursor = self.db.cursor()
      cursor.execute("INSERT OR REPLACE INTO user (user) VALUES(?)", (event.author.lower(),))
      self.db.commit()
      return None

    def how_long_ago(self, date):
      """
      Turn a past date into how long ago it was, i.e 2 hours ago, 1 hour ago, yesterday.
      Provide either a timestamp or a past date
      """
      from datetime import datetime
      now = datetime.now()

      if type(date) is int:
        difference = now - datetime.fromtimestamp(date)
      elif isinstance(date,datetime):
        difference = now - date
      elif not date:
        difference = 0
      else:
        difference = now - datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        print(type(date))


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
      cursor.execute('CREATE TABLE IF NOT EXISTS "user" ("user" TEXT PRIMARY KEY NOT NULL, "timestamp" INTEGER NOT NULL DEFAULT (CURRENT_TIMESTAMP));')
      self.db.commit()
