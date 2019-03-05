
from TwitchWebsocket import TwitchWebsocket
import random, time, json, requests

class Settings:
    def __init__(self, bot):
        try:
            with open("settings.txt", "r") as f:
                settings = f.read()
                data = json.loads(settings)
                bot.setSettings(data['Host'],
                                data['Port'],
                                data['Channel'],
                                data['Nickname'],
                                data['Authentication'],
                                data["TimeAfterLastDial"]
                                )
        except ValueError:
            raise ValueError("Error in settings file.")
        except FileNotFoundError:
            with open('settings.txt', 'w') as f:
                standard_dict = {
                                    "Host": "irc.chat.twitch.tv",
                                    "Port": 6667,
                                    "Channel": "#<channel>",
                                    "Nickname": "<name>",
                                    "Authentication": "oauth:<auth>",
                                    "TimeAfterLastDial": 10
                                }
                f.write(json.dumps(standard_dict, indent=4, separators=(',', ': ')))
                raise ValueError("Please fix your settings.txt file that was just generated.")

class DialCheck:
    def __init__(self):
        # Variables with None are overridden with the Settings class
        self.host = None
        self.port = None
        self.chan = None
        self.nick = None
        self.auth = None
        self.t = None

        # Fill previously initialised variables with data from the settings.txt file
        Settings(self)

        self.track = 0
        self.tracked = []

        # Start the websocket.
        self.ws = TwitchWebsocket(self.host, self.port, self.message_handler, live=False)
        self.ws.login(self.nick, self.auth)
        self.ws.join_channel(self.chan)
        self.ws.add_capability(["membership", "tags", "commands"])

    def setSettings(self, host, port, chan, nick, auth, t):
        self.host = host
        self.port = port
        self.chan = chan.lower()
        self.nick = nick.lower()
        self.auth = auth
        self.t = t

    def isAccepted(self, message):
        # Check if message contains a DIAL message of any kind
        return "D I A L" in message or "dangDial" in message or "dial" in message.lower()

    def message_handler(self, m):
        if m.type == "PRIVMSG":
            # Check if message contains a DIAL message of any kind
            # And update self.track aka time when previous DIAL message occurred 
            if self.isAccepted(m.message):
                self.track = time.time()
            
            # If it's within self.t seconds since the previous DIAL, add True or False to self.tracked
            # Based on if the message is a DIAL message
            if self.track > time.time() - self.t:
                self.tracked.append(self.isAccepted(m.message))
                print(self.tracked)
            
            # If it's been over self.t seconds since the previous DIAL
            elif len(self.tracked):
                # Remove trailing Falses
                for b in reversed(self.tracked):
                    if b:
                        break
                    else:
                        self.tracked.pop(-1)

                # Get amount of true values
                trues = sum([b for b in self.tracked if b])
                
                # Get ratio of messages that is DIAL related
                ratio = trues / len(self.tracked)
                
                # Get percentage of chat that is involved
                percentage = trues / self.current_viewers() * 100
                
                # Get result as a function from 10 to 100
                result = min(percentage * ratio * 10 * 0.9 + 10 + random.uniform(-1, 1), 100)
                
                print(f"Amt of Trues\t: {trues:}\nRatio\t\t: {ratio * 100:.2f}%\nPercentage\t: {percentage:.2f}%")
                # Output dial percentage to chat
                self.ws.send_message(f"Chat is {result:.2f}% dialed.")

                # Reset stored Trues and Falses
                self.tracked = []
    
    def current_viewers(self):
        # Returns amount of current viewers for channel
        i = 0
        while i < 20:
            try:
                # Attempt to get chatter count
                data = requests.get(f"https://tmi.twitch.tv/group/user/{self.chan.replace('#', '')}/chatters").json()
            except Exception as e:
                print(e)
                i += 1
            else:
                print(data["chatter_count"], "chatters")
                # Return amount of chatters divided by 1.5
                # This value seems to provide a decent result
                return data["chatter_count"] / 1.5 if data["chatter_count"] != 0 else 200

if __name__ == "__main__":
    DialCheck()
