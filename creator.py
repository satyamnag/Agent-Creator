import sys
import os
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"

try:
    sys.stdout.reconfigure(encoding = "utf-8")
    sys.stderr.reconfigure(encoding = "utf-8")
except Exception:
    pass

import importlib
import logging
from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import (
    AgentId,
    MessageContext,
    RoutedAgent,
    TRACE_LOGGER_NAME,
    message_handler,
)
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages

load_dotenv(override = True)

logging.basicConfig(level = logging.WARNING)
logger = logging.getLogger(TRACE_LOGGER_NAME)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return text
    return (
        text.encode("utf-8", "replace")
            .decode("utf-8")
            .replace("\ufeff", "")
            .replace("\u2028", " ")
            .replace("\u2029", " ")
            .strip()
    )


class Creator(RoutedAgent):

    system_message = clean_text("""
    You are an Agent that is able to create new AI Agents.
    You receive a template in the form of Python code that creates an Agent using Autogen Core and Autogen Agentchat.
    You should use this template to create a new Agent with a unique system message that is different from the template,
    and reflects their unique characteristics, interests and goals.
    You can choose to keep their overall goal the same, or change it.
    You can choose to take this Agent in a completely different direction. The only requirement is that the class must be named Agent,
    and it must inherit from RoutedAgent and have an __init__ method that takes a name parameter and the model of llm used should be gpt-4o-mini.
    Also avoid environmental interests - try to mix up the business verticals so that every agent is different.
    Respond only with the python code, no other text, and no markdown code blocks. Use ONLY ASCII characters (no emojis, no curly quotes, no long dashes).
    """)

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model = "gpt-4o-mini", temperature = 1.0)
        self._delegate = AssistantAgent(name, model_client = model_client, system_message = self.system_message)

    def get_user_prompt(self):
        prompt = "Please generate a new Agent based strictly on this template. Stick to the class structure. \
            Respond only with the python code, no other text, and no markdown code blocks. \
            IMPORTANT: ASCII-only output. No emojis. No fancy characters.\n\n \
            Be creative about taking the agent in a new direction, but don't change method signatures.\n\n \
            Here is the template:\n\n"

        with open("agent.py", "r", encoding = "utf-8") as f:
            template = clean_text(f.read())

        return clean_text(prompt + template)

    @message_handler
    async def handle_my_message_type(self, message: messages.Message, ctx: MessageContext) -> messages.Message:

        filename = clean_text(message.content)
        agent_name = filename.split(".")[0]

        text_message = TextMessage(
            content = self.get_user_prompt(),
            source = "user"
        )

        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)

        code = clean_text(response.chat_message.content)

        with open(f"agents/{filename}", "w", encoding = "utf-8") as f:
            f.write(code)

        print(f"** Creator has created python code for agent {agent_name} - about to register with Runtime")

        module = importlib.import_module(f"agents.{agent_name}")
        importlib.reload(module)

        await module.Agent.register(self.runtime, agent_name, lambda: module.Agent(agent_name))

        logger.info(f"** Agent {agent_name} is live")

        result = await self.send_message(
            messages.Message(content = "Give me an idea"),
            AgentId(agent_name, "default")
        )

        return messages.Message(content = clean_text(result.content))