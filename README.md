# 🧠 GraphMind – GraphRAG Knowledge Engine

GraphMind is a **GraphRAG-powered application** that transforms unstructured documents into structured knowledge graphs and enables **natural language querying** over a Neo4j database.

---

## 🚀 Features

- 📄 Upload PDF documents  
- 🧠 Extract entities & relationships using **LLMs (GPT-4o)**  
- 🕸️ Build a **knowledge graph in Neo4j**  
- 🔍 Query the graph using **natural language**  
- 💬 Multi-turn **chat interface** for continuous Q&A  
- 📊 Interactive **graph visualization** with PyVis  
- 🔄 Real-time graph updates per document  

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit  
- **LLM:** GPT-4o (OpenAI)  
- **Framework:** LangChain  
- **Graph DB:** Neo4j (Aura / Local)  
- **Visualization:** PyVis  
- **Backend:** Python  

---

## ⚙️ How It Works

1. Upload a PDF document  
2. Text is extracted and chunked  
3. LLM converts text → **graph structure (nodes + relationships)**  
4. Data is stored in **Neo4j**  
5. Users query the graph via natural language  
6. Cypher queries are auto-generated and executed  
7. Results are returned and visualized  

---

## 📦 Installation

```bash
git clone https://github.com/your-username/GraphMind.git
cd GraphMind

python3 -m venv venv
source venv/bin/activate   # Mac/Linux
# venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

---

## 🔑 Environment Setup

Create a .env file:
```
OPENAI_API_KEY=your_openai_api_key
```

---

## 🧪 Run the App
```
streamlit run main.py
```

---

## 🗄️ Neo4j Setup

### Use Neo4j Aura (recommended):

- Create a free instance
- Copy credentials:
  URI → neo4j+s://...
  Username
  Password
  Database

Enter these in the Streamlit sidebar.

---

## 💡 Example Queries
- “What diseases does John have?”
- “Which medications are prescribed?”
- “Who treated Alice?”
- “What relationships exist in the graph?”

---

## 📊 Output
- Dynamic knowledge graph visualization
- Multi-turn conversational responses
- Structured insights from unstructured data

--- 

## 📈 Project Impact
- Generated 100+ nodes and relationships from document data
- Enabled real-time graph-based querying
- Reduced manual knowledge extraction effort significantly

--- 

## 🔮 Future Improvements
- Advanced graph filtering & search
- Multi-document ingestion
- Table-aware PDF parsing
- Domain-specific schema tuning
- Export graph as JSON / PNG
