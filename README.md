# Custom character chatbot (alan kay default character)

## Online Link:
- https://custom-character-ai-chatbot.onrender.com/


## Chat with Alan kay:
<img width="1510" alt="Alan kay Ai chatbot" src="https://github.com/user-attachments/assets/7d736399-855a-4e5c-aa35-9b3b9e2231a1" />


## Application architecture diagram

<img width="661" alt="Application Architecture diagram" src="https://github.com/user-attachments/assets/2e23c6f0-c9e8-4da6-a3cd-25c41b46a8da" />

### short description:
The application architecture is structured around three main conceptual sections: `Create Custom Character Tab`, `Text Data Preprocessing`, and `Alan Kay Chatbot Tab`.

* **Create Custom Character Tab:** This section allows users to create and manage custom characters for their chatbot. Users can submit their character data, including a knowledge base text file, through a Streamlit form, which then stores the information in `characters.db`. After submission, users can generate embeddings from the uploaded text data by pressing the "Feed the chat with your uploaded text data" button.
* **Text Data Preprocessing:** This stage handles the preparation of the knowledge base for the chatbot. It takes the `quora_q&a_alan_kay.txt` file or the users custom text data file as input from the db. The process focuses on splitting the input text documents to create the Text Chunks and finally "Generate Embeddings" which then are stored to the vector database.
* **Alan Kay Chatbot Tab:** This is the core interaction point where the user engages with the chatbot. A "User Question" is fed into the system, which then interacts with the "Vector Database" by retrieving the most relevant chunks as context. Finally, the context is then augmented into the final Prompt before generating the "Final Response" and present it to the user.

## How to run and set up
To run the Alan Kay chatbot application, you need to set up your Python environment, configure your OpenAI API key, and then execute it via the command line. Once running, you can freely interact with the Alan Kay chatbot.
### Set up python
First set up your python environment with the following command
```
python -m venv myenv
```
and activate it with
```
source myenv/bin/activate
```
on Linux/Mac users or 
```
myenv\Scripts\activate
```
for window users.

After activation, you can install the applications requirements (python 3.10.0 recommended) with:
```
pip install -r requirements.txt
```

### Configure your OpenAi api key

To configure your OpenAI API key, navigate to the main [OpenAI platform website](https://platform.openai.com/).

After obtaining your API key, add it to a `.env` file in your project root with the following format:
```
OPENAI_API_KEY=your_api_key_here
```

### Run webapp.py
To run the application you should enter the following command to your terminal:
```
streamlit run webapp.py
```


# Additional features for programmers
## Create your character:
<img width="809" alt="Screenshot 2025-05-20 at 11 46 17 PM" src="https://github.com/user-attachments/assets/77cafcd1-7fe3-4a09-b11a-77072205ab2d" />

## Feed the chat with your character data:
<img width="765" alt="Screenshot 2025-05-20 at 11 48 29 PM" src="https://github.com/user-attachments/assets/56a7b8a4-04cf-44c0-bc58-a76dbeb819f9" />

