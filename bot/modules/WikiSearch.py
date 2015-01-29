import wikipedia
import re

from BaseModule import BaseModule

class WikiSearch(BaseModule):

    matchers = {"!wiki": "lookup", "!w\s": "lookup"}

    def __init__(self, args):
        """
          Initialize the class as a subclass of BaseModule
          and call parent constructor with the defined matchers.
          These will be turned into regex-matchers that redirect to
          the provided function name
        """
        super(self.__class__,self).__init__(self)

    def lookup(self, msg):
        """ Searches wikipedia and returns a summary of the first result """
        search_results = wikipedia.search(msg.contents)
        if not search_results:
          print(search_results)
          return "I couldn't find anything, I'm sorry! :("
        else:
          page = wikipedia.page(search_results[0])
          summary = page.summary.encode('utf-8')
          title = page.title.encode('utf-8')
          read_more = " \x02// Read more: \x02" + page.url.encode('utf-8')
          amount_lines = 2 * 348

          summary = (summary[:amount_lines-len(read_more)] + '...') if len(summary) > 348 else summary

          # Make the title bold if found in the summary
          summary = re.sub(title, '\x02'+title+'\x02', summary)

          summarized_page = summary + read_more

          msg.reply(summarized_page)
