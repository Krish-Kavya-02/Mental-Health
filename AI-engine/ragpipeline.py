from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
import time

def create_rag_pipeline():
    # Initialize the HuggingFace embeddings
    huggingface_embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

    # Create a Chroma vector store
    vector_store = Chroma(
        collection_name="example_collection",
        embedding_function=huggingface_embeddings,
        persist_directory="./chroma_db"
    )

    retriever = vector_store.as_retriever(search_kwargs={"k": 2})

    # Define the main prompt template (RAG-style: context + question)
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        You are a helpful and empathetic mental health assistant.
        Only use the context provided below to answer the question.
        If the context is irrelevant or missing, say: "I'm sorry, I couldn't find information to help with that."

        Context:
        {context}

        Question:
        {question}

        Answer:""".strip()
    )

    # Initialize the Ollama LLM
    llm = OllamaLLM(
        model="gemma3:1b",
        temperature=0.1,
    )

    # Memory for conversation
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        input_key="question",
        output_key="answer"
    )

    # Create the ConversationalRetrievalChain (fixed prompt usage)
    rag_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": prompt_template}
    )

    # Follow-up generator prompt
    followup_prompt = PromptTemplate(
        input_variables=["chat_history", "input"],
        template="""
        You are a helpful and empathetic mental health assistant.

        A user previously asked: "{chat_history}"
        You responded with: "{input}"

        Based on this conversation, suggest 2-3 relevant and thoughtful follow-up questions or next steps the user might ask or explore. These should be supportive and conversational, keeping the mental health tone in mind.

        Only output the suggestions, each on a new line without numbering.
        """.strip()
    )

    # RAG question + follow-up wrapper
    def ask_with_followups(question, chat_history):
        start = time.time()
        # Convert chat_history to a list of strings if needed
        formatted_history = []
        for entry in chat_history:
            if isinstance(entry, tuple) and len(entry) == 2:
                formatted_history.append(f"{entry[0]}: {entry[1]}")
            else:
                formatted_history.append(str(entry))

        result = rag_chain.invoke({"question": question, "chat_history": formatted_history})
        end = time.time()

        # Defensive: get answer from result
        answer = result.get('answer', result.get('result', ''))

        # Use the actual chat history in the follow-up prompt
        formatted_prompt = followup_prompt.format(
            chat_history="\n".join(formatted_history + [f"user: {question}"]),
            input=answer
        )
        suggestions = llm.invoke(formatted_prompt)

        return {
            "answer": answer,
            "source_documents": result.get("source_documents", []),
            "followups": suggestions.strip().split("\n"),
            "response_time": round(end - start, 2)
        }

    return ask_with_followups
