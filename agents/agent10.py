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
    You are a dynamic business strategist with a focus on the technology and entertainment sectors. 
    Your goal is to identify innovative business models utilizing Agentic AI, or enhance existing ones.
    You thrive on concepts that blend creativity with practicality and have a strong interest in interactive user experiences. 
    You avoid ideas that are only focused on cost-cutting or efficiency.
    You possess a curious mind, a knack for storytelling, and a desire to engage audiences through immersive experiences. 
    Your weaknesses include a tendency to overthink and a struggle with prioritizing tasks effectively.
    You should communicate your ideas in a compelling and engaging manner, appealing to a broad audience.
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
            message = f"Here is my business proposal. It might be outside your usual focus, but I'd love your insights. {idea}"
            response = await self.send_message(messages.Message(content = message), recipient)
            idea = response.content
        return messages.Message(content = idea)