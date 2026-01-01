# Medical AI RAG System - Copilot Instructions

## Project Overview
This is a **multimodal medical RAG (Retrieval-Augmented Generation) system** that combines clinical case studies with disease knowledge to provide AI-powered medical assistance. The system processes tropical medicine cases with images, lab data, and comprehensive clinical narratives.

## Architecture Components

### 1. Dual Dataset Structure
- **Clinical Cases** (`extracted-clinical-dataset/`): 90+ real patient cases with structured JSON data, medical images, and clinical narratives
- **Disease Knowledge** (`ngocdataset/`): Comprehensive medical textbook chapters on tropical diseases
- Both use identical JSON schema but different content patterns (clinical vs. encyclopedic)

### 2. Multi-Model Embedding Pipeline
```python
# Core embedding models - DO NOT change without testing
bio_model_name = "emilyalsentzer/Bio_ClinicalBERT"  # 768D medical text
clip_model_name = "openai/clip-vit-base-patch32"    # 512D text + 512D image
final_dimension = 1792  # BioClinicalBERT(768) + CLIP_text(512) + CLIP_image(512)
```

### 3. Generation Models
- **Primary**: LLaVA v1.6 Mistral 7B for multimodal medical reasoning
- **Quantization**: 4-bit with BitsAndBytesConfig for memory efficiency
- **Re-ranking**: Cross-encoder for improved retrieval relevance

## Critical Development Patterns

### JSON Schema (Both Datasets)
```json
{
  "patient_information": "Clinical cases: real data | Knowledge: 'not reported'",
  "chief_complaint": "Clinical description | 'not reported'",
  "final_diagnosis": "Always populated with medical content",
  "disease_name_short": "Standardized disease name",
  "images": [{"file_name": "path", "caption": "description"}],
  "tables": [{"title": "", "headers": [], "rows": []}]
}
```

### Embedding Weight Strategy
```python
# Section importance weights for BioClinicalBERT
section_weights = {
    "final_diagnosis": 3.0,           # Highest priority
    "history_of_present_illness": 3.0,
    "exposure_and_epidemiology": 3.0,
    "differential_diagnosis": 2.0,
    "management_and_clinical_course": 2.0,
    "labs_and_diagnostics": 1.2,
    "patient_information": 0.5        # Lowest priority
}

# Multimodal fusion weights
fused = np.hstack([
    2.0 * bio_emb * source_multiplier,   # Core medical semantics
    0.75 * clip_text_emb,                # Text coherence
    0.25 * clip_image_emb                # Visual context
])
```

### Three-Variant Generation System
1. **Model-Only**: Pure LLaVA without retrieval
2. **RAG+Text**: Retrieved context + text-only generation
3. **RAG+Multimodal**: Retrieved context + images + full multimodal processing

## Key Development Workflows

### Building/Updating FAISS Index
```python
# Always use this pattern for consistent embeddings
def get_fused_text_embedding(text):
    bio_emb = embed_bio_text(text, mode="diagnosis")  # Choose mode carefully
    clip_text_emb = embed_clip_text(text)
    clip_image_emb = np.zeros((1, clip_image_dim))    # For text-only queries
    return np.hstack([2.0 * bio_emb, 0.75 * clip_text_emb, 0.25 * clip_image_emb])
```

### File Path Conventions
- **Clinical images**: `extracted_images/{case_folder}/page{N}_img{N}.jpeg`
- **NGOC images**: `images/{filename}` (if present)
- **JSON files**: Numbered cases `1---Patient-Description...json`
- **FAISS outputs**: `output/enhanced_medclip_index.faiss` + `enhanced_medclip_metadata.json`

### Error Handling Patterns
- Always check for "not reported" values in JSON fields
- Gracefully handle missing images with zero embeddings
- Use try/catch blocks around model inference calls
- Validate FAISS index dimensions before operations

## Testing Strategy
- **Test all three variants** for any generation changes
- **Validate retrieval diversity** (clinical vs. knowledge sources)
- **Check image loading** from both dataset structures
- **Monitor embedding dimensions** (must equal 1792)

## Performance Considerations
- Models use quantized weights for memory efficiency
- FAISS IndexFlatIP for exact cosine similarity
- Cross-encoder re-ranking adds latency but improves relevance
- Image processing is the bottleneck - optimize batch operations

## Integration Points
- **Kaggle paths**: Notebook assumes `/kaggle/input/` for datasets
- **Local development**: Update paths to match workspace structure
- **CUDA/CPU**: System automatically detects and adjusts device placement
- **Memory management**: Call `gc.collect()` and `torch.cuda.empty_cache()` between major operations

## Common Debugging Areas
- **Low similarity scores**: Check embedding normalization and dimension consistency
- **Image loading failures**: Verify path construction for both dataset types
- **Generation errors**: Ensure proper prompt formatting and token limits
- **FAISS crashes**: Validate vector dimensions match index configuration