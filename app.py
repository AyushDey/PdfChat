import streamlit as st
from dotenv import load_dotenv 
import os
from pypdf import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import GPT4All
from langchain.llms.google_palm import GooglePalm
from chat_template import css, bot_template, user_template

def convert_pdf_to_text(pdfdocs):
    txt = ''
    for pdf in pdfdocs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            txt += page.extract_text()
    return txt

def getChunks(rawtxt):
    splitText = CharacterTextSplitter(
        separator='\n',
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = splitText.split_text(rawtxt)
    return chunks

def get_vectors(txt_list):
    #load the value from .env file to get the huggingface api key
    embeddings = HuggingFaceInferenceAPIEmbeddings(
        api_key=os.getenv('HUGGINGFACEHUB_API_TOKEN'),
        model_name = "BAAI/bge-large-en-v1.5"
    )
    vector_store = FAISS.from_texts(txt_list, embeddings)
    return vector_store

def getConversation(vector):
    model = 'models/text-bison-001'
    api_key = os.getenv('PALM_API')
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    llm = GooglePalm(
        google_api_key=api_key,
        model_name=model
    )
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector.as_retriever(),
        memory=memory
    )
    return chain

def handle_input(user_q):
    response = st.session_state.converse({'question': user_q})
    #st.write(response)
    st.session_state.chat_history = response['chat_history']
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace('{{MSG}}', message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace('{{MSG}}', message.content), unsafe_allow_html=True)

#main function
def main():
    load_dotenv()
    st.set_page_config(page_title='Note Buddy',
                       page_icon=':memo:',
                       layout='centered',
                       initial_sidebar_state='auto')
    
    st.write(css, unsafe_allow_html=True)
    
    if 'converse' not in st.session_state:
        st.session_state.converse = None
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = None

    st.header('Chat with your PDFs')
    st.subheader('Upload your PDFs and get notes from them')
    st.markdown('---')
    user_q = st.text_input('Ask your question:')
    if user_q:
        handle_input(user_q)

    with st.sidebar:
        st.subheader('Your documents')
        
        pdfdocs = st.file_uploader('Upload your PDFs', type=['pdf'], accept_multiple_files=True)
        if st.button('Process documents'):
            st.spinner('Processing your documents...')
            # get pdf text
            rawtxt = convert_pdf_to_text(pdfdocs)
            #st.write(rawtxt)
            st.spinner('Converting into text...')
            #get text chunks
            txt_list = getChunks(rawtxt)
            
            #create vector store
            vector = get_vectors(txt_list)
            #st.write(vector)
            st.spinner('Creating conversation chain...')
            #create conversation chain
            st.session_state.converse = getConversation(vector)
            st.write('Made with :heart: by Ayush for Dayita Maity')




if __name__ == "__main__":
    main()