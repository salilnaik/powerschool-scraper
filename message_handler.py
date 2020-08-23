import slack
from threading import Thread
import time


class MessageHandler:
    def __init__(self, token, channel="#general"):
        self.slack_token = token
        self.client = slack.WebClient(token=self.slack_token)
        self.latest_message = ""
        self.channel = channel
        for ch in self.client.conversations_list()['channels']:
            if ch['is_general']:
                self.id = ch['id']
                break
        self.running = True

    # Send a message to the general channel
    def send(self, message):
        response = self.client.chat_postMessage(
            channel=self.channel,
            text=message)

    def get_message(self):
        messages = self.client.conversations_history(channel=self.id, limit=1)
        if "subtype" not in messages['messages']:
            return messages['messages'][0]['text'].lower()

    def recv(self):
        while True:
            messages = self.client.conversations_history(channel=self.id, limit=1)
            if "subtype" not in messages['messages'] and messages['messages'][0]['ts'] != self.latest_message:
                self.latest_message = messages['messages'][0]['ts']
                if messages['messages'][0]['text'].lower() == 'running':
                    self.send("\nI am running")
                if messages['messages'][0]['text'].lower() == 'help':
                    self.send("\nList of Commands: (not case sensitive)\n\n"
                              "running: Returns text if the service is running.\n"
                              "stop: Stops the service.\n"
                              "help: Displays this text.")
                if messages['messages'][0]['text'].lower() == 'stop':
                    self.send("\nAre you sure?")
                    time.sleep(10)
                    messages = self.client.conversations_history(channel=self.id, limit=1)
                    if messages['messages'][0]['text'].lower() == 'yes':
                        self.send("\nStopping...")
                        self.stop()
                    else:
                        self.send("\nTimed out.")
            if not self.running:
                break
            time.sleep(1)

    def stop(self):
        self.running = False

    def start(self):
        thread = Thread(target=self.recv)
        # thread.daemon = True
        thread.start()
