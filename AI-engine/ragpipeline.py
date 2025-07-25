from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langdetect import detect
import time


def is_english(text):
    try:
        return detect(text) == "en"
    except:
        return False


def create_rag_pipeline():
    # Initialize HuggingFace embeddings
    huggingface_embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

    # Load Chroma vector store
    vector_store = Chroma(
        collection_name="example_collection",
        embedding_function=huggingface_embeddings,
        persist_directory="./chroma_db"
    )

    retriever = vector_store.as_retriever(search_kwargs={"k": 2})

    # Prompt template
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        You are a supportive and empathetic mental health chatbot named "Mira".

        Your job is to listen, validate, and respond with compassion — just like a therapist might in a friendly conversation.

        - If the context contains useful information, use it in your response.
        - If context is missing, still respond empathetically and encourage the user.
        - Never say "I'm sorry I couldn't help" outright — instead, validate the emotion and offer a gentle nudge or suggestion.
        - Only respond to questions related to emotions, stress, relationships, or mental well-being. If the query is unrelated (e.g., about tech or programming), kindly guide the user back to mental health topics, in such cases  say "Ican't help you with that, but I'm here to talk about how you're feeling or what's on your mind."
        - Always speak in a warm, caring tone.
        - Avoid clinical jargon unless absolutely necessary.

        Context:
        {context}

        User: {question}

        Mira:""".strip()
    )

    # Initialize Ollama LLM
    llm = OllamaLLM(
        base_url= "http://host.docker.internal:11434",
        model="phi3:3.8b",
        temperature=0.1,
    )

    # Memory
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        input_key="question",
        output_key="answer"
    )

    # Build RAG chain
    rag_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": prompt_template}
    )

    # Follow-up suggestion prompt
    followup_prompt = PromptTemplate(
        input_variables=["chat_history", "input"],
        template="""
            You're Mira, an empathetic mental health chatbot.

            Based on the conversation so far, suggest 2–3 gentle follow-up replies Mira could say next. These should be friendly, warm, and show that you're listening and care.

            Chat History:
            {chat_history}

            Last Response:
            {input}

            Mira's possible next responses (one per line):""".strip()
    )

    # Final wrapper function
    def ask_with_followups(question, chat_history):
        start = time.time()

        # Format chat history
        formatted_history = []
        for entry in chat_history:
            if isinstance(entry, tuple) and len(entry) == 2:
                formatted_history.append(f"{entry[0]}: {entry[1]}")
            else:
                formatted_history.append(str(entry))

        # Invoke RAG chain
        result = rag_chain.invoke({
            "question": question,
            "chat_history": formatted_history
        })

        # DEBUG: Print source documents
        print("SOURCE DOCUMENTS:")
        for doc in result.get("source_documents", []):
            print(doc.page_content[:500])  # print first 500 characters to keep it readable
            print("-----")

        end = time.time()

        # Extract answer safely
        answer = result.get("answer", result.get("result", ""))

        # Language check
        if not is_english(answer) or not answer.strip():
            answer = "I'm here for you. It sounds like you're going through a lot — would you like to talk more about what's bothering you?"

        # Generate follow-up suggestions
        formatted_prompt = followup_prompt.format(
            chat_history="\n".join(formatted_history + [f"user: {question}"]),
            input=answer
        )

        suggestions = llm.invoke(formatted_prompt)
        if not is_english(suggestions):
            suggestions = "Sorry, I couldn't generate follow-up suggestions in English."

        return {
            "reply": answer.strip(),
            "source_documents": [doc.page_content for doc in result.get("source_documents", [])],
            "followups": [s.strip() for s in suggestions.strip().split("\n") if s.strip()],
            "response_time": round(end - start, 2)
        }

    return ask_with_followups
