# Multimodal Medical RAG System
## Evidence-Based Architecture & Metrics

---

## Slide 1: RAG Processing Pipeline & Model Architecture

### 🔄 **Complete RAG Processing Flow**

```
Query → Embedding (1792D) → RAG Retrieval → Model → Generate Answer (With RAG)
                     ↓                    ↓
                FAISS Search           Generate Answer (No RAG)
                     ↓
              Cross-Encoder Rerank
```

### 📊 **Pipeline Components**

#### **Embedding Stage:**
- **Input**: Text query + optional images
- **Models**: BioClinicalBERT (768D) + CLIP Text (512D) + CLIP Image (512D)
- **Output**: Fused 1792D embedding vector
- **Section Weights**: Applied during BioClinicalBERT processing

#### **RAG Retrieval Stage:**
- **FAISS Search**: k=10 initial candidates using cosine similarity
- **Cross-Encoder Rerank**: ms-marco-MiniLM-L-6-v2 for final k=3
- **Combined Scoring**: α=0.7 × FAISS + 0.3 × CrossEncoder (Karpukhin et al., 2020)

#### **Generation Models:**
- **Generation Model**: llava-hf/llava-v1.6-mistral-7b-hf (4-bit quantized)
- **Re-ranking Model**: cross-encoder/ms-marco-MiniLM-L-6-v2
- **Three Variants**: Model-only, RAG+Text, RAG+Multimodal

### ⚖️ **Embedding Weights Configuration**

```python
# Section Weights (Applied to BioClinicalBERT)
section_weights = {
    "final_diagnosis": 3.0,
    "differential_diagnosis": 2.0, 
    "management_and_clinical_course": 2.0,
    "labs_and_diagnostics": 1.2,
    "history_of_present_illness": 3.0,
    "physical_exam": 0.8,
    "exposure_and_epidemiology": 3.0,
    "vitals": 0.5,
    "patient_information": 0.5,
    "chief_complaint": 1.0
}

# Dynamic Fusion Weights
text_only_weights = [2.0, 0.75, 0.25]  # [BioBERT, CLIP_text, CLIP_image(zeros)]
multimodal_weights = [1.85, 0.75, 0.4]  # [BioBERT, CLIP_text, CLIP_image(if yes)]
multimodal_weights = [2.0, 0.75, 0.25]  # [BioBERT, CLIP_text, CLIP_image(if no)]

```

## Slide 2: Model Selections & Processing Results

### 🎯 **Evidence-Based Model Selections**

#### **Generation Model: llava-hf/llava-v1.6-mistral-7b-hf**
- **Source**: Liu et al. (2024) - "Improved Baselines with Visual Instruction Tuning"
- **Citation**: Liu, H., Li, C., Wu, Q., & Lee, Y. J. (2024). Visual instruction tuning. *Advances in Neural Information Processing Systems*.
- **Link**: https://arxiv.org/abs/2304.08485
- **Evidence**: State-of-the-art multimodal reasoning, handles medical images effectively
- **4-bit Quantization**: Memory efficiency (16GB→4GB) via BitsAndBytesConfig

#### **Re-ranking Model: cross-encoder/ms-marco-MiniLM-L-6-v2**
- **Source**: Reimers & Gurevych (2019) - "Sentence-BERT"
- **Evidence**: 15-25% improvement in passage ranking vs bi-encoder only
- **Implementation**: Text-only cross-encoder for passage relevance scoring


## Slide 3: Pipeline Validation & Performance Metrics

#### **Generation Comparison Results**

| Test Case | Variant | Context | Score | Images Processed |
|-----------|---------|---------|-------|-----------------|
| Lassa Fever | RAG+Text | 3 cases | [-1.964, -1.964, -2.282] | 0 |
| Lassa Fever | RAG+Multimodal | 3 cases | [-1.964, -1.964, -2.282] | 0 |
| Cardiac Case | RAG+Text | 3 cases | [-2.134, -2.229, -2.331] | 0 |
| Cardiac Case | RAG+Multimodal | 3 cases | [-2.165, -2.201, -2.302] | 2 X-rays |

---

## References

1. **Alsentzer, E., Murphy, J., Boag, W., Weng, W. H., Jindi, D., Naumann, T., & McDermott, M.** (2019). Publicly available clinical BERT embeddings. *Proceedings of the 2nd Clinical Natural Language Processing Workshop*, 72-78. https://aclanthology.org/W19-1909/

2. **Chapman, W. W., Nadkarni, P. M., Hirschman, L., D'avolio, L. W., Savova, G. K., & Uzuner, O.** (2011). Overcoming barriers to NLP for clinical text: the role of shared tasks and the need for additional creative solutions. *Journal of the American Medical Informatics Association*, 18(5), 540-543. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3168328/

3. **Karpukhin, V., Oguz, B., Min, S., Lewis, P., Wu, L., Edunov, S., ... & Yih, W. T.** (2020). Dense passage retrieval for open-domain question answering. *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing*, 6769-6781. https://arxiv.org/abs/2004.04906

4. **Kassirer, J. P.** (1989). Diagnostic reasoning. *New England Journal of Medicine*, 320(21), 1459-1462. https://www.nejm.org/doi/full/10.1056/NEJM198909073211007

4. **Moor, M., Huang, Q., Wu, S., Yasunaga, M., Zakka, C., Dalmia, A., ... & Leskovec, J.** (2023). Foundation models for generalist medical artificial intelligence. *Nature*, 616(7956), 259-265. https://www.nature.com/articles/s41586-023-05881-4

5. **Radford, A., Kim, J. W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., ... & Sutskever, I.** (2021). Learning transferable visual representations from natural language supervision. *International conference on machine learning*, 8748-8763. https://arxiv.org/abs/2103.00020

6. **Rajkomar, A., Oren, E., Chen, K., Dai, A. M., Hajaj, N., Hardt, M., ... & Dean, J.** (2018). Scalable and accurate deep learning with electronic health records. *npj Digital Medicine*, 1(1), 18. https://www.nature.com/articles/s41746-018-0029-1

7. **Reimers, N., & Gurevych, I.** (2019). Sentence-BERT: Sentence embeddings using siamese BERT-networks. *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing*, 3982-3992. https://arxiv.org/abs/1908.10084

8. **Rosenbloom, S. T., Denny, J. C., Xu, H., Lorenzi, N., Stead, W. W., & Johnson, K. B.** (2011). Data from clinical notes: a perspective on the tension between structure and flexible documentation. *Journal of the American Medical Informatics Association*, 18(2), 181-186. https://pubmed.ncbi.nlm.nih.gov/21347133/

9. **Singhal, K., Azizi, S., Tu, T., Mahdavi, S. S., Wei, J., Chung, H. W., ... & Natarajan, V.** (2023). Large language models encode clinical knowledge. *Nature*, 620(7972), 172-180. https://www.nature.com/articles/s41586-023-06291-2

10. **World Health Organization.** (2020). Control of neglected tropical diseases. WHO Technical Report Series, No. 949. https://www.who.int/publications/i/item/9789241549981

11. **Zhang, Y., Jiang, H., Miura, Y., Manning, C. D., & Langlotz, C. P.** (2022). Contrastive learning of medical visual representations from paired images and text. *Machine Learning for Healthcare Conference*, 2022.