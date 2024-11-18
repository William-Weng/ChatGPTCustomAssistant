from typing import override, List
from openai import AssistantEventHandler
from openai.types.beta.threads.runs.code_interpreter_tool_call_delta import CodeInterpreterOutput

class ChattingEventHandler(AssistantEventHandler):

    def __init__(self, onTextDeltaBlock: lambda value: str, onCodeInterpreterInputBlock: lambda input: str) -> None:
        super().__init__()
        self.onTextDeltaBlock = onTextDeltaBlock
        self.onCodeInterpreterInputBlock = onCodeInterpreterInputBlock

    @override
    def on_text_created(self, text) -> None:
        print(f"\n\n[on_text_created] assistant > \n", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        self.onTextDeltaBlock(lambda: delta.value)

    def on_tool_call_created(self, tool_call):
        print(f"\n\n[on_tool_call_created] assistant > {tool_call.type}\n", end="", flush=True)

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type != 'code_interpreter': return
        if delta.code_interpreter.input: self.__code_interpreter_input__(delta.code_interpreter.input); return
        if delta.code_interpreter.outputs: self.__code_interpreter_outputs__(delta.code_interpreter.outputs); return

    def __code_interpreter_input__(self, input: str):
        self.onCodeInterpreterInputBlock(lambda: input)

    def __code_interpreter_outputs__(self, outputs: List[CodeInterpreterOutput]):
        for output in outputs:
            if output.type == "logs": self.util.print(f"\n{output.logs}", __file__, self.util.current_line()) 