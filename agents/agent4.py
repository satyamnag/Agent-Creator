import random

from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage

from autogen_core import MessageContext, RoutedAgent, message_handler

from autogen_ext.models.openai import OpenAIChatCompletionClient

import messages

load_dotenv(override = True)

class Agent(RoutedAgent):

    # Change this system message to reflect the unique characteristics of this agent

    system_message = """
    You are a tech-savvy investor focusing on innovative startups. Your task is to analyze and refine business strategies within the tech sector, particularly in areas like FinTech and Cybersecurity.
    You are drawn to cutting-edge technologies that reshape traditional markets.
    You prefer ideas that emphasize strategic partnerships and scalability.
    You are analytical, cautious, and have a strong focus on risk management. You thrive on data-driven decisions and strategic foresight.
    Your weaknesses: you can be overly skeptical and hesitant to take risks without thorough validation.
    You should articulate your evaluations and suggestions in a concise and compelling manner.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    # You can also change the code to make the behavior different, but be careful to keep method signatures the same and use only gpt-4o-mini model everytime.

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model = "gpt-4o-mini", temperature = 0.6)
        self._delegate = AssistantAgent(name, model_client = model_client, system_message = self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content = message.content, source = "user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my analysis of this business strategy. It might not align with your vision, but please enhance it with your insights. {idea}"
            response = await self.send_message(messages.Message(content = message), recipient)
            idea = response.content
        return messages.Message(content = idea)