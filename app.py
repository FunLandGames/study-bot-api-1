from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# Study data
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
    return "Study Bot API चल रही है!"

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

# Random question feature
@app.route('/api/random')
def get_random_question():
    try:
        # सभी questions एक list में collect करें
        all_questions = []
        for subject_name, questions_list in study_data.items():
            for q in questions_list:
                # हर question के साथ subject name भी add करें
                all_questions.append({
                    "subject": subject_name,
                    "question": q["question"],
                    "answer": q["answer"]
                })
        
        # Randomly एक question select करें
        if all_questions:
            random_question = random.choice(all_questions)
            return jsonify(random_question)
        else:
            return jsonify({"error": "No questions available"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add new question feature
@app.route('/api/add_question', methods=['POST'])
def add_question():
    try:
        # Request से data get करें
        data = request.get_json()
        
        # Data check करें
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        subject = data.get('subject')
        question = data.get('question')
        answer = data.get('answer')
        
        # Validation
        if not all([subject, question, answer]):
            return jsonify({"error": "Subject, question and answer are required"}), 400
        
        # New subject create करें अगर नहीं exists
        if subject not in study_data:
            study_data[subject] = []
        
        # New question add करें
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
    app.run(host='0.0.0.0', port=5000, debug=True)
