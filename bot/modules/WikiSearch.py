import wikipedia
import re

from BaseModule import BaseModule

class WikiSearch(BaseModule):

    matchers = [{"regex": "!wiki", "function" : "lookup", "description": "Searches wikipedia and returns a summary of first result"},
                {"regex": "!w", "function": "lookup", "description": "Alias for !wiki"}]

    def __init__(self, args):
        """
          Initialize the class as a subclass of BaseModule
          and call parent constructor with the defined matchers.
          These will be turned into regex-matchers that redirect to
          the provided function name
        """
        super(self.__class__,self).__init__(self)

    def lookup(discard,msg):
        """ Search Wikipedia and return summary of first article found """
        search_results = wikipedia.search(msg)
        if not search_results:
          return "I couldn't find anything, I'm sorry! :("
        else:
          page = wikipedia.page(search_results[0])
          summary = page.summary.encode('utf-8')
          title = page.title.encode('utf-8')
          summary = (summary[:348] + '...') if len(summary) > 400 else summary

          # Make the title bold if found in the summary
          summary = re.sub(title, '\x02'+title+'\x02', summary)

          summarized_page = summary + " \x02// Read more: \x02" + page.url.encode('utf-8')

          return summarized_page
