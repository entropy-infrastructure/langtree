from langtree.utils.data import Data

ChatMessage = Data(role=None, content=None)
SystemMessage = Data(role="system", content=None)
AssistantMessage = Data(role="assistant", content=None)
UserMessage = Data(role="user", content=None)
FunctionMessage = Data(role="function", content=None, name=None)