import streamlit as st
import sqlite3
import time
import os
import base64
from PIL import Image
import io
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv
import chromadb
from openai import OpenAI
from chromadb.utils import embedding_functions
import shutil
from response_fuctions import *


load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
import chromadb

# This initializes Chroma persistent storage properly
client = chromadb.PersistentClient(path="./data/chroma_persistent_storage")
client.get_or_create_collection(name="init_collection")
client = OpenAI(api_key=openai_key)

def split_text(text,chunk_size=1000,chunk_overlap=20):
    chunks = []
    start = 0
    while start <len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - chunk_overlap
    return chunks

def get_openai_embedding(text):
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    embedding = response.data[0].embedding
    print("==== Generating embeddings... ====")
    return embedding

def create_embeddings():
    import tempfile
    chroma_path = "./data/chroma_persistent_storage"

    # Check if Chroma storage is missing or corrupted
    if not os.path.exists(os.path.join(chroma_path, "chroma.sqlite3")):
        st.warning("🔁 Bootstrapping Chroma persistent directory...")

        # Use Ephemeral (in-memory) client to create a dummy collection
        temp_client = chromadb.Client()
        temp_client.get_or_create_collection("bootstrap")
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = os.path.abspath(tmp)
            shutil.copytree(temp_client._system._persist_directory, chroma_path, dirs_exist_ok=True)

    
    # Initialize the embedding function
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=openai_key,
        model_name="text-embedding-3-small",
    )

    # Initialize Chroma client
    chroma_client = chromadb.PersistentClient(path=chroma_path)

    collection_name = "document_qa_collection"

    # Delete existing collection if it exists (for re-indexing)
    try:
        chroma_client.delete_collection(name=collection_name)
    except:
        pass

    # Recreate collection with embedding function
    collection = chroma_client.get_or_create_collection(
        name=collection_name,
        embedding_function=openai_ef
    )

    data = row[2]
    chunks = split_text(data)
    # print(f"== Splitting docs into chunks ==")
    text_chunks = []
    for i, chunk in enumerate(chunks):
        text_chunks.append({"id": f"chunk{i+1}", "text": chunk})
        
    
    for chunk in text_chunks:
        st.write("==== Generating embeddings... ====")
        chunk["embedding"] = get_openai_embedding(chunk["text"])
    
    for chunk in text_chunks:
        st.write("==== inserting chunks into db;; ====")
        collection.upsert(ids=[chunk["id"]], documents=[chunk["text"]],embeddings=[chunk['embedding']])

tabs = ["Character creation"]
if os.path.isdir("./data/chroma_persistent_storage"):
    tabs = ["Character creation", "Chatbot"]
icons = ["bi-box-arrow-in-right"] + ["person-fill"]

# selected_tab = option_menu(
#     menu_title="Select a tab",
#     options=tabs,
#     default_index=0,
#     icons=icons,
#     orientation="horizontal",
# )

conn = sqlite3.connect('characters.db', check_same_thread=False)  # allow Streamlit threads
c = conn.cursor()
c.execute("SELECT name, prompt, text_data, image, description FROM characters ORDER BY id DESC LIMIT 1")
row = c.fetchone()
CUSTOM_CHARACTER_PROFILE_IMG = None
if row and row[3]:
    try:
        CUSTOM_CHARACTER_PROFILE_IMG = Image.open(io.BytesIO(row[3]))
    except Exception as e:
        st.error(f"❌ Failed to load profile image: {e}")

# if selected_tab == "Character creation":
#     st.title("🧠 Create Your Own Character Chatbot")
#     c.execute("SELECT name, prompt, text_data, image, description FROM characters ORDER BY id DESC LIMIT 1")
#     saved_character = c.fetchone()
#     default_name = saved_character[0] if saved_character else ""
#     default_prompt = saved_character[1] if saved_character else ""
#     default_description = saved_character[4] if saved_character else ""
    
    
#     # --- FORM ---
#     with st.form("character_form"):
#         name = st.text_input("Character Name", value=default_name)
#         prompt = st.text_area("System Prompt (personality, tone, etc.)", value=default_prompt)
#         text_file = st.file_uploader("Upload .txt file for knowledge base", type=["txt"])
#         image_file = st.file_uploader("Upload Profile Image (JPG/PNG)", type=["jpg", "png"])
#         description = st.text_area("Description", value=default_description)

#         if saved_character:
#             st.markdown("📝 Using last saved files unless new ones are uploaded.")

#         submitted = st.form_submit_button("💾 Save Character")
#         if submitted:
#             text_data = text_file.read().decode("utf-8") if text_file else saved_character[2]
#             image_bytes = image_file.read() if image_file else saved_character[3]
#             if not (name and prompt and text_data and image_bytes):
#                 st.error("⚠️ Please complete all fields before saving.")
#             else:
#                 c.execute("DELETE FROM characters")
#                 conn.commit()
#                 c.execute(
#                     "INSERT INTO characters (name, prompt, text_data, image, description) VALUES (?, ?, ?, ?, ?)",
#                     (name, prompt, text_data, image_bytes, description)
#                 )
#                 conn.commit()
#                 st.success(f"✅ Character '{name}' saved successfully!")

#     c.execute("SELECT name, prompt, text_data, image, description FROM characters ORDER BY id DESC LIMIT 1")
#     row = c.fetchone()
#     if row:
#         st.subheader(f"Character: {row[0]}")
#         st.markdown(f"**Prompt:** {row[1]}")
#         st.markdown("**Sample from text data (first 300 chars):**")
#         st.code(row[2][:300] + "..." if len(row[2]) > 300 else row[2])
#         st.markdown("**Profile Image:**")
#         image = Image.open(io.BytesIO(row[3]))
#         st.image(image, width=150)
#         st.markdown(f"**Description:** {row[4]}")
#     else:
#         st.info("No character saved yet.")

#     st.write("## Press the button to create your character chatbot")
#     create_embeddings_button = st.button("Feed the chat with your uploaded text data")
#     if create_embeddings_button:
#         create_embeddings()



def get_circular_image_html(img, width=150):
    try:
        c.execute("SELECT name, prompt, text_data, image FROM characters ORDER BY id DESC LIMIT 1")
        row = c.fetchone()
        
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # HTML with CSS for circular image
        html = f'''
        <div style="display: flex; flex-direction: row; justify-content: flex-start; margin-bottom:20px;">
            <div style="width:100px;">
                <img src="data:image/png;base64,{img_str}" 
                    style="border-radius:50%; width:{width}px; height:{width}px; object-fit:cover;">
            </div>
            <div style="margin-left:30%;">
                <h1>{row[0]}</h1>
            </div>
        </div>
        '''
        return html
    except Exception as e:
        return f"<div>Error loading image: {e}</div>"




# Spacing to prevent overlap

# if selected_tab == "Chatbot":
with st.sidebar:
    st.markdown(get_circular_image_html(CUSTOM_CHARACTER_PROFILE_IMG), unsafe_allow_html=True)
    st.write("# Profile:")
    st.write(f'''{row[4]}''')
st.markdown('<h1 class="chat-title">AI Chatbot</h1>', unsafe_allow_html=True)

# Scrollable chat messages container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    if message["role"] == 'assistant':
        with st.chat_message("assistant", avatar=CUSTOM_CHARACTER_PROFILE_IMG):
            st.write(message['message'])
    else:
        with st.chat_message("user"):
            st.write(message['message'])
st.markdown('</div>', unsafe_allow_html=True)

if user_input := st.chat_input("Ask me anything...", key="user_input"):
    user_message = {"role": "user", "message": user_input}
    st.session_state.chat_history.append(user_message)
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant", avatar=CUSTOM_CHARACTER_PROFILE_IMG):
        status_text = st.empty()
        status_text.markdown(row[0] +" is typing...")
        chunks = retrieve_documents(user_input)
        assistant_response = generate_response(user_input, chunks, row[1])
        message_placeholder = st.empty()
        status_text.empty()
        full_response = ""
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response,unsafe_allow_html=True)
        
    chatbot_message = {"role": "assistant", "message": assistant_response}
    st.session_state.chat_history.append(chatbot_message)
