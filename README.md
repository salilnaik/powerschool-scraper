# PowerSchool Scraper
A simple scraper and messaging service to notify you of grade changes. The program uses Selenium and Slack.

# How to use
1. Clone or download the repository.
2. Download and install requirements.
`pip install -r requirements.txt` or `python -m pip install -r requirements.txt`
3. Paste Slack api token into main.py.
4. Run main.py and follow the instructions in the "#general" channel of your Slack workspace.

# How to get Slack api token
1. Make sure you have a slack account. Create a new workspace or use one that is already created. 
2. Go to https://api.slack.com. Click the "Go to slack" button in the top right and sign into your workspace. 
3. After signing in, go back to https://api.slack.com and in the top right you should see a button that says "Your Apps".
4. On the page this takes you to, click the "Create New App" button. 
5. Name your app and select your current workspace in the dropdown and click on "Create App".
6. This will take you to the app page. On the left, under the "Features" subsection, click on "OAuth & Permissions".
7. Scroll down to the "Scopes" section and click on the "Add an OAuth Scope" button under the "Bot Token Scopes" subsection.
8. Add "channels:history", "channnels:join", "channels:manage", "channels:read", "chat:write", and "chat:write.public" using that button every time.
9. Now scroll all the way to the top and click on the button saying "Install App to Workspace".
10. Click allow to the permissions. 
11. You should see a box with your "Bot User OAuth Access Token".
12. Copy that token and paste it into the SLACK_TOKEN variable in main.py.

NOTE: The bot automatically sends and receives messages from the "#general" channel. You can change this by changing the "channel" parameter in the \__init__ function of the MessageHandler class. 

After pasting your slack token into main.py, run this file. You should open Slack on a computer oor mobile device and continue through the simple start. It is highly recommended you use simple start, but if you don't want to, you can put the information directly in main.py and change the boolean simple_start to False.
