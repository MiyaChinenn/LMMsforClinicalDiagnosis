import json
from collections import Counter

# Load input file
with open('high_relevance_questions_multi.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# Load output file
with open('generation_outputs_for_evaluation_multi.json', 'r', encoding='utf-8') as f:
    outputs = json.load(f)

# Count variants in questions
question_variants = Counter(q.get('variant') for q in questions)
output_variants = Counter(o.get('variant') for o in outputs)

print("=" * 60)
print("INPUT STATISTICS - HIGH_RELEVANCE_QUESTIONS_MULTI.JSON")
print("=" * 60)
print(f"Total questions: {len(questions)}")
print("\nQuestions by variant:")
for variant, count in sorted(question_variants.items(), key=lambda x: str(x[0])):
    print(f"  {variant}: {count}")

print("\n" + "=" * 60)
print("OUTPUT STATISTICS - GENERATION_OUTPUTS_FOR_EVALUATION_MULTI.JSON")
print("=" * 60)
print(f"Total outputs: {len(outputs)}")
print("\nOutputs by variant:")
for variant, count in sorted(output_variants.items(), key=lambda x: str(x[0])):
    print(f"  {variant}: {count}")

print("\n" + "=" * 60)
print("EXPECTED vs ACTUAL COMPARISON")
print("=" * 60)
print("\nExpected Output:")
print("  model_only: 84")
print("  rag_text_reranked: 84")
print("  rag_multimodal: 18")
print("  Total: 186")

print("\nActual Output:")
print(f"  model_only: {output_variants.get('model_only', 0)}")
print(f"  rag_text_reranked: {output_variants.get('rag_text_reranked', 0)}")
print(f"  rag_multimodal: {output_variants.get('rag_multimodal', 0)}")
print(f"  Total: {len(outputs)}")

print("\n" + "=" * 60)
print("MATCH STATUS")
print("=" * 60)
expected = {'model_only': 84, 'rag_text_reranked': 84, 'rag_multimodal': 18}
match = True
for variant, exp_count in expected.items():
    actual_count = output_variants.get(variant, 0)
    status = "PASS" if actual_count == exp_count else "FAIL"
    print(f"[{status}] {variant}: Expected {exp_count}, Got {actual_count}")
    if actual_count != exp_count:
        match = False

print(f"\nTotal match: Expected 186, Got {len(outputs)} - {'PASS' if len(outputs) == 186 else 'FAIL'}")
print(f"\n{'✓ ALL EXPECTATIONS MET!' if match and len(outputs) == 186 else '✗ EXPECTATIONS NOT MET'}")
