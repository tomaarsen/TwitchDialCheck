# TwitchDialCheck
Twitch Bot to detect and rate DIAL-in checks.

---
# Note
This Bot was written for one streamer in particular, which means this script likely will not be useful to anyone else, but people interested in checking out how I use my [TwitchWebsocket](https://github.com/CubieDev/TwitchWebsocket) library.

---
# Functionality
This Bot will read Twitch chat looking for messages such as "Dial", "dangDial", "D I A L", and so forth.
Ten seconds after the most recent of these messages the bot will output a "Dial Percentage" based on this formula:

`trues = amount of DIAL messages`<br>
`ratio = trues / total messages found in the span`<br>
`percentage = trues / (amount of current viewers / 1.5) * 100`<br>
`result = min(percentage * ratio * 10 * 0.9 + 10 + random.uniform(-1, 1), 100)`

In short, it's a linear formula based on the percentage of chat that was involved in the messages, and the ratio of DIAL messages relative to other messages, ranging from 10% to 100%.

---

# Settings
This bot is controlled by a settings.txt file, which looks like:
```
{
    "Host": "irc.chat.twitch.tv",
    "Port": 6667,
    "Channel": "#<channel>",
    "Nickname": "<name>",
    "Authentication": "oauth:<auth>"
}
```

| **Parameter**        | **Meaning** | **Example** |
| -------------------- | ----------- | ----------- |
| Host                 | The URL that will be used. Do not change.                         | "irc.chat.twitch.tv" |
| Port                 | The Port that will be used. Do not change.                        | 6667 |
| Channel              | The Channel that will be connected to.                            | "#CubieDev" |
| Nickname             | The Username of the bot account.                                  | "CubieB0T" |
| Authentication       | The OAuth token for the bot account.                              | "oauth:pivogip8ybletucqdz4pkhag6itbax" |

*Note that the example OAuth token is not an actual token, but merely a generated string to give an indication what it might look like.*

I got my real OAuth token from https://twitchapps.com/tmi/.

---

# Other Twitch Bots

* [TwitchGoogleTranslate](https://github.com/CubieDev/TwitchGoogleTranslate)
* [TwitchMarkovChain](https://github.com/CubieDev/TwitchMarkovChain)
* [TwitchRhymeBot](https://github.com/CubieDev/TwitchRhymeBot)
* [TwitchCubieBotGUI](https://github.com/CubieDev/TwitchCubieBotGUI)
* [TwitchCubieBot](https://github.com/CubieDev/TwitchCubieBot)
* [TwitchDeathCounter](https://github.com/CubieDev/TwitchDeathCounter)
* [TwitchSuggestDinner](https://github.com/CubieDev/TwitchSuggestDinner)
* [TwitchPickUser](https://github.com/CubieDev/TwitchPickUser)
* [TwitchSaveMessages](https://github.com/CubieDev/TwitchSaveMessages)
* [TwitchPackCounter](https://github.com/CubieDev/TwitchPackCounter) (Streamer specific bot)
* [TwitchSendMessage](https://github.com/CubieDev/TwitchSendMessage) (Not designed for non-programmers)
