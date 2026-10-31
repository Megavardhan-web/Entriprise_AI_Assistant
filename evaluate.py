import json
from rag import answer_question


with open("evaluation_questions.json", "r", encoding="utf-8") as file:
    test_questions = json.load(file)


def check_answer(result, test):
    answer = result.get("answer", "").lower()
    sources = result.get("sources", [])
    expected_behavior = test.get("expected_behavior", "answer")

    source_names = [
        source.get("document", "").lower()
        for source in sources
    ]

    # Check whether the expected source was retrieved
    expected_source = test.get("expected_source", "").lower()

    if expected_source:
        source_ok = any(
            expected_source in source_name
            for source_name in source_names
        )
    else:
        source_ok = True

    # Check behavior rather than exact wording
    if expected_behavior == "answer":
        expected_answer = test.get("expected_answer", "").lower()
        answer_ok = expected_answer in answer

    elif expected_behavior == "detect_conflict":
        # The answer should mention both policy values
        mentions_three = (
            "3 remote" in answer
            or "three remote" in answer
            or "3 days" in answer
            or "three days" in answer
        )

        mentions_two = (
            "2 remote" in answer
            or "two remote" in answer
            or "2 days" in answer
            or "two days" in answer
        )

        mentions_conflict = any(
            word in answer
            for word in ["conflict", "disagree", "earlier version", "older policy"]
        )

        answer_ok = mentions_three and (
            mentions_two or mentions_conflict
        )

    elif expected_behavior == "refuse":
        refusal_phrases = [
            "couldn't find enough information",
            "not enough information",
            "cannot answer",
            "can't answer",
            "not provided in the documents",
            "insufficient evidence",
        ]

        answer_ok = any(
            phrase in answer
            for phrase in refusal_phrases
        )

    else:
        answer_ok = False

    return answer_ok, source_ok


passed = 0

for index, test in enumerate(test_questions, start=1):
    result = answer_question(test["question"])

    answer_ok, source_ok = check_answer(result, test)
    passed_test = answer_ok and source_ok

    if passed_test:
        passed += 1

    print(f"\nTest {index}: {'PASS' if passed_test else 'FAIL'}")
    print(f"Question: {test['question']}")
    print(f"Answer: {result.get('answer', '')}")
    print(f"Answer behavior correct: {answer_ok}")
    print(f"Source correct: {source_ok}")
    print(f"System status: {result.get('status', '')}")

print(f"\nFinal score: {passed}/{len(test_questions)}")