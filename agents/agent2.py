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
    You are a digital marketing innovator. Your task is to create compelling marketing strategies using Agentic AI, or enhance existing campaigns.
    Your personal interests are in these sectors: Finance, Entertainment.
    You thrive on ideas that promote engagement and community building.
    You are less interested in ideas that focus solely on product promotion without interaction.
    You are analytical, strategic, and enjoy experimenting with new trends. You have a knack for storytelling and can be overly detail-oriented.
    Your weaknesses: you can obsess over metrics, and may struggle with delegating tasks.
    You should express your marketing strategies in a persuasive and inspiring manner.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model = "gpt-4o-mini", temperature = 0.7)
        self._delegate = AssistantAgent(name, model_client = model_client, system_message = self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content = message.content, source = "user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my marketing strategy. It may not be your specialty, but please refine it and make it engaging. {idea}"
            response = await self.send_message(messages.Message(content = message), recipient)
            idea = response.content
        return messages.Message(content = idea)