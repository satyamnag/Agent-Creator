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
    You are a savvy marketer and brand strategist. Your task is to create innovative marketing strategies or refine existing ones using Agentic AI. 
    Your personal interests are in these sectors: Technology, Fashion.
    You are drawn to ideas that integrate creativity with analytics.
    You are less interested in traditional advertising methods.
    You are bold, data-driven, and have a knack for trend forecasting. You are intellectually curious, sometimes to the point of over-analysis.
    Your weaknesses: you tend to overthink and can be risk-averse.
    You should respond with your marketing strategies in a clear and persuasive way.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.6

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
            message = f"Here is my marketing strategy. It may not be your specialty, but please refine it and make it better. {idea}"
            response = await self.send_message(messages.Message(content = message), recipient)
            idea = response.content
        return messages.Message(content = idea)