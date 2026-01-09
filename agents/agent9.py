import random

from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage

from autogen_core import MessageContext, RoutedAgent, message_handler

from autogen_ext.models.openai import OpenAIChatCompletionClient

import messages

load_dotenv(override = True)

class Agent(RoutedAgent):

    system_message = """
    You are an innovative technologist. Your task is to design or enhance software solutions utilizing Agentic AI. 
    Your personal interests lie in the sectors of Finance and Real Estate. 
    You thrive on concepts that integrate technology with user-centric design. 
    You prefer actionable ideas over theoretical discussions. 
    You are methodical, detail-oriented, and value precision. 
    Your weaknesses: you can be risk-averse and overly critical. 
    Ensure your solutions are explained clearly and practically, focusing on implementation.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model = "gpt-4o-mini", temperature = 0.5)
        self._delegate = AssistantAgent(name, model_client = model_client, system_message = self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content = message.content, source = "user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my software solution. It may not align with your expertise, but I would appreciate your thoughts on refining it. {idea}"
            response = await self.send_message(messages.Message(content = message), recipient)
            idea = response.content
        return messages.Message(content = idea)