# cli-chat
A simple command line chat program for linux and windows written in python  
It runs on Window and Linux on both Python 2 and 3

The messages are stored on: http://waksmemes.x10host.com/mess/  
  
## Usage:  
### Entering chat rooms:  
To start chatting in the main chat room:  
`python chat.py`  
  
To start chatting in a chat room called "different_chat_room":  
`python chat.py different_chat_room`
  
### Sending messages  
After all a chat room's messages are printed a '> ' symbol is printed. This final line of text is called the _input line_.
To send a message simply type your message on the input line and press enter.  
If the user presses enter without typing a message, no message is sent.  
Likewise, when a user issues a command, no message is sent.  

### Reading messages
New messages are fetched every time the user presses enter on the input line, regardless of whether or not they sent a message  
To automatically reload the chat (fetch messages without having to press enter) you can start the script in _auto-reloading read-only mode_.  
  
To start in auto-reloading read-only mode:  
`python chat.py -r`
  
To start in auto-reloading read-only mode in a chat room called "different_chat_room":  
`python chat.py -r different_chat_room`

### Commands  
Commands begin with a backslash (\) and are issued on the input line in a similar fashion to shell commands. Commands can take any number of arguments.  
#### The set command
set is used to configure your user settings. User settings are saved in a local configuration file that is automatically generated when the set command is used. These settings are sent along with every message you send so that other clients can use them.
  
Usage:  
`\set setting value`

Types of settings:  

|Setting name | Purpose                                                                                                      |
| ----------- |:------------------------------------------------------------------------------------------------------------:|
| name        | Sets your name so you're no longer identified by your IP                                                     |
| color       | Sets the color of your name. The only possible colors so far are red, green, purple, blue, yellow and cyan   |

#### The key command
key is used to encrypt your messages in the current room with a specified key. Any other users in the same room with the same key can decrypt the messages that you send with that key.  
  
Usage:  
`\key secret_key`
  
Once you set your key you can switch to a different key by using the key command agian, however you can only save one key per room at any one time. Using the key command without specifying a key will remove your key for that room, causing all your messages to be unencrypted until you set a new key.  
  
Encrypted messages contain a red colon after the name of the sender instead of the usual white (or whatever your default terminal color is) colon. This is so that users can easily distinguish between encrypted and unencrypted messages.  
  
#### Other commands  

|Command name | Args                | Explanation                                             | Example           |
| ----------- |:-------------------:|:-------------------------------------------------------:|:------------------:
| room        | (1) roomname        | Switches the room to _roomname_                         | \room other_room  |
| read        | (0) No arguments    | Swithces into auto-reloading read-only mode             | \read             |
| flush       | (1) m (optional)    | Spams the room with _m_ messages, Defaults to _m_ = 300 | \flush 100        |
| nokey       | (1) message         | Sends _message_ with no encryption                      | \nokey hello world|
