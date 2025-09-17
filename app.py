from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import os

app = Flask(__name__)
CORS(app)

study_data = {
    "math": [
        {"question": "2+2 क्या है?", "answer": "4"},
        {"question": "5×5 क्या है?", "answer": "25"},
        {"question": "10÷2 क्या है?", "answer": "5"}
    ],
    "science": [
        {"question": "पानी का chemical formula क्या है?", "answer": "H2O"},
        {"question": "हवा में oxygen की मात्रा कितनी है?", "answer": "21%"}
    ],
    "hindi": [
        {"question": "रामायण के रचयिता कौन हैं?", "answer": "वाल्मीकि"},
        {"question": "महाभारत के रचयिता कौन हैं?", "answer": "वेद व्यास"}
    ]
}

@app.route('/')
def home():
    return "Study Bot API Online है!"

@app.route('/api/subjects')
def get_subjects():
    return jsonify({"subjects": list(study_data.keys())})

@app.route('/api/questions/<subject>')
def get_questions(subject):
    if subject in study_data:
        return jsonify({
            "subject": subject,
            "questions": study_data[subject],
            "total_questions": len(study_data[subject])
        })
    else:
        return jsonify({"error": "Subject not found"}), 404

@app.route('/api/random')
def get_random_question():
    try:
        all_questions = []
        for subject_name, questions_list in study_data.items():
            for q in questions_list:
                all_questions.append({
                    "subject": subject_name,
                    "question": q["question"],
                    "answer": q["answer"]
                })
        
        if all_questions:
            random_question = random.choice(all_questions)
            return jsonify(random_question)
        else:
            return jsonify({"error": "No questions available"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/add_question', methods=['POST'])
def add_question():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        subject = data.get('subject')
        question = data.get('question')
        answer = data.get('answer')
        
        if not all([subject, question, answer]):
            return jsonify({"error": "Subject, question and answer are required"}), 400
        
        if subject not in study_data:
            study_data[subject] = []
        
        study_data[subject].append({
            "question": question,
            "answer": answer
        })
        
        return jsonify({
            "message": "Question successfully added!",
            "subject": subject,
            "new_question": question,
            "total_questions": len(study_data[subject])
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
