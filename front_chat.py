import streamlit as st
from back_rag import (
    bot,
    ingest_pdf,
    retrieve_threads,
    thread_document_metadata,
)
from langchain_core.messages import HumanMessage,AIMessage
import uuid
#---------------------------------------------------
def generate_uid():
    thread_id=uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id=generate_uid()
    st.session_state['thread_id']=thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history']=[]

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_thread']:
        st.session_state['chat_thread'].append(thread_id)
    
def load_conv(thread_id):
    state = bot.get_state(
        config={"configurable": {"thread_id": thread_id}}
    )

    messages = state.values.get("messages", [])

    temp = []
    for msg in messages:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        temp.append({"role": role, "content": msg.content})

    return temp

#----------------------session------------------------------------
if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]

if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=generate_uid()

if 'chat_thread' not in st.session_state:
    st.session_state['chat_thread']=retrieve_threads()

if "ingested_docs" not in st.session_state:
    st.session_state["ingested_docs"] = {}

add_thread(st.session_state['thread_id'])

thread_key = str(st.session_state["thread_id"])
thread_docs = st.session_state["ingested_docs"].setdefault(thread_key, {})
threads = st.session_state["chat_thread"][::-1]
selected_thread = None
#----------------------session------------------------------


#### side bar----------------------------------
st.sidebar.title("LangGraph PDF Chatbot")
st.sidebar.markdown(f"**Thread ID:** `{thread_key}`")

if st.sidebar.button("New Chat", use_container_width=True):
    reset_chat()
    st.rerun()

if thread_docs:
    latest_doc = list(thread_docs.values())[-1]
    st.sidebar.success(
        f"Using `{latest_doc.get('filename')}` "
        f"({latest_doc.get('chunks')} chunks from {latest_doc.get('documents')} pages)"
    )
else:
    st.sidebar.info("No PDF indexed yet.")

uploaded_pdf = st.sidebar.file_uploader("Upload a PDF for this chat", type=["pdf"])
if uploaded_pdf:
    if uploaded_pdf.name in thread_docs:
        st.sidebar.info(f"`{uploaded_pdf.name}` already processed for this chat.")
    else:
        with st.sidebar.status("Indexing PDF…", expanded=True) as status_box:
            summary = ingest_pdf(
                uploaded_pdf.getvalue(),
                thread_id=thread_key,
                filename=uploaded_pdf.name,
            )
            thread_docs[uploaded_pdf.name] = summary
            status_box.update(label="✅ PDF indexed", state="complete", expanded=False)

st.sidebar.subheader("Past conversations")
if not threads:
    st.sidebar.write("No past conversations yet.")
else:
    for thread_id in threads:
        if st.sidebar.button(str(thread_id), key=f"side-thread-{thread_id}"):
            selected_thread = thread_id


st.sidebar.header('My Chats')

for thread_id in st.session_state['chat_thread']:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id']=thread_id
        st.session_state['message_history']=load_conv(thread_id)
        
###---------------------------------------------
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])


user_input=st.chat_input("Type here: ")
config={
    'configurable':{'thread_id':st.session_state['thread_id']},
    'metadata':{'thread_id':st.session_state['thread_id']},
    'run_name':'Chat_turn'
    }
if user_input:
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.markdown(user_input)

    
    with st.chat_message('Assistant'):
        def ai_only():
            for message_chunk,metadata in bot.stream(
                {'messages':[HumanMessage(content=user_input)]},
                config=config,
                stream_mode='messages'
            ):
                if isinstance(message_chunk,AIMessage):
                    yield message_chunk.content
        ai_message=st.write_stream(ai_only())
        
    st.session_state['message_history'].append({'role':'assistant','content':ai_message })

    doc_meta = thread_document_metadata(thread_key)
    if doc_meta:
        st.caption(
            f"Document indexed: {doc_meta.get('filename')} "
            f"(chunks: {doc_meta.get('chunks')}, pages: {doc_meta.get('documents')})"
        )

    st.divider()

    if selected_thread:
        st.session_state["thread_id"] = selected_thread
        messages = load_conv(selected_thread)

        temp_messages = []
        for msg in messages:
            role = "user" if isinstance(msg, HumanMessage) else "assistant"
            temp_messages.append({"role": role, "content": msg.content})
        st.session_state["message_history"] = temp_messages
        st.session_state["ingested_docs"].setdefault(str(selected_thread), {})
        st.rerun()




