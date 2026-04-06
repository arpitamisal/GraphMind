# 🧠 GraphMind – GraphRAG Knowledge Engine

GraphMind is a **GraphRAG-powered application** that transforms unstructured documents into structured knowledge graphs and enables **natural language querying** over a Neo4j database.

---

<img width="1281" height="681" alt="9" src="https://github.com/user-attachments/assets/3480f562-3543-45be-82c6-a44a38fe9bff" />
<img width="1259" height="766" alt="8" src="https://github.com/user-attachments/assets/ae5c9f21-53af-4e07-9125-6d5895475b22" />
<img width="1468" height="729" alt="7" src="https://github.com/user-attachments/assets/de4d54a5-24f7-4d8f-8d4c-3d01fd65b83b" />
<img width="1468" height="803" alt="6" src="https://github.com/user-attachments/assets/2d2aea50-c6df-4218-9f0e-98ab9a41a541" />
<img width="1470" height="812" alt="5" src="https://github.com/user-attachments/assets/05b0763d-a775-411b-a6e8-405434b4bb73" />
<img width="1470" height="812" alt="4" src="https://github.com/user-attachments/assets/5b27bc4a-696e-4e79-823a-ea4c9c674c86" />
<img width="1469" height="809" alt="3" src="https://github.com/user-attachments/assets/4df13c6e-fe7a-4e3b-be42-18301542fa39" />
<img width="1138" height="523" alt="2" src="https://github.com/user-attachments/assets/a54a4169-5f08-435c-860e-d181f574075b" />
<img width="1469" height="817" alt="1" src="https://github.com/user-attachments/assets/ca30e418-b9a7-42b0-a23f-25e141d9c818" />

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
