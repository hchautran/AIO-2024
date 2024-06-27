import torch
from transformers import BitsAndBytesConfig
from transformers import AutoTokenizer , AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface . llms import HuggingFacePipeline

from langchain . memory import ConversationBufferMemory
from langchain_community . chat_message_histories import ChatMessageHistory
from langchain_community . document_loaders import PyPDFLoader,TextLoader
from langchain . chains import ConversationalRetrievalChain

from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core . runnables import RunnablePassthrough
from langchain_core . output_parsers import StrOutputParser
from langchain import hub
import os

PATH = f'{os.path.dirname(os.path.realpath(__file__))}'
FILE_PATH = f'{PATH}/materials/YOLOv10_Tutorials.pdf'

################################
loader = PyPDFLoader(FILE_PATH)
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size =1000, chunk_overlap =100)
docs = text_splitter.split_documents(documents)
print (" Number of sub - documents : ", len ( docs ) )
print(docs[0])

embedding = HuggingFaceEmbeddings()
vector_db = Chroma.from_documents ( documents =docs, embedding = embedding )
retriever = vector_db.as_retriever()
result = retriever.invoke (" What is YOLO ?")
print ("Number of relevant documents : ", len ( result ) )

################################

nf4_config = BitsAndBytesConfig (
    load_in_4bit =True ,
    bnb_4bit_quant_type =" nf4 ",
    bnb_4bit_use_double_quant =True ,
    bnb_4bit_compute_dtype = torch . bfloat16
)


MODEL_NAME = "lmsys/vicuna-7b-v1.5"

model = AutoModelForCausalLM . from_pretrained (
    MODEL_NAME ,
    quantization_config = nf4_config ,
    low_cpu_mem_usage = True
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


model_pipeline = pipeline (
    "text-generation",
    model =model ,
    tokenizer = tokenizer ,
    max_new_tokens =512 ,
    pad_token_id = tokenizer.eos_token_id ,
    device_map ="auto "
)

llm = HuggingFacePipeline (
    pipeline = model_pipeline ,
)

################################
prompt = hub.pull("rlm/rag-prompt")


def format_docs ( docs ) :
    return "\n\n". join (doc . page_content for doc in docs )

rag_chain = (
    {" context ": retriever | format_docs , " question ": RunnablePassthrough
    () }
    | prompt
    | llm
    | StrOutputParser ()
)

USER_QUESTION = " YOLOv10 là gì?"
output = rag_chain . invoke ( USER_QUESTION )
answer = output . split ('Answer :') [1].strip ()
print ( answer )