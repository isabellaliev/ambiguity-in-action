# ambiguity-in-action

This computational linguistics project analyzes how linguistic ambiguity in Colombian legal decrees creates interpretive spaces that create interpretive ambiguity. Using corpus analysis, speech act theory and CDA, I examine modal verbs, performative constructions, and rhetorical vagueness in governmental discourse focusing on post-1965 security legislation. 

This repository supports my graduate research goals in computational linguistics and reflects my ongoing transition from humanities-based inquiry to applied data analysis. This methodology could extend to legal discourse analysis in other Latin American contexts and contribute to computational approaches in legal studies.

**Methods:**

- Iterative methodology development using pilot corpus of 3 decrees.
- Focus on annotation consistency and pattern identification before corpus expansion
- Manual validation of automated detection algorithms on small sample
- Text preprocessing with spaCy Spanish language models
- Modal verb detection using custom lexicons (deontic, epistemic, dynamic)
- Dependency parsing for syntactic ambiguity identification
- Statistical analysis of ambiguity patterns across decree types

**Current Status:**

**Phase 2:** Core Analysis Development. Creation of a Modal Verb detection system and Subjunctive mood detector. 

**Preliminary Findings:**

Initial analysis demonstrates feasibility of modal verb detection approach and reveals consistent patterns in authority delegation language.

**Folder Structure**

- `/data`: Raw and processed texts ready for parsing
- `/docs`: Theoretical frameworks and annotation guidelines
- `/notebooks`: Python notebooks 
- `/results`: Visuals, figures, tables
- `/src`: Evaluation, feature extraction, models, preprocessing and visualization python scripts
- `/tests`: Pending - for future reference
- `README.md`: You are here :)
- `requirements.txt`: Required libraries for reproduction

This project incorporates mathematical modeling to deepen the analysis. The *notebooks/math_applications* folder contains explorations applying graph theory, probability, and linear algebra to model relationships and patterns within the legal corpus.