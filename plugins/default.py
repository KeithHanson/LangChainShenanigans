import os

from dotenv import load_dotenv
load_dotenv()

from mmpy_bot import Plugin, listen_to

from mmpy_bot import Message

from langchain.chains import ConversationChain

from langchain.chat_models import ChatOpenAI

from langchain.embeddings import OpenAIEmbeddings

from langchain.memory import VectorStoreRetrieverMemory

from langchain.vectorstores.pgvector import PGVector, DistanceStrategy

connection_string = PGVector.connection_string_from_db_params(
    driver="psycopg",
    host="localhost",
    port="5432",
    database="langchain",
    user="postgres",
    password="postgresql"
)

llm=ChatOpenAI(temperature=0)
embeddings = OpenAIEmbeddings()


class Default(Plugin):
    @listen_to("(.*?)")
    async def everything(self, message: Message):
        if message.text.startswith("#"):
            return

        if message.user_id == self.driver.user_id:
            return

        vectorstore = PGVector(
            connection_string=connection_string,
            embedding_function=embeddings,
            collection_name=message.channel_id,
            distance_strategy=DistanceStrategy.COSINE
        )

        retriever = vectorstore.as_retriever()

        memory = VectorStoreRetrieverMemory(retriever=retriever)

        agent_chain = ConversationChain(
            llm=llm,
            memory=memory,
            verbose=True)

        self.driver.create_post(message.channel_id, "_relaying to langchain_")
        output = agent_chain.run(message.text)
        self.driver.create_post(message.channel_id, output)
