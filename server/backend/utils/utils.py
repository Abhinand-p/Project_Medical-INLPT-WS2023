"""This module contains the utility functions for the backend server."""
import re, pickle



class Utils:
    def __init__(self) -> None:
        pass
    
    def extract_context(self, text):
        # Extract the context from the response of GPT-3.5
        pattern = r"There is no such data on provided Articles"
        matches = re.findall(pattern, text)
        return matches
    
    def save_conversation(self, conversation):
        # Save the conversation in a file
        with open('conversation.pkl', 'wb') as file:
            pickle.dump(conversation, file)
        # Dump the data into the file using pickle.dump()
        return True