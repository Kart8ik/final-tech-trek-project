import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader
import pypdf

st.set_page_config(page_title="WORLD CUP BOT, powered by LlamaIndex", page_icon="🏆", layout="centered", initial_sidebar_state="auto", menu_items=None)

openai.api_key =("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")
st.title("question about the cricket and FIFA world cup schedule, powered by LlamaIndex 🏆🏏")
st.write("created with ❤️ by :blue[Karthik] and :blue[Musharraf]")
st.caption("this chatbot can answer questions about schedule of cwc and schedule of fifa world cup 2022 and also give the results of the match")
st.caption("you can also ask it our names and details like branch,year and SRN")



if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about the world cup schedule...let me know todays date as well..thanks"}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading the world cup data -let me coook!!."):
        reader = SimpleDirectoryReader(input_dir=r"C:\Users\Shri Karthik\Desktop\techtrek", recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert in analyzing world cup data of the world cup , Assume all input prompts to be with respect to world cup and mention u support india and love virat kohli"))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

index = load_data()

# st.text(index)

# chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True, system_prompt="You are an expert on the Streamlit Python library and your job is to answer technical questions. Assume that all questions are related to the Streamlit Python library. Keep your answers technical and based on facts – do not hallucinate features.")

if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("let me coook..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)
st.write("""
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            right: 0;
            width: 400px; /* Adjust the width as needed */
            
            color: white; /* Text color */
            text-align: center;
            padding: 10px;
        }
        .icon {
            display: inline-block;
            margin: 0 10px;
        }
    </style>
    <div class="footer">
        <p>Follow Karthik on <a href="https://github.com/Kart8ik" target="_blank" style="color: white;">GitHub</a></p>
        <p>Follow Musharraf on <a href="https://github.com/MohammedMusharraf11" target="_blank" style="color: white;">GitHub</a></p>
	
    </div>
         """, unsafe_allow_html=True)

