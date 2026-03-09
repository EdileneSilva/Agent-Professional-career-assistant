import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from deepagents import create_deep_agent
from langchain_ollama import ChatOllama

load_dotenv(override=True)

# Configurar USER_AGENT para evitar o warning
os.environ.setdefault('USER_AGENT', 'CareerAgent/1.0 (Python script for job matching)')

#model = ChatOllama(model="mistral:7b-instruct")
model=ChatMistralAI(model="mistral-small-latest", api_key=os.getenv("MISTRALAI_API_KEY"))
embedder=MistralAIEmbeddings(model="mistral-embed", api_key=os.getenv("MISTRALAI_API_KEY"))

# Documents préparation
current_dir = os.getcwd()
file_name = "EDILENECV.pdf"
file_path = os.path.join(current_dir, "data", file_name)
db_dir = os.path.join(current_dir, "data","db")

if not os.path.exists(db_dir):
# Vector Store inictialization
    loader = PyPDFLoader(file_path)
    loaded_document = loader.load()

    # CUtting in chunks the text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=0)
    chunks = text_splitter.split_documents(loaded_document)

    # Addition of metadata
    for chunk in chunks:
        chunk.metadata["source"] = file_path
        chunk.metadata["categories"] = ["synthese", "expérience", "compétences", "formation","langues"]

    db = Chroma.from_documents(chunks, embedder, persist_directory=db_dir)
    print("vector store created")
else:
    print("vector store already exists")

db = Chroma(persist_directory=db_dir, embedding_function=embedder)

retriever = db.as_retriever(
    search_type = "similarity",
    search_kwargs = {"k": 5}
)

@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Recherche des informations dans le CV."""
    retrieve_docs = retriever.invoke(query)
    serialized = "\n\n".join(
        f"Contenu : {doc.page_content}" for doc in retrieve_docs
    )
    return (serialized, retrieve_docs)

memory = MemorySaver()

retrieve_subagent = {
    "name": "retrieve-agent",
    "description": "Récupère les informations du CV",
    "system_prompt": (
        "Tu es un assistant spécialisé dans l'extraction d'informations d'un CV. "
        "IMPORTANT: Le CV est déjà chargé dans la base de données vectorielle. "
        "Utilise TOUJOURS l'outil 'retrieve' pour chercher les informations. "
        "Cherche les compétences, expériences, formations et langues du candidat. "
        "Retourne un résumé complet des points forts du CV."
    ),
    "tools": [retrieve],
}

@tool
def extract_text_url(url: str) -> str:
    """Extrait le texte d'une page web."""
    try:
        loader = WebBaseLoader(url)
        docs = loader.load()
        return docs[0].page_content
    except Exception as e:
        return f"Erreur: {str(e)}"

offer_subagent = {
    "name": "offer-agent",
    "description": "Extrait le contenu d'une offre d'emploi depuis un URL",
    "system_prompt": (
        "Tu es un extracteur de contenu web. "
        "Quand tu reçois une demande avec une URL, utilise l'outil 'extract_text_url' "
        "pour extraire le texte de la page. "
        "L'URL sera fournie dans la description de la tâche ou dans le contexte."
    ),
    "tools": [extract_text_url],
}   

@tool
def offer_match(percentage: int, points_forts: str, points_faibles: str) -> str:
    """
    Calcule et retourne la correspondance entre CV et offre.
    
    Args:
        percentage: Pourcentage de match entre 0 et 100
        points_forts: Liste des compétences qui matchent (séparées par des virgules)
        points_faibles: Liste des compétences manquantes (séparées par des virgules)
    
    Returns:
        Résultat formaté du match
    """
    result = f"""
Resultat du match CV/offre

Score de correspondance : {percentage}%

Points forts :
{points_forts}

Points à ameliorer:
{points_faibles}
"""
    return result

match_subagent = {
    "name": "match-agent",
    "description": "Analyse la correspondance entre un CV et une offre d'emploi",
    "system_prompt": (
        "Tu analyses la correspondance entre un CV et une offre d'emploi. "
        "\n\nTa tâche est SIMPLE: "
        "\n1. Compare les compétences du CV avec celles de l'offre "
        "\n2. Identifie ce qui MATCHE et ce qui MANQUE "
        "\n3. Calcule un pourcentage (0-100%) "
        "\n\nTu DOIS ABSOLUMENT utiliser l'outil 'offer_match' avec: "
        "\n- percentage: un nombre entre 0 et 100 "
        "\n- points_forts: liste des compétences qui matchent (ex: 'Python, SQL, Machine Learning, Communication') "
        "\n- points_faibles: liste des compétences manquantes (ex: 'Power BI, RGPD, Gestion de bases de données') "
        "\n\nNE PAS écrire un rapport long. JUSTE appeler l'outil avec ces 3 paramètres. "
        "\nL'outil se chargera du formatage."
    ),
    "tools": [offer_match],
}   

@tool
def write_text(content: str) -> str:
    """Rédige la lettre de motivation ou le mail."""
    return content

writer_subagent = {
    "name": "writer-agent",
    "description": "Rédige une lettre de motivation professionnelle",
    "system_prompt": (
        "Tu es un rédacteur expert en lettres de motivation et mail pour candidater à une offre de travail. "
        "Tu reçois: (1) les informations du CV, (2) le contenu de l'offre, (3) l'analyse de match. "
        "Rédige une lettre de motivation ou mail convaincant en français qui: "
        "- Met en avant les compétences pertinentes du candidat "
        "- Fait le lien avec les exigences de l'offre "
        "- Est structurée professionnellement "
        "- Montre la motivation et l'adéquation au poste "
        "Utilise l'outil 'write_text' pour retourner le contenu textuel complet."
    ),
    "tools": [write_text],
}

multi_agent = create_deep_agent(
    model=model,
    subagents=[retrieve_subagent, offer_subagent, match_subagent, writer_subagent],
    system_prompt=(
        "Tu es un coordinateur de candidature. Exécute DANS L'ORDRE: "
        "\n1. retrieve-agent → Récupère TOUTES les infos du CV "
        "\n2. offer-agent → Extrait l'offre depuis l'URL "
        "\n3. match-agent → Calcule le pourcentage de match (il DOIT utiliser l'outil offer_match) "
        "\n4. writer-agent → Rédige la lettre de motivation  ou le mail de candidature "
        "\n\nPrésente ensuite le résultat final avec: "
        "\n- Le score de match "
        "\n- La lettre de motivation "
    ),
    # memory=None,
    middlewares=[],
)

# Test avec l'URL
if __name__ == "__main__":
    url_offre = "https://www.welcometothejungle.com/fr/companies/datascientest/jobs/data-analyst-intelligence-artificielle-alternance-h-f_puteaux"

    result = multi_agent.invoke(
        {"messages":[{
            "role": "user",
            "content": f"Analyse l'offre d'emploi sur ce site: {url_offre}. Compare avec le CV dans la base de données et rédige une lettre de motivation."
        }]}
    )

    print(result["messages"][-1].content)
