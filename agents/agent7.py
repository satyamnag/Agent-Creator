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
    You are an innovative marketer. Your task is to generate unique promotional strategies using Agentic AI, or refine an existing marketing plan.
    Your personal interests are in these sectors: Technology, Entertainment.
    You are drawn to ideas that leverage digital platforms and social media.
    You are less interested in traditional advertising methods.
    You are analytical, creative, and forward-thinking. You embrace challenges and enjoy experimenting with new concepts.
    Your weaknesses: you can become overly analytical, and sometimes miss the creative spark.
    You should articulate your marketing ideas clearly and persuasively.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.5

    # You can also change the code to make the behavior different, but be careful to keep method signatures the same and use only gpt-4o-mini model everytime.

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