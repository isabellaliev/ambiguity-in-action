# ambiguity-in-action

This project aims to explore how ambiguity, modality, and performativity shape the legal discourse of Colombian decrees. 

This repo investigates the **silent work of verbs**, the **vagueness of legal recommendations**, and how **power operates through ambiguity**.

Folder Structure

- `/cleaned`: Preprocessed texts, standardized for analysis
- `/data`: Raw corpus files (scraped or manually collected)
- `/scripts`: Python notebooks (text cleaning, extraction, counting)
- `/outputs`: Visuals, counts, modality maps
- `README.md`: You are here :)

This repository supports my graduate research goals in computational linguistics and reflects my ongoing transition from humanities-based inquiry to applied data analysis.

┌────────────────────────────┐
│        Raw Text Corpus     │
│ (Legal docs, press, etc.) │
└────────────┬──────────────┘
             │
             ▼
┌────────────────────────────┐
│        Tokenization        │
│  (spaCy, NLTK, custom)     │
│  → Splits text into units  │
└────────────┬──────────────┘
             │
             ▼
┌────────────────────────────┐
│         Regex Rules        │
│  → Match modal verbs,      │
│    hedges, vague terms     │
│  → Transparent tagging     │
└────────────┬──────────────┘
             │
             ▼
┌────────────────────────────┐
│     Modality & Ambiguity   │
│         Tagging Layer      │
│  → Labels: epistemic,      │
│    deontic, hedging, etc.  │
└────────────┬──────────────┘
             │
             ▼
┌────────────────────────────┐
│      Frequency Counts      │
│  → How often tags appear   │
│  → Normalize across docs   │
└────────────┬──────────────┘
             │
             ▼
┌────────────────────────────┐
│   Co-occurrence Analysis   │
│  → Sliding window (e.g. 5) │
│  → PMI scores              │
│  → Graphs of associations  │
└────────────┬──────────────┘
             │
             ▼
┌────────────────────────────┐
│     Interpretive Layer     │
│  → Rhetorical strategies   │
│  → Institutional framing   │
│  → Silences & evasions     │
└────────────────────────────┘
