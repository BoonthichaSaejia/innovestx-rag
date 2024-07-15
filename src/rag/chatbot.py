import os
import gradio as gr

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
import sys

sys.path.append(os.path.abspath('../..'))
import config
OPENAI_APIKEY = config.OPENAI_API_KEY

absolute_path = '/Users/bsaejia/Documents/2024_innovestx/innovestx-rag'
embeddings = OpenAIEmbeddings(api_key=OPENAI_APIKEY, max_retries=100, chunk_size=16, show_progress_bar=False)
llm = ChatOpenAI(api_key=OPENAI_APIKEY, temperature=0.5, model='gpt-4-turbo-2024-04-09')

# load faiss from disk
vectorstore = Chroma(persist_directory="innovestx_db/", embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_type = 'similarity_score_threshold' ,search_kwargs={"k":10,"score_threshold":0.4})
# Get pre-written rag prompt
prompt = hub.pull("rlm/rag-prompt")

prompt.messages[0].prompt.template = ''' 
You are an assistant for question-answering tasks working in InnovestX. InnovestX is the only securities company in Thailand that has both securities and digital asset brokerage licenses. The company is determined to take the industry to the next level by providing secure, transparent investment financial services and by collaborating with regulators to ensure that all customers receive the highest quality service.
Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question} 
Context: {context} 
Answer:
'''

# Format docs function
def format_docs(docs):
    whole_answer = ''
    for doc in docs:
        if doc.metadata['topic']=='pug' and doc.metadata['context'].find('data/txt') != -1:
            #print(doc.metadata['context'])
            file_path = os.path.join(absolute_path,doc.metadata['context'])
            #print(file_path)
            with open(file_path) as f:
                answer = f.read()
        elif doc.metadata['topic']=='faq':
            answer = f'Question:{doc.page_content}\nAnswer:{doc.metadata["context"]}'
        else:
            answer = doc.page_content
        whole_answer += "\n\n"+answer
            
    return whole_answer

# Create RAG Chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Function to generate answer
def generate_answer(message, history):
    result = rag_chain.invoke(message)
    return result


answer_bot = gr.ChatInterface(
                            generate_answer,
                            chatbot=gr.Chatbot(height=600),
                            textbox=gr.Textbox(placeholder="เชิญถามเกี่ยวกับข้อสงสัยและบริการของ InnovestX", container=False, scale=7),
                            title="Customer Assistant for InnovestX",
                            description="This application assist customers of InnovestX, an asset management company under SCBX Group. It could provide information and support on frequently asked questions (FAQs), product user guides, and private fund assistance.",
                            theme="soft",
                            cache_examples=False,
                            retry_btn=None,
                            undo_btn=None,
                            clear_btn=None,
                            stop_btn="Interrupt",
                            submit_btn="Ask"
                        )

if __name__ == "__main__":
    answer_bot.launch()