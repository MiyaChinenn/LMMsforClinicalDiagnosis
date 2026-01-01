# Week Presentation Script - Medical AI RAG System
**Duration: ~20 seconds**


## Slide 1: Data Preparation - Medical Text Dataset (Tu)
**Duration: ~6-7 seconds**

"We prepared a medical text dataset from Hunter's Tropical Medicine textbook. We create different question types — diagnosis, symptoms, and treatment — so the model learns how doctors think and reason clinically."


## Slide 2: Data Preparation - Medical Image Dataset (Nguyen)
**Duration: ~6-7 seconds**

For the image processing, we generate questions about visual features because images contain diagnostic information that text alone cannot provide. Our questions focus on three aspects: interpreting what we see in the image, assessing severity from visual signs, and determining treatment based on imaging findings.

This output will be used for tokenization work later on the pipeline.



## Slide 3: RAG Processing - Multimodal Q-A Generation (Nguyen)
**Duration: ~7-8 seconds**

We designed the generation system with four different approaches:

On the one hand, we test pure model knowledge without any search, that could be processed with both text and image input. On the other hand, we use an embedding system with re-ranking support to find relevant clinical cases from our database, which could retrieve both text and image for multimodal reasoning.

This output will be used for rag evaluation work later on the pipeline.
