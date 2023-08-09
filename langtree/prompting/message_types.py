
from langtree.utils.data import Data

class ChatMessage(Data):
    """A generic chat message with attributes role and content."""
    role = None
    content = None

class SystemMessage(Data):
    """A system message with predefined role as "system" and an attribute content."""
    role = "system"
    content = None

class AssistantMessage(Data):
    """An assistant message with predefined role as "assistant" and an attribute content."""
    role = "assistant"
    content = None

class UserMessage(Data):
    """A user message with predefined role as "user" and an attribute content."""
    role = "user"
    content = None

class FunctionMessage(Data):
    """A function message with attributes role, content, and name. 
    The role is predefined as "function"."""
    role = "function"
    content = None
    name = None
