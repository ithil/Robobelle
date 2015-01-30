import urllib
import re

from BaseModule import BaseModule
from bs4 import BeautifulSoup
import praw


class PreviewTitle(BaseModule):

    matchers = {"!sub": "sub_new", "!hot": "sub_hot", "!top": "sub_top"}
    r = praw.Reddit(user_agent = "Mirabelle")

    def __init__(self, args):
        """
          Initialize the class as a subclass of BaseModule
          and call parent constructor with the defined matchers.
          These will be turned into regex-matchers that redirect to
          the provided function name
        """
        super(self.__class__,self).__init__(self)

    def sub_new(self, msg):
      """
      Retrieves current top 5 new links for a subreddit
      """
      subreddit = self.r.get_subreddit(msg.clean_contents.strip())
      if subreddit:
        for submission in subreddit.get_new(limit=5):
          msg.reply("[{score}] {title} ({url})".format(score=submission.score, title=submission.title, url=submission.permalink).encode("utf-8"))
      return None;

    def sub_hot(self, msg):
      """
      Retrieves current top 3 hot links for a subreddit
      """
      subreddit = self.r.get_subreddit(msg.clean_contents.strip())
      if subreddit:
        for submission in subreddit.get_hot(limit=5):
          msg.reply("[{score}] {title} ({url})".format(score=submission.score, title=submission.title, url=submission.permalink))
      return None;

    def sub_top(self, msg):
      """
      Retrieves current top 3 links for a subreddit
      """
      subreddit = self.r.get_subreddit(msg.clean_contents.strip())
      if subreddit:
        for submission in subreddit.get_top(limit=5):
          msg.reply("[{score}] {title} ({url})".format(score=submission.score, title=submission.title, url=submission.permalink))
      return None;

    def raw(self, msg, channel, reply_handle):
        """ If msg contains a URL, fetch the title and return it as a fancy string """
        print("Scanning {}".format(msg))
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', msg)
        if len(urls):
          soup = BeautifulSoup(urllib.urlopen(urls[0]))
          print("Scanned for URLs. Match: {}".format(urls[0]))
          reply_handle.msg(channel, "\x02Title: \x02" + soup.title.string.encode('utf-8'))
          return
        return None
        print("Scanned for URLs. No match.")
