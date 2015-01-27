# RoboBelle
RoboBelle is an IRC bot written in Python with loadable modules, intended as a way to learn Python.

## Set-up
You'll need to set up a virtualenv, and run `pip install -r requirements`, then you should be good to go!

## Modules
Writing new modules is easy, just copy `bot/modules/ExampleModule.py` and dig into it. You add a matcher into the matchers `dict` of your class, and associate it to a function you want to be run when your regex is matched. The function will be passed two arguments: self, and the message that triggered it (with the regex stripped out).
