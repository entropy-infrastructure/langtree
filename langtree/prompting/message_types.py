
from langtree.utils.data import Data

class ChatMessage(Data):
    """A generic chat message with attributes role and content."""
    role = None
    content = None

    def __init__(self, role=None, content=None):
        super(ChatMessage, self).__init__(role=role, content=content)
        self.content = content


class SystemMessage(ChatMessage):
    """A system message with predefined role as "system" and an attribute content."""
    role = "system"
    content = None

    def __init__(self, content=None):
        super(SystemMessage, self).__init__(role=SystemMessage.role, content=content)
        self.content = content

class AssistantMessage(ChatMessage):
    """An assistant message with predefined role as "assistant" and an attribute content."""
    role = "assistant"
    content = None

    def __init__(self, content=None):
        super(AssistantMessage, self).__init__(role=AssistantMessage.role, content=content)
        self.content = content

class UserMessage(ChatMessage):
    """A user message with predefined role as "user" and an attribute content."""
    role = "user"
    content = None

    def __init__(self, content=None):
        super(UserMessage, self).__init__(role=UserMessage.role, content=content)
        self.content = content

class FunctionMessage(ChatMessage):
    """A function message with attributes role, content, and name. 
    The role is predefined as "function"."""
    role = "function"
    name = None

    def __init__(self, content=None):
        super(FunctionMessage, self).__init__(role=FunctionMessage.role, content=content)
        self.content = content
