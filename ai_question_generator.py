import os
import openai
from flask import Blueprint, request, jsonify
from flask_login import login_required

ai_question_bp = Blueprint('ai_question', __name__)

# Set up OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_questions(subject, grade_level, topic, num_questions=5):
    prompt = f"Generate {num_questions} {grade_level} grade level questions about {subject} focusing on {topic}. Format the output as a numbered list."

    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.7,
        )

        questions = response.choices[0].text.strip().split("\n")
        return questions
    except Exception as e:
        print(f"Error generating questions: {str(e)}")
        return []

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

    questions = generate_questions(subject, grade_level, topic, num_questions)

    if questions:
        return jsonify({'questions': questions})
    else:
        return jsonify({'error': 'Failed to generate questions'}), 500
