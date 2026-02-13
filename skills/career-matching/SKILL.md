---
name: career-matching
description: "Analyse la correspondance entre un CV et une offre d'emploi. Calcule un score de match pondéré et génère une lettre de motivation personnalisée. Utilise ce skill quand l'utilisateur demande d'analyser une candidature ou de comparer un profil avec une offre."
---

# Skill : Career Matching & Cover Letter

## Objectif

Analyser la correspondance entre un CV et une offre d'emploi, calculer un score de match précis, et générer une lettre de motivation professionnelle et personnalisée.

---

## Méthodologie de Matching

### 1. Extraction et Catégorisation

**Du CV, extrais:**
- Compétences techniques (langages, frameworks, outils)
- Compétences soft (communication, autonomie, travail en équipe)
- Expériences (années, domaines, réalisations quantifiées)
- Formation (diplômes, certifications)
- Langues (avec niveaux)
- Projets concrets

**De l'offre, extrais:**
- Must-have (compétences obligatoires)
- Nice-to-have (compétences bonus)
- Soft skills recherchés
- Contexte (taille entreprise, secteur, culture)

### 2. Calcul du Score (Weighted Scoring)

**Formule:**
```
Score Total = (
    Technical Match × 40% +
    Experience Match × 25% +
    Soft Skills Match × 20% +
    Education Match × 10% +
    Languages Match × 5%
)
```

**Grille d'interprétation:**
- 90-100% : Excellent fit (candidat très fort)
- 80-89% : Very good fit (gaps mineurs)
- 70-79% : Good fit (développement nécessaire)
- 60-69% : Acceptable fit (gaps significatifs)
- <60% : Poor fit (désalignement majeur)

### 3. Catégorisation des Gaps

**Pour chaque compétence manquante, classe-la:**

1. **Easily Learnable** (1-2 semaines)
   - Exemple: Power BI quand le candidat connaît Matplotlib
   - Action suggérée: Cours en ligne + mini-projet

2. **Medium Effort** (1-3 mois)
   - Exemple: NLP quand le candidat connaît ML basics
   - Action suggérée: Cours structuré + projet personnel

3. **Long-term** (6+ mois)
   - Exemple: 5 ans d'expérience quand le candidat en a 1
   - Action suggérée: Trajectoire de croissance

4. **Non-negotiable**
   - Exemple: Certification obligatoire, exigence légale
   - Action suggérée: Indiquer si cela bloque la candidature

---

## Structure de la Lettre de Motivation

### Format Obligatoire

```
1. EN-TÊTE (5 lignes)
   - Coordonnées candidat
   - Coordonnées entreprise
   - Date
   - Objet

2. OUVERTURE (2-3 phrases)
   - Hook: Pourquoi CETTE entreprise/ce rôle
   - Intro brève: Qui vous êtes
   - Thèse: Pourquoi vous êtes un excellent fit

3. CORPS (3 paragraphes)
   
   § 1: Alignement Technique
   - Matcher vos compétences avec les requis du poste
   - Utiliser des EXEMPLES SPÉCIFIQUES de votre expérience
   - Montrer compréhension du rôle
   
   § 2: Expérience & Réalisations
   - Résultats CONCRETS: "Réduit le temps de traitement de 40%"
   - PAS: "Je suis travailleur"
   - Connecter aux défis de l'entreprise
   
   § 3: Motivation & Fit
   - Pourquoi CETTE entreprise (recherche mission/culture)
   - Comment vous ajoutez de la valeur au-delà du job description
   - Votre trajectoire de croissance

4. CLÔTURE (2-3 phrases)
   - Call to action (demande d'entretien)
   - Disponibilité
   - Formule professionnelle

5. SIGNATURE
```

### Règles d'Or

**✅ À FAIRE:**
- Voix active: "J'ai développé" PAS "J'ai été impliqué dans"
- Quantifier: "Analysé 10,000+ points de données" PAS "Analysé des données"
- Montrer progression: "De X à Y, j'ai appris Z"
- Mirror le langage de l'entreprise: Si ils disent "data-driven", utilisez "data-driven"
- Recherche entreprise: Mentionner projets/valeurs spécifiques

**❌ À ÉVITER:**
- Templates génériques: "Je vous écris pour exprimer mon intérêt..."
- Répéter le CV: La lettre ajoute du CONTEXTE, pas de la duplication
- Framing négatif: "Bien que je manque de X" → "Je suis enthousiaste d'apprendre X"
- Buzzwords vides: "Synergie", "Rockstar", "Ninja"
- Dépasser 1 page (400-500 mots max)

### Calibrage du Ton

| Type d'entreprise | Ton | Exemple d'ouverture |
|-------------------|-----|---------------------|
| Startup | Énergique, direct | "Votre mission de démocratiser l'éducation en IA résonne profondément..." |
| Corporate | Professionnel, structuré | "Avec 5 ans d'expérience en analyse de données et un doctorat..." |
| Non-profit | Mission-driven, chaleureux | "L'opportunité de contribuer à votre travail impactant en EdTech..." |
| Recherche | Académique, détaillé | "Ma recherche doctorale en science des polymères, combinée à..." |

---

## Format de Sortie

### Pour l'Analyse de Match

Utilise OBLIGATOIREMENT l'outil `offer_match` avec cette structure:

```python
offer_match(
    percentage=85,  # Score global
    strong_alignments="Python, SQL, Data Science, Communication, Autonomie",
    partial_matches="Visualisation (a Matplotlib mais pas Power BI - 2 semaines apprentissage)",
    missing_elements="NLP spécifique (peut apprendre avec cours + projet - 2 mois)",
    recommendations="1. Formation Power BI (Coursera, 2 semaines)\n2. Projet NLP personnel (2 mois)\n3. Mettre en avant PhD = 5 ans analyse de données"
)
```

### Pour la Lettre

Utilise OBLIGATOIREMENT l'outil `write_cover_letter` avec les 5 sections:

```python
write_cover_letter(
    opening="...",           # Hook + intro (2-3 phrases)
    paragraph_1="...",       # Technical alignment
    paragraph_2="...",       # Experience & achievements
    paragraph_3="...",       # Motivation & fit
    closing="..."            # Call to action
)
```

---

## Scénarios Spécifiques

### Reconversion Professionnelle

**Problème:** Candidat passe de Recherche → Data Science

**Solution:**
1. Emphaser compétences TRANSFÉRABLES (pensée analytique, manipulation de données)
2. Framer le PhD comme "5 ans d'expérience en analyse de données"
3. Montrer transition intentionnelle (cours, projets, certifications)
4. Adresser "pourquoi le changement" de façon proactive

### Surqualification

**Problème:** PhD pour poste junior

**Solution:**
1. Ne pas cacher les credentials, mais ne pas mener avec eux
2. Emphaser compétences PRATIQUES sur réalisations académiques
3. Expliquer motivation (apprentissage, croissance, mission entreprise)
4. Montrer que le rôle n'est pas "en dessous" de vous

### Gaps de Compétences

**Problème:** Manque 2-3 requis clés

**Solution:**
1. Reconnaître gaps BRIÈVEMENT
2. Emphaser compétences similaires/transférables
3. Montrer VOLONTÉ et PLAN d'apprentissage
4. Prouver capacité d'apprentissage rapide (reconversion, adoption tech)

---

## Checklist Qualité

Avant de finaliser, vérifier:

- [ ] Score de match justifié avec exemples spécifiques
- [ ] Lettre < 500 mots
- [ ] Pas de phrases génériques
- [ ] Recherche entreprise évidente
- [ ] Réalisations quantifiées incluses
- [ ] Gaps adressés constructivement
- [ ] Call to action clair
- [ ] Ton matche la culture entreprise
- [ ] Aucune faute
- [ ] Proposition de valeur unique du candidat claire

---

## Exemples

### Bon Output de Match

```
## ANALYSE DE MATCH

**SCORE: 85%**

### ✅ Alignements Forts (40/50 points)
- **Python & Data Science Stack**: Match parfait
  → CV montre 3+ ans avec Pandas, NumPy, Scikit-learn
  → Offre requiert Python pour manipulation de données ✓

- **SQL & Bases de données**: Alignement fort
  → Expérience PostgreSQL, MySQL (IMT Nord Europe)
  → Offre nécessite SQL pour requêtes ✓

### ⚠️ Matches Partiels (25/30 points)
- **Outils de Visualisation**: Gap dans outils spécifiques
  → A: Matplotlib, Seaborn (bibliothèques Python)
  → Besoin: Power BI ou Tableau
  → Action: Formation 2 semaines recommandée
```

---

**Version:** 1.0 (2025-02-13)
**Auteur:** Career Matching Skill
**Cas d'usage:** Analyse CV/offre, génération lettres de motivation
