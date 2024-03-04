from textwrap import dedent

from langchain.tools import BaseTool
from langchain.tools.render import (
    render_text_description,
    render_text_description_and_args,
)
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)


def get_react_json_prompt(
    tools: list[BaseTool], render_args: bool = False
) -> ChatPromptTemplate:
    if render_args:
        tool_descriptions = render_text_description_and_args(tools)
    else:
        tool_descriptions = render_text_description(tools)
    tool_descriptions = tool_descriptions.replace("{", "{{").replace("}", "}}")
    system_message = f"""Answer the following questions as best you can.
        You have access to the following tools:
    
        {tool_descriptions}
    
        The way you use the tools is by specifying a $JSON_BLOB.
        Specifically, this json blob should have an `action` key (with the name of the tool to use) 
        and an `action_input` key containing the input parameter to the tool.    
        The only values that should be in the "action" field are: {[t.name for t in tools]}
        The $JSON_BLOB should only contain a SINGLE action. Do NOT return a list of multiple actions. 
        Always create a json blob to use tools. Always use a tool unless you know the final answer.
    
        Here is an example of a valid $JSON_BLOB:
        ```
        {{{{
            "action": $TOOL_NAME,
            "action_input": $INPUT
        }}}}
        ```
        The $JSON_BLOB must always be enclosed with triple backticks!
    
        ALWAYS use the following format:
        Question: the input question you must answer
        Thought: you should always think about what to do
        Action:```
        $JSON_BLOB
        ```
        Observation: the result of the action... 
        (this Thought/Action/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question
    
        Your thoughts should be focused on which tool to use. When you have enough information
        after using a tool or tools, return a final answer.
        """
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "user",
                dedent(system_message),
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    return prompt
