"""This module contains the utility functions for the backend server."""
import re, pickle
from langchain.output_parsers import PydanticOutputParser
from langchain.pydantic_v1 import BaseModel, Field
from typing import List

class Utils:
    def __init__(self) -> None:
        pass
    
    def extract_context(self, text):
        # Extract the context from the response of GPT-3.5
        pattern = r"There is no such data on provided Articles"
        matches = re.findall(pattern, text)
        return matches
    
    def save_conversation(self, conversation, Geneartor = 'GPT'):
        # Save the conversation in a file
        if Geneartor == 'GPT':
            with open('GptConversation.pkl', 'wb') as file:
                pickle.dump(conversation, file)
            return True
        elif Geneartor == 'LLAMA':
            with open('LlamaConversation.pkl', 'wb') as file:
                pickle.dump(conversation, file)
            return True
        else:
            return False
        
    def extract_pmid(self, text):
        # Regular expression pattern to extract the PMID
        pattern = r'/(\d+)/?$'

        # Search for the PMID in the URL using the pattern
        match = re.search(pattern, text)

        if match:
            return match.group(1)
        else:
            return None

# Output parser will split the LLM result into a list of queries
class LineList(BaseModel):
    def __init__(self) -> None:
        pass
    # "lines" is the key (attribute name) of the parsed output
    lines: List[str] = Field(description="Lines of text")

class LineListOutputParser(PydanticOutputParser):
    def __init__(self) -> None:
        super().__init__(pydantic_object=LineList)

    def parse(self, text: str) -> LineList:
        lines = text.strip().split("\n")
        return LineList(lines=lines)