from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

# Function to fetch questions from Open Trivia API
def fetch_questions():
    url = "https://opentdb.com/api.php?amount=5&type=multiple"
    response = requests.get(url)
    data = response.json()
    questions = data['results']
    return questions


# Index page
@app.route('/')
def index():
    return render_template('index.html')


# Quiz page
@app.route('/quiz', methods=['GET'])
def quiz():
    questions = fetch_questions()
    mapped_questions = []

    for q in questions:
        mapped_question = {}

        mapped_question['question'] = q['question']
        mapped_question['options'] = q['incorrect_answers'] + [q['correct_answer']]

        # Shuffle the options to avoid bias
        random.shuffle(mapped_question['options'])

        mapped_question['answer'] = q['correct_answer']

        mapped_questions.append(mapped_question)

    return render_template('quiz.html', questions=mapped_questions)


# Result page
@app.route('/result', methods=['POST'])
def result():
    questions_count = 5  # عدد الأسئلة الثابت
    score = 0
    
    # جلب الإجابات الصحيحة والمختارة لكل سؤال
    for i in range(questions_count):
        selected = request.form.get(f'question{i}')
        correct = request.form.get(f'correct{i}')
        
        if selected == correct:
            score += 1
    
    return render_template('result.html', score=score, total=questions_count)



if __name__ == "__main__":
    app.run(debug=True)