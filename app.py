import csv
import difflib
import streamlit as st

# ----- LOAD DATASET -----
def load_dataset(filename):
    data = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) < 3:
                continue
            data.append({
                'question': row[0].lower().strip(),
                'topic': row[1].lower().strip(),
                'answer': row[2].strip()
            })
    return data

# ----- SEARCH ANSWER -----
def search_answer(question, dataset):
    question = question.lower().strip()
    questions_list = [entry['question'] for entry in dataset]
    close_matches = difflib.get_close_matches(question, questions_list, n=3, cutoff=0.5)

    if close_matches:
        st.markdown("### 🔍 Similar Questions:")
        for i, match in enumerate(close_matches, 1):
            score = difflib.SequenceMatcher(None, question, match).ratio()
            st.markdown(f"<div class='bubble'>{i}. {match} (Confidence: {int(score * 100)}%)</div>", unsafe_allow_html=True)

        best_match = close_matches[0]
        for entry in dataset:
            if entry['question'] == best_match:
                return f"✅ Best Answer (Confidence: {int(score * 100)}%):\n\n{entry['answer']}"
    return None

# ----- SAVE NEW QUESTION -----
def save_new_question(user_question, filename="new_questions.csv"):
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([user_question])
    st.success("💾 Question saved for future training!")

# ----- LOAD DATA -----
dataset = load_dataset('DATA SET.csv')

# ----- CUSTOM CSS -----
st.markdown("""
    <style>
    .bubble {
        background: linear-gradient(145deg, #e6e6e6, #ffffff);
        box-shadow: 6px 6px 12px #d1d1d1, -6px -6px 12px #ffffff;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        font-size: 16px;
    }

    .response {
        background: #f9f9ff;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 8px 8px 15px rgba(0,0,0,0.1);
        font-size: 18px;
        line-height: 1.5;
    }

    .center-text {
        text-align: center;
    }

    </style>
""", unsafe_allow_html=True)

# ----- UI -----
st.title("🌐 AI Q&A Assistant")
st.markdown("<div class='center-text'>Ask me anything from the dataset. Let's make learning beautiful ✨</div>", unsafe_allow_html=True)

user_question = st.text_input("💬 Type your question below:")

if st.button("🚀 Get Answer"):
    if user_question.strip():
        answer = search_answer(user_question, dataset)
        if answer:
            st.markdown(f"<div class='response'>{answer}</div>", unsafe_allow_html=True)
        else:
            st.warning("🤔 Sorry, I don't have an answer for that.")
            if st.checkbox("✅ Save this question for future learning?"):
                save_new_question(user_question)
    else:
        st.error("Please type a valid question.")
