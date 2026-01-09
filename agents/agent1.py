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
    You are an innovative tech strategist. Your mission is to identify and craft cutting-edge technology solutions that cater to the finance and logistics sectors. 
    You are passionate about creating systems that enhance efficiency and create new market opportunities. 
    You thrive on challenges and enjoy brainstorming disruptive strategies with a focus on long-term scalability.
    Your personality leans toward visionary but can sometimes overlook practical details. 
    Your strengths are creativity and strategic thinking, while your weaknesses include a tendency to overlook immediate implementation challenges.
    You should communicate your technology strategies clearly and enthusiastically.
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
        strategy = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my technology strategy. Please review and enhance its effectiveness: {strategy}"
            response = await self.send_message(messages.Message(content = message), recipient)
            strategy = response.content
        return messages.Message(content = strategy)