import difflib
import csv

def load_dataset(filename):
    dataset = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 3:
                question = row[0].strip().lower()
                explanation = row[2].strip()
                dataset.append({
                    'question': question,
                    'answer': explanation  # using explanation as the answer
                })
    return dataset

def search_answer(question, dataset):
    question = question.lower().strip()
    questions_list = [entry['question'] for entry in dataset]
    close_matches = difflib.get_close_matches(question, questions_list, n=3, cutoff=0.5)

    if close_matches:
        print("\nI found some similar questions:")
        for i, match in enumerate(close_matches, start=1):
            score = difflib.SequenceMatcher(None, question, match).ratio()
            print(f"{i}. \"{match}\" (Confidence: {int(score * 100)}%)")

        best_match = close_matches[0]
        for entry in dataset:
            if entry['question'] == best_match:
                score = difflib.SequenceMatcher(None, question, best_match).ratio()
                return f"\nBest Match Answer (Confidence: {int(score * 100)}%): {entry['answer']}"
    
    return None  # No match found

def save_new_question(user_question, filename="new_questions.csv"):
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([user_question])
    print("Your question has been saved for future improvement.\n")

if __name__ == "__main__":
    dataset = load_dataset('DATA SET.csv')
    print("Ask your question below. Type 'exit' or 'quit' to stop.\n")

    while True:
        user_q = input("Ask: ")
        if user_q.lower() in ['exit', 'quit']:
            print("Exiting. Come back soon, jaan!")
            break
        elif not user_q.strip():
            print("Please enter a valid question.")
            continue

        result = search_answer(user_q, dataset)
        if result:
            print(result)
        else:
            print("\nSorry, I don't have an answer for that.")
            choice = input("Would you like to save this question for future training? (yes/no): ")
            if choice.strip().lower() in ['yes', 'y']:
                save_new_question(user_q)
