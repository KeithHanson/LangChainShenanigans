import os

from dotenv import load_dotenv
load_dotenv()

from mmpy_bot import Plugin, listen_to
from mmpy_bot import Message

from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
from langchain.agents import AgentType

SERPAPI_API_KEY = os.environ["SERPAPI_API_KEY"]

search = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)
tools = [
    Tool(
        name = "Current Search",
        func=search.run,
        description="useful for when you need to answer questions about current events or the current state of the world. the input to this should be a single search term."
    ),
]

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

llm=ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0)

agent_chain = initialize_agent(tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)


class Default(Plugin):
    @listen_to("(.*?)")
    async def everything(self, message: Message):
        #self.driver.reply_to(message, message.text)
        #self.driver.create_post(message.channel_id, "Hai!")
        if message.text.startswith("#"):
            return

        self.driver.create_post(message.channel_id, "_relaying to langchain_")
        output = agent_chain.run(input=message.text)
        self.driver.create_post(message.channel_id, output)


