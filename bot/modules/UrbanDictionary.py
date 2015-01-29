import urllib
from bs4 import BeautifulSoup
from BaseModule import BaseModule

class UrbanDictionary(BaseModule):

    matchers = { "!ud": "lookup" }

    def __init__(self, args):
        """
          Initialize the class as a subclass of BaseModule
          and call parent constructor with the defined matchers.
          These will be turned into regex-matchers that redirect to
          the provided function name
        """
        super(self.__class__,self).__init__(self)

    def lookup(self,msg):
        """ Looks up a term on UrbanDictionary """
        page = urllib.urlopen("http://www.urbandictionary.com/define.php?term=%s" % msg.clean_contents)

        try:
          soup = BeautifulSoup(page.read())
          title = "\x02" + soup.find('div', {'id': 'content'}).findChild('div', {'class': 'def-header'}).findChild('a', {'class': 'word'}).text.encode('utf-8').strip() + "\x02"
          meaning = soup.find('div', {'id': 'content'}).findChild('div', {'class': 'meaning'}).text.encode('utf-8').strip()
          example = "\x03" + soup.find('div', {'id': 'content'}).findChild('div', {'class': 'example'}).text.encode('utf-8').strip('\t\n\r') + "\x03"

          response = title + ": " + meaning + "\n\x02Example:\x02 " + example
          msg.reply(response)
        except Exception, e:
          raise Exception(e)

        return msg
