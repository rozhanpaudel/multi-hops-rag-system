import os
from config import get_environment_config
from langchain_openai import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from langchain_openai import OpenAIEmbeddings
from helper import split_and_format_data
from elastic_helper import get_elastic_retrival_obj
from elastic_helper import indices

# Fetching Environment Variables
openai_api_key=get_environment_config('OPEN_API_KEY')
model=get_environment_config('OPEN_API_MODEL')

# Fetching elastic retrival obj and indices
elastic_retrival = get_elastic_retrival_obj()
indices = indices()

class RAGModel():
    def __init__(self,api_key,model):
        self.chat = ChatOpenAI(
        openai_api_key=api_key,
        model=model
        )

        self.messages = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content="Hi AI, how are you today?"),
            AIMessage(content="I'm great thank you. How can I help you?")
        ]

        self.embedding_function = OpenAIEmbeddings(
                openai_api_key=api_key,
            )

    # {type:'ai',message:'message'}
    def get_inference(self,prompt,history=[]):
        if(len(history)):
           for elem in history:
               if elem.type == 'ai':
                   self.messages.append(AIMessage(content=elem.message))
               elif elem.type == 'user':
                   self.messages.append(HumanMessage(content=elem.message))           

        augmented_prompt_with_context = self.get_augmented_prompt(prompt)
        prompt = HumanMessage(content=str(prompt))
        self.messages.append(prompt)
        res = self.chat(self.messages)
        return res.content

    def get_augmented_prompt(self,query):
        query_vector = self.embedding_function.embed_query(str(query))

        source_knowledge = []
        for index in indices:
            knowledge_list = elastic_retrival.search_similar_documents(query_vector=query_vector, index_name=index, top_k=2)
            for knowledge in knowledge_list:
                print(knowledge['meta']['title'])
                source_knowledge.append(f"As per the {knowledge['meta']['title']} paper, the knowledge and evidence for the query is, {knowledge['content']}")

        source_knowledge = "\n".join(source_knowledge)   
        print(source_knowledge) 
        augmented_prompt = f"""Using the contexts below, answer the query. Contexts: {source_knowledge} Query: {query}"""
        return augmented_prompt

                            

def get_multihop_rag_model():
    return RAGModel(api_key=openai_api_key,model=model)



