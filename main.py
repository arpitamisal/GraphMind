import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from neo4j import GraphDatabase

import streamlit.components.v1 as components
from pyvis.network import Network
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Neo4jVector
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.graphs import Neo4jGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain

def render_graph(graph):
    query = """
    MATCH (n)
    OPTIONAL MATCH (n)-[r]->(m)
    RETURN n, r, m
    LIMIT 100
    """
    results = graph.query(query)

    net = Network(height="600px", width="100%", directed=True)
    net.barnes_hut()
    net.set_options("""
    {
    "nodes": {
        "shape": "dot",
        "size": 16,
        "font": { "size": 14 }
    },
    "edges": {
        "arrows": "to",
        "font": { "size": 12 }
    },
    "physics": {
        "enabled": true
    }
    }
    """)

    added_nodes = set()
    added_edges = set()

    for row in results:

    # Handle tuple OR dict
        if isinstance(row, tuple):
            n, r, m = row
        else:
            n = row.get("n")
            r = row.get("r")
            m = row.get("m")

        # ---------- NODE N ----------
        if n:
            if isinstance(n, dict):
                n_id = str(n.get("id", n.get("elementId", "node")))
                n_labels = n.get("labels", ["Node"])
                n_props = n.get("properties", {})
            else:
                n_id = str(getattr(n, "id", getattr(n, "element_id", "node")))
                n_labels = list(getattr(n, "labels", ["Node"]))
                n_props = dict(n)

            n_label = n_labels[0] if n_labels else "Node"
            n_name = n_props.get("id") or n_props.get("name") or n_props.get("text") or n_id

            if n_id not in added_nodes:
                net.add_node(n_id, label=str(n_name), title=str(n_label))
                added_nodes.add(n_id)

        # ---------- NODE M ----------
        if m:
            if isinstance(m, dict):
                m_id = str(m.get("id", m.get("elementId", "node")))
                m_labels = m.get("labels", ["Node"])
                m_props = m.get("properties", {})
            else:
                m_id = str(getattr(m, "id", getattr(m, "element_id", "node")))
                m_labels = list(getattr(m, "labels", ["Node"]))
                m_props = dict(m)

            m_label = m_labels[0] if m_labels else "Node"
            m_name = m_props.get("id") or m_props.get("name") or m_props.get("text") or m_id

            if m_id not in added_nodes:
                net.add_node(m_id, label=str(m_name), title=str(m_label))
                added_nodes.add(m_id)

        # ---------- EDGE ----------
        if n and r and m:
            if isinstance(r, dict):
                rel_type = r.get("type", "RELATED_TO")
            else:
                rel_type = getattr(r, "type", "RELATED_TO")

            source_id = str(n_id)
            target_id = str(m_id)

            edge_key = (source_id, target_id, rel_type)
            if edge_key not in added_edges:
                net.add_edge(source_id, target_id, label=rel_type)
                added_edges.add(edge_key)

    net.save_graph("graph.html")

    with open("graph.html", "r", encoding="utf-8") as f:
        html = f.read()

    components.html(html, height=620, scrolling=True)

def main():
    st.set_page_config(
        layout="wide",
        page_title="GraphMind",
        page_icon=":graph:"
    )
    st.sidebar.image('logo.png', width='content') 
    with st.sidebar.expander("Expand Me"):
        st.markdown("""
    This application allows you to upload a PDF file, extract its content into a Neo4j graph database, and perform queries using natural language.
    It leverages LangChain and OpenAI's GPT models to generate Cypher queries that interact with the Neo4j database in real-time.
    """)
    st.title("GraphMind: Real-Time GraphRAG App")

    load_dotenv()

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Set OpenAI API key
    if 'OPENAI_API_KEY' not in st.session_state:
        st.sidebar.subheader("OpenAI API Key")
        openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type='password')
        if openai_api_key:
            os.environ['OPENAI_API_KEY'] = openai_api_key
            st.session_state['OPENAI_API_KEY'] = openai_api_key
            st.sidebar.success("OpenAI API Key set successfully.")
            embeddings = OpenAIEmbeddings()
            llm = ChatOpenAI(model_name="gpt-4o")  # Use model that supports function calling
            st.session_state['embeddings'] = embeddings
            st.session_state['llm'] = llm
    else:
        embeddings = st.session_state['embeddings']
        llm = st.session_state['llm']

    # Initialize variables
    neo4j_url = None
    neo4j_username = None
    neo4j_password = None
    graph = None

    # Set Neo4j connection details
    neo4j_database = st.sidebar.text_input("Neo4j Database:", value="406f38bf")
    if 'neo4j_connected' not in st.session_state:
        st.sidebar.subheader("Connect to Neo4j Database")
        neo4j_url = st.sidebar.text_input("Neo4j URL:", value="neo4j+s://<your-neo4j-url>")
        neo4j_username = st.sidebar.text_input("Neo4j Username:", value="neo4j")
        neo4j_password = st.sidebar.text_input("Neo4j Password:", type='password')
        connect_button = st.sidebar.button("Connect")
        if connect_button and neo4j_password:
            try:
                graph = Neo4jGraph(
                url=neo4j_url,
                username=neo4j_username,
                password=neo4j_password,
                database=neo4j_database
            )
                st.session_state['graph'] = graph
                st.session_state['neo4j_connected'] = True
                # Store connection parameters for later use
                st.session_state['neo4j_url'] = neo4j_url
                st.session_state['neo4j_username'] = neo4j_username
                st.session_state['neo4j_password'] = neo4j_password
                st.session_state['neo4j_database'] = neo4j_database
                st.sidebar.success("Connected to Neo4j database.")
            except Exception as e:
                st.error(f"Failed to connect to Neo4j: {e}")
    else:
        graph = st.session_state['graph']
        neo4j_url = st.session_state['neo4j_url']
        neo4j_username = st.session_state['neo4j_username']
        neo4j_password = st.session_state['neo4j_password']
        neo4j_database = st.session_state['neo4j_database']

    # Ensure that the Neo4j connection is established before proceeding
    if graph is not None:
        # File uploader
        uploaded_file = st.file_uploader("Please select a PDF file.", type="pdf")

        if uploaded_file is not None:
            with st.spinner("Processing the PDF..."):
                st.session_state["chat_history"] = []
                # Save uploaded file to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_file_path = tmp_file.name

                # Load and split the PDF
                loader = PyPDFLoader(tmp_file_path)
                pages = loader.load_and_split()

                text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=40)
                docs = text_splitter.split_documents(pages)

                lc_docs = []
                for doc in docs:
                    lc_docs.append(Document(page_content=doc.page_content.replace("\n", ""), 
                    metadata={'source': uploaded_file.name}))

                # Clear the graph database
                cypher = """
                  MATCH (n)
                  DETACH DELETE n;
                """
                graph.query(cypher)

                # Define allowed nodes and relationships
                allowed_nodes = ["Patient", "Disease", "Medication", "Test", "Symptom", "Doctor"]
                allowed_relationships = ["HAS_DISEASE", "TAKES_MEDICATION", "UNDERWENT_TEST", "HAS_SYMPTOM", "TREATED_BY"]

                # Transform documents into graph documents
                transformer = LLMGraphTransformer(
                    llm=llm,
                    allowed_nodes=allowed_nodes,
                    allowed_relationships=allowed_relationships,
                    node_properties=False, 
                    relationship_properties=False
                ) 

                graph_documents = transformer.convert_to_graph_documents(lc_docs)
                graph.add_graph_documents(graph_documents, include_source=True)

                # Use the stored connection parameters
                index = Neo4jVector.from_existing_graph(
                    embedding=embeddings,
                    url=neo4j_url,
                    username=neo4j_username,
                    password=neo4j_password,
                    database=neo4j_database,
                    node_label="Patient",
                    text_node_properties=["id", "text"],
                    embedding_node_property="embedding",
                    index_name="vector_index",
                    keyword_index_name="entity_index",
                    search_type="hybrid"
                )

                st.success(f"{uploaded_file.name} preparation is complete.")
                st.subheader("Knowledge Graph Visualization")
                render_graph(graph) 

                # Retrieve the graph schema
                schema = graph.get_schema

                # Set up the QA chain
                template = """
                Task: Generate a Cypher statement to query the graph database.

                Instructions:
                Use only relationship types and properties provided in schema.
                Do not use other relationship types or properties that are not provided.

                schema:
                {schema}

                Note: Do not include explanations or apologies in your answers.
                Do not answer questions that ask anything other than creating Cypher statements.
                Do not include any text other than generated Cypher statements.

                Question: {question}""" 

                question_prompt = PromptTemplate(
                    template=template, 
                    input_variables=["schema", "question"] 
                )

                qa = GraphCypherQAChain.from_llm(
                    llm=llm,
                    graph=graph,
                    cypher_prompt=question_prompt,
                    verbose=True,
                    allow_dangerous_requests=True
                )
                st.session_state['qa'] = qa
    else:
        st.warning("Please connect to the Neo4j database before you can upload a PDF.")

    if 'qa' in st.session_state:
        st.subheader("Ask Questions")

        question = st.text_input("Enter your question:", key="question_input")

        col1, col2 = st.columns([1, 1])

        with col1:
            ask_button = st.button("Ask")

        with col2:
            clear_button = st.button("Clear Chat History")

        if ask_button and question:
            with st.spinner("Generating answer..."):
                res = st.session_state['qa'].invoke({"query": question})
                answer = res["result"]

                st.session_state["chat_history"].append({
                    "question": question,
                    "answer": answer
                })

        if clear_button:
            st.session_state["chat_history"] = []

        if st.session_state["chat_history"]:
            st.markdown("### Conversation")
            for i, chat in enumerate(st.session_state["chat_history"], start=1):
                st.markdown(f"**Q{i}:** {chat['question']}")
                st.markdown(f"**A{i}:** {chat['answer']}")
                st.markdown("---")


if __name__ == "__main__":
    main()


