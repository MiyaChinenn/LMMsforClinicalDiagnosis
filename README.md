# Large Multimodal Models for Clinical Diagnosis

Built AI-powered diagnostic support system for tropical diseases using multimodal RAG and Fine-tune with dual-source knowledge base from structured clinical cases and disease references.

## Project Overview
- **Goal**: Assist clinicians with differential diagnosis and management suggestions for tropical and infectious diseases.
- **Approach**: Combine text + medical images with multimodal RAG for evidence retrieval and fine-tune LMMs for domain adaptation.
- **Scope**: Tropical/infectious cases; supports clinical narratives, labs, and imaging.

## Objectives
- Triage and diagnostic support grounded in curated tropical/infectious disease data.
- Expand expertise in healthcare AI, LLMs/LMMs, and multimodal reasoning.
- Strengthen software engineering, project management, and interdisciplinary skills (critical thinking, problem solving, decision making).

## Methods
- **Multimodal RAG**: Retrieve clinical cases and visuals; re-rank for relevance; feed into LMMs for grounded answers.
- **Model Adaptation (Fine-tune)**: Domain-specific tuning on curated Q&A pairs to improve clinical accuracy.

## Data & Modalities
- **Clinical cases**: Structured text (history, vitals, labs, diagnosis, management).
- **Images**: Radiology and clinical photos aligned to cases.
- **Knowledge base**: Tropical/infectious disease references for retrieval grounding.

## Deliverables
- Diagnosis support system for tropical/infectious diseases (language + image inputs).
- Multimodal models: base LMM + fine-tuned variants.
- Project documentation (use cases, data, models), technical report, and Agile/DevOps artifacts.

## Module Info
- Type: Project | Credits: 10 | Weekly hours: 4
- Author: TRAN Duc Khanh | Faculty of Engineering, Vietnamese–German University

## Workstreams (High Level)
- **Data**: Collect/clean clinical cases and images; align metadata.
- **Retrieval**: Build multimodal embeddings and FAISS index; implement re-ranking.
- **Modeling**: Multimodal RAG pipelines; fine-tune for domain adaptation.
- **Evaluation**: Compare model-only vs. RAG (text + multimodal); measure diagnostic quality.
- **Engineering**: CI/CD, experiment tracking, and deployment readiness.

## Stack
- PyTorch, HuggingFace, LLaVA, FAISS, BioClinicalBERT, CLIP, BitsAndBytesConfig, PIL, pandas, Jupyter, Google Colab, CUDA.