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
You are a helpful and empathetic mental health assistant.

Your task is to ONLY answer the user's question using the context provided below.
You are NOT allowed to use external facts or make assumptions.
If the context is missing or irrelevant to the question, respond strictly with:
"I'm sorry, I couldn't find information to help with that."

If the context is missing but the query is clearly about mental health,
you may use your general knowledge to provide a helpful answer.

Always respond in a supportive and understanding tone, as if you are a mental health professional.
Always respond in English.

Context:
{context}

Question:
{question}

Answer:""".strip()
    )

    # Initialize Ollama LLM
    llm = OllamaLLM(
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
You are a helpful and empathetic mental health assistant. Always respond only in English.

A user previously asked: "{chat_history}"
You responded with: "{input}"

Based on this conversation, suggest 2–3 relevant and thoughtful follow-up questions or next steps the user might ask or explore. These should be supportive and conversational, keeping the mental health tone in mind.

Only output the suggestions, each on a new line without numbering.
""".strip()
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
        if not is_english(answer):
            answer = "Sorry, something went wrong. Let's try again in English."

        # Generate follow-up suggestions
        formatted_prompt = followup_prompt.format(
            chat_history="\n".join(formatted_history + [f"user: {question}"]),
            input=answer
        )

        suggestions = llm.invoke(formatted_prompt)
        if not is_english(suggestions):
            suggestions = "Sorry, I couldn't generate follow-up suggestions in English."

        return {
            "answer": answer,
            "source_documents": result.get("source_documents", []),
            "followups": suggestions.strip().split("\n"),
            "response_time": round(end - start, 2)
        }

    return ask_with_followups
