
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
        self.host = None
        self.port = None
        self.chan = None
        self.nick = None
        self.auth = None
        self.t = None

        # Fill previously initialised variables with data from the settings.txt file
        Settings(self)

        self.track = 0
        self.tracked = []#[True, False, True, False, False]

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
        return "D I A L" in message or "dangDial" in message or "DIAL" in message

    def message_handler(self, m):
        if m.type == "PRIVMSG":
            if m.message.startswith("!power"):
                self.ws.send_message("The office and studio lost power for the past 24 hours, Dan is setting up the show now. Please enjoy the Tark Squad play, normal shows will resume on Wednesday with the new game, new studio! dangC")

            if self.isAccepted(m.message):
                #print("Dial recorded")
                self.track = time.time()
            
            if self.track > time.time() - self.t:
                self.tracked.append(self.isAccepted(m.message))
                print(self.tracked)
            
            elif len(self.tracked):
                for b in reversed(self.tracked):
                    if b:
                        break
                    else:
                        self.tracked.pop(-1)

                trues = sum([b for b in self.tracked if b])
                
                # Get ratio of messages that is DIAL related
                ratio = trues / len(self.tracked)
                
                # Get percentage of chat that is involved
                percentage = trues / self.current_viewers() * 100
                
                # Get result as a function from 10 to 100
                result = min(percentage * ratio * 10 * 0.9 + 10 + random.uniform(-1, 1), 100)
               
                print(f"Amt of Trues\t: {trues:}\nRatio\t\t: {ratio * 100:.2f}%\nPercentage\t: {percentage:.2f}%")
                self.ws.send_message(f"Chat is {result:.2f}% dialed.")
                self.tracked = []
    
    def current_viewers(self):
        i = 0
        while i < 20:
            try:
                data = requests.get(f"https://tmi.twitch.tv/group/user/{self.chan.replace('#', '')}/chatters").json()
            except Exception as e:
                print(e)
                i += 1
            else:
                # Return + 1 to prevent division by 0
                print(data["chatter_count"], "chatters")
                return data["chatter_count"] / 1.5 if data["chatter_count"] != 0 else 200

if __name__ == "__main__":
    DialCheck()

'''
[True, True, True, True, False, True, True, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, True, False, True, True, False]
500 chatters
Amt of Trues    : 30
Ratio           : 88.24%
Percentage      : 6.00%
Chat is 57.65% dialed.
'''