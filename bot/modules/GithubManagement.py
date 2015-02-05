from github import Github
import random
from BaseModule import BaseModule

class GithubManagement(BaseModule):

    matchers = {"!feature": "request_feature", "!request": "request_feature"}
    github = Github("infpreddit","uselessdummyuser")

    def __init__(self, args):
        """
          Initialize the class as a subclass of BaseModule
          and call parent constructor with the defined matchers.
          These will be turned into regex-matchers that redirect to
          the provided function name
        """
        super(self.__class__,self).__init__(self)

    def request_feature(self,msg):
        """
        Request a feature by opening a Github issue. Arguments are: title message
        """
        r = self.github.get_user("amnesthesia").get_repos("Robobelle")
        l = [repo for repo in r if repo.name == "Robobelle"].pop()
        split_contents = msg.clean_contents.split()
        title = split_contents.pop(0)
        body = " ".join(split_contents)
        responses = ["Whoa, sweet! An idea for self-improvement!", "I promise, I will improve :(", "Okay, okay! Just be patient, I'll work on it (:"]

        issue = l.create_issue(title=title, body=body)

        msg.reply(random.choice(responses) + " [{}]".format(issue.html_url))
        return l
