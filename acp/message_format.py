# acp/message_format.py

def create_message(sender, receiver, intent, content):
    return {
        "sender": sender,
        "receiver": receiver,
        "intent": intent,
        "content": content
    }
