import os
import time
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from deepagents import create_deep_agent

print("DÉMARRAGE DE L'AGENT DE CARRIÈRE (avec protection rate limit)")
print("="*80)

load_dotenv(override=True)
os.environ.setdefault('USER_AGENT', 'CareerAgent/1.0 (Python script for job matching)')

# Configuration avec température réduite pour économiser tokens
model = ChatMistralAI(
    model="mistral-small-latest", 
    api_key=os.getenv("MISTRALAI_API_KEY"),
    temperature=0.3  # Réponses plus déterministes, moins de tokens
)
embedder = MistralAIEmbeddings(model="mistral-embed", api_key=os.getenv("MISTRALAI_API_KEY"))

# Chargement de la base vectorielle existante
current_dir = os.getcwd()
db_dir = os.path.join(current_dir, "data", "db")

print(f"\nChargement de la base depuis: {db_dir}")
db = Chroma(persist_directory=db_dir, embedding_function=embedder)
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 5})
print("Base de données chargée!")

# Tool 1: Recherche dans le CV
@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Recherche des informations dans le CV."""
    print(f"Recherche: '{query}'")
    time.sleep(0.5)  # Petit délai pour éviter rate limit
    retrieve_docs = retriever.invoke(query)
    serialized = "\n\n".join(
        f"Contenu : {doc.page_content}" for doc in retrieve_docs
    )
    print(f"Trouvé {len(retrieve_docs)} résultats")
    return (serialized, retrieve_docs)

# Tool 2: Extraction d'URL
@tool
def extract_text_url(url: str) -> str:
    """Extrait le texte d'une page web."""
    print(f"Extraction de: {url[:50]}...")
    time.sleep(0.5)  # Petit délai
    try:
        loader = WebBaseLoader(url)
        docs = loader.load()
        content = docs[0].page_content[:5000]  # Limiter à 5000 chars pour économiser tokens
        print(f"Contenu extrait ({len(content)} caractères)")
        return content
    except Exception as e:
        error = f"Erreur: {str(e)}"
        print(f"{error}")
        return error

# Tool 3: Match CV/Offre
@tool
def offer_match(evaluation: str, percentage: int) -> str:
    """Calcule la correspondance entre CV et offre."""
    print(f"   Match: {percentage}%")
    time.sleep(0.5)  # Petit délai
    return f"CORRESPONDANCE: {percentage}%\n\nÉVALUATION:\n{evaluation}"

# Tool 4: Rédaction
@tool
def write_text(content: str) -> str:
    """Rédige la lettre de motivation."""
    print(f"   Lettre rédigée ({len(content)} caractères)")
    time.sleep(0.5)  # Petit délai
    return content

# Subagents avec prompts plus concis pour économiser tokens
retrieve_subagent = {
    "name": "retrieve-agent",
    "description": "Extrait les infos du CV",
    "system_prompt": (
        "Recherche dans le CV avec l'outil 'retrieve': "
        "compétences, expérience, formation, langues. "
        "Retourne un résumé concis."
    ),
    "tools": [retrieve],
}

offer_subagent = {
    "name": "offer-agent",
    "description": "Extrait l'offre d'emploi",
    "system_prompt": (
        "Extrais le contenu de l'offre avec 'extract_text_url'. "
        "L'URL est dans la demande."
    ),
    "tools": [extract_text_url],
}

match_subagent = {
    "name": "match-agent",
    "description": "Analyse le match CV/offre",
    "system_prompt": (
        "Compare CV et offre. "
        "Utilise 'offer_match' avec pourcentage (0-100) et évaluation brève."
    ),
    "tools": [offer_match],
}

writer_subagent = {
    "name": "writer-agent",
    "description": "Rédige la lettre de motivation",
    "system_prompt": (
        "Rédige une lettre de motivation concise en français. "
        "Structure: introduction, compétences, motivation, conclusion. "
        "Max 300 mots. Utilise 'write_text'."
    ),
    "tools": [write_text],
}

# Agent principal
print("\nCréation de l'agent multi-agents...")
multi_agent = create_deep_agent(
    model=model,
    subagents=[retrieve_subagent, offer_subagent, match_subagent, writer_subagent],
    system_prompt=(
        "Coordonne l'analyse: "
        "1. retrieve-agent (CV) "
        "2. offer-agent (URL dans demande) "
        "3. match-agent (analyse) "
        "4. writer-agent (lettre) "
    )
)
print("Agent créé!")

# Exécution
url_offre = "https://www.welcometothejungle.com/fr/companies/datascientest/jobs/data-analyst-intelligence-artificielle-alternance-h-f_puteaux"

print(f"\nAnalyse de l'offre:")
print(f"   {url_offre}")
print("\nATTENTION: Peut prendre 2-3 minutes pour éviter rate limit...")
print("="*80 + "\n")

try:
    result = multi_agent.invoke({
        "messages": [{
            "role": "user",
            "content": f"Analyse: {url_offre}. Compare avec CV et rédige lettre courte."
        }]
    })

    print("\n" + "="*80)
    print("RÉSULTAT FINAL")
    print("="*80)

    # Extraire le dernier message de l'agent
    if 'messages' in result:
        last_message = result['messages'][-1]
        if hasattr(last_message, 'content'):
            print(last_message.content)
        else:
            print(last_message)
    else:
        print(result)

    print("\n" + "="*80)
    print("TERMINÉ!")
    print("="*80)
    
except Exception as e:
    if "429" in str(e) or "rate" in str(e).lower():
        print("\n" + "="*80)
        print("ATE LIMIT ATTEINT!")
        print("="*80)
        print("\nSolutions:")
        print("   1. Attendez 5-10 minutes")
        print("   2. Vérifiez votre plan API Mistral")
        print("   3. Utilisez un tier payant pour plus de requêtes")
        print("\nAstuce: Lancez le script qu'une seule fois!")
    else:
        print(f"\nErreur: {e}")
        import traceback
        traceback.print_exc()
