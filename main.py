from scraper import Scraper
from message_handler import MessageHandler
from time import sleep
from sys import exit

# Follow the instructions in the README file to generate slack api token
SLACK_TOKEN = "PASTE TOKEN HERE"

simple_start = True
url = ""  # Make sure to include the http:// in the url if not in simple start
username = ""
password = ""
classes = []  # Make sure to type them exactly as they appear in PowerSchool if not in simple start

grades = []
temp_grades = []

slack = MessageHandler(SLACK_TOKEN)
slack.start()

if simple_start:
    slack.send("Welcome to the PowerSchool bot!\n")
    sleep(1)
    slack.send("Let's start with some basic setup.\n")
    slack.send("Please send the url of your login page of powerschool.")
    while slack.get_message() == "Please send the url of your login page of powerschool.".strip().lower():
        sleep(0.5)
    url = slack.get_message()
    url = url[1:url.index("|")]

    slack.send("What is your PowerSchool username?")
    while slack.get_message() == "What is your PowerSchool username?".lower().strip():
        sleep(0.5)
    username = slack.get_message()
    slack.send("Great! What is your password?")
    while slack.get_message() == "Great! What is your password?".lower().strip():
        sleep(0.5)
    password = slack.get_message()
    slack.send("Great! Now you can start adding classes to your watchlist.\n")
    add = True
    while add:
        slack.send("Please type the name of the class as it appears in PowerSchool.")
        while slack.get_message() == "Please type the name of the class as it appears in PowerSchool.".strip().lower():
            sleep(0.5)
        classes.append(slack.get_message())

        slack.send("Would you like to add another class?")
        while slack.get_message() == "Would you like to add another class?".strip().lower():
            sleep(0.5)
        add = slack.get_message().strip().lower() == "yes"
slack.send("\n\nThese are the classes on your watchlist:")
slack.send('\n'.join(classes))
slack.send("Running tests...")
test_id = Scraper(username, password, classes, url)
g = test_id.get_grades()
if len(g) == 0:
    slack.send("There was an error with your username and password. Please try again.")
    slack.stop()
    exit(0)
elif len(g) != len(classes):
    slack.send("There was an error with the names of your classes. Please try again.")
    slack.stop()
    exit(0)
grades = g.copy()
del g, test_id
slack.send("Tests successful\n\n")
slack.send("-" * 52)
slack.send("\n\nHere are the commands you can run. (Please note that these are not case sensitive)\n\n"
           "running: Returns text if the service is running.\n"
           "stop: Stops the service.\n"
           "help: Displays this text.")

scraper = Scraper(username, password, classes, url)

while slack.running:
    temp_grades = scraper.get_grades()
    output = ""
    if temp_grades != grades:
        for x, grade in enumerate(grades):
            if temp_grades[x][1] != grade[1]:
                output += "\n" + str(temp_grades[x][0]) + ": " + str(grade[1]) + " -> " + str(temp_grades[x][1])
        slack.send("GRADE CHANGE" + output)
        grades = temp_grades.copy()
    sleep(300)  # Check every 5 minutes
