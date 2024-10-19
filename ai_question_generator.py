import os
from openai import OpenAI
from flask import Blueprint, request, jsonify
from flask_login import login_required

ai_question_bp = Blueprint('ai_question', __name__)

# Set up OpenAI API key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_questions(subject, grade_level, topic, num_questions=5):
    subjects = ["math", "science", "reading", "writing", "spelling", "reading comprehension"]
    grade_levels = ["K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

    if subject.lower() not in subjects:
        return [], "Invalid subject. Please choose from: " + ", ".join(subjects)

    if grade_level not in grade_levels:
        return [], "Invalid grade level. Please choose from: " + ", ".join(grade_levels)

    prompt = f"Generate {num_questions} diverse {grade_level} grade level questions about {subject} focusing on {topic}. Include a mix of question types (e.g., multiple choice, open-ended, problem-solving). Format the output as a numbered list."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates diverse and engaging educational questions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            n=1,
            temperature=0.8,
        )

        questions = response.choices[0].message.content.strip().split("\n")
        return questions, None
    except Exception as e:
        print(f"Error generating questions: {str(e)}")
        return [], "Failed to generate questions. Please try again."

@ai_question_bp.route('/generate_ai_questions', methods=['POST'])
@login_required
def generate_ai_questions():
    data = request.json
    subject = data.get('subject')
    grade_level = data.get('grade_level')
    topic = data.get('topic')
    num_questions = data.get('num_questions', 5)

    if not all([subject, grade_level, topic]):
        return jsonify({'error': 'Missing required fields'}), 400

    questions, error = generate_questions(subject, grade_level, topic, num_questions)

    if error:
        return jsonify({'error': error}), 400

    if questions:
        return jsonify({'questions': questions})
    else:
        return jsonify({'error': 'Failed to generate questions. Please try again.'}), 500

@ai_question_bp.route('/regenerate_ai_questions', methods=['POST'])
@login_required
def regenerate_ai_questions():
    return generate_ai_questions()
