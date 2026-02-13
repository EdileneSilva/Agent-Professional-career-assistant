import streamlit as st
from career_agent import multi_agent

st.set_page_config(page_title="Career Agent", page_icon="📄")

st.title("🤖 Career Agent – Analyse CV / Offre")
st.write("Collez l’URL d’une offre d’emploi pour lancer l’analyse.")

url_offre = st.text_input(
    "🔗 URL de l’offre d’emploi",
    placeholder="https://www.exemple.com/offre"
)

if st.button("Analyser l’offre"):
    if not url_offre.strip():
        st.error("Merci de fournir une URL valide.")
    else:
        with st.spinner("Analyse en cours..."):
            result = multi_agent.invoke(
                {"messages": [{
                    "role": "user",
                    "content": f"""
Analyse l'offre d'emploi sur ce site: {url_offre}.
Compare avec le CV dans la base de données et rédige une lettre de motivation.
"""
                }]}
            )
            final_message = result["messages"][-1].content
        
        st.success("Analyse terminée ✅")
        st.markdown(final_message)
