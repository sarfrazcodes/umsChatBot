class ConversationContext:
    """
    Maintains basic conversation state to handle follow-up questions.
    """
    def __init__(self):
        self.last_intent = None
        self.last_subject = None
        self.last_date = None
        
    def update(self, intent, entities):
        if intent and intent != "UNKNOWN":
            self.last_intent = intent
            
        if 'subject' in entities:
            self.last_subject = entities['subject']
            
        if 'date' in entities:
            self.last_date = entities['date']

    def clear(self):
        self.last_intent = None
        self.last_subject = None
        self.last_date = None
        
    def get_context(self):
        return {
            "intent": self.last_intent,
            "subject": self.last_subject,
            "date": self.last_date
        }
