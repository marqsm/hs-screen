import re

class ZulipRequestHandler:
    def __init__(self, zulipClient, username, text_renderer, image_renderer):
        self.SCREEN_SIZE = screenSize
        self.USERNAME = username
        # If string starts with "@led-bot" or "led-bot"
        self.BOT_MSG_PREFIX = '^(\\@\\*\\*)*led-bot(\\*\\*)*'
        self.zulipClient = zulipClient
        self.text_renderer = text_renderer
        self.image_renderer = image_renderer
        return None
	
    def __handle_error_message(self, msg, msgToken):
        self.send_response(self.get_response(msg, "syntaxError"))
        # Do we need to do something here?
        return None;
	
    def __handle_text_message(self, msg, msgToken):
        print "getMsgQueueToken text"
        return self.text_renderer.get_queue_token(msgToken)
	
    def __handle_image_message(self, msg, msgToken):
        print "getMsgQueueToken image"
        queue_token = self.image_renderer.get_queue_token(msgToken)
        print("This is what I got from ImageRenderer")
        print(queue_token)
        return queue_token
      
    message_handler_dispatcher = {
        'error': __handle_error_message,
        'text' : __handle_text_message,
        'image': __handle_image_message,
    }
	
    # Main function, this is what gets passed to the actual Zulip Client
    def get_msg_queue_token(self, msg):
        
        # Do stuff
        if not self.is_bot_message(msg):
          	return None
        
        print("is Bot message")
        msgToken = self.tokenize_message(msg)
        
        # use dispatcher to handle the message
        queue_token = message_handler_dispatcher.get(msgToken['type'],'error')(msg, msgToken)
        
        # if queue item valid, send response to user
        if queue_token["valid"]:
            self.send_response(self.get_response(msg))
            return queue_token
        
        self.send_response( self.get_response(msg, "unknownError"))
        return None


    # Sends the zulip user who sent the message a response
    # either an "ok" or an error-message
    def send_response(self, response):
        self.zulipClient.send_message(response)
        return None

    token_formats = {
      'show-image': lambda url: { 'type':'image','url': url[0] },
      'show-text': lambda text: { 'type':'text','text': text },
      'error': lambda dummy: { 'type':'error' }
    }
    def tokenize_message(self, msg):
        arr = re.sub(self.BOT_MSG_PREFIX, '', msg["content"]).split()
        
        token = token_formats.get(arr[0],'error')(arr[1:])
        
        print('tokenize_message: ', token)
        
        return token

    def get_msg_to(self, msg):
        if msg["type"] == "stream":
            # user message was public
            return msg["display_recipient"]    # name of the stream
        if msg["type"] == "private":
            # message sent by user is a private stream message
            return msg["sender_email"]
        return None

    # get_response :: create response to message sender
    #   - ok-message
    #   - error-message
    #       - invalid syntax - explain how to use
    #       - Image load failed
    #       - WTF (aka "Something broke, I don't know what")
    statuses = {
      'ok': """JUST GIVE ME A SEC I'LL SHOW YOUR STUFF WHEN I CAN!
                         WE'RE ALL UNDER A LOT OF PRESSURE HERE!!!""",
      'syntaxError':  """I don't know what that is.. you could try sending me
                          led-bot show-image http://www.example.com/cat.gif
                          led-bot show-text whatever you want to say""",
      'imageLoadError': """WHAT KIND OF IMAGES ARE YOU TRYING TO SEND ME
                         I DONT KNOW WHAT THAT STUFF IS!! """,
      'unknownError': """ WTF WAS THAT SOMETHING BROKE
                          AND I HAVE NO IDEA WHAT IT WAS!""",
      'default': "Yeah, this default message should never be reached.."
    }
    
    def get_response(self, msg, status="ok"):
        return {
            "type": msg["type"],
            # topic within the stream
            "subject": msg["subject"],           
            # name of the stream
            "to": self.get_msg_to(msg),      
            # message to print to stream
            "content": "%s" % statuses.get(status,'default')        
        }

    # Checks if message is meant for the bot
    def is_bot_message(self, msg):
        return (msg["sender_email"] != self.USERNAME 
                and re.match(self.BOT_MSG_PREFIX, msg["content"], flags=re.I or re.X))

