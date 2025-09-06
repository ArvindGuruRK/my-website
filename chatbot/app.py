from flask import Flask, request, jsonify, render_template, send_from_directory, send_file
from flask_cors import CORS
import os
import json

app = Flask(__name__, static_folder='..', template_folder='..')
CORS(app)

# Load predefined Q&A data
def load_qa_data():
    qa_data = {
        "questions": [
            {
                "question": "who are you",
                "answer": "I'm Arvind R K, an AI developer focused on turning data into useful, human-centered products. I enjoy clean engineering, rapid prototyping, and shipping features that make a real impact. I'm currently pursuing my Bachelor's degree at Rajalakshmi Institute of Technology, Chennai."
            },
            {
                "question": "what are your skills",
                "answer": "My technical skills include:\n- Programming: Python, Java, C, SQL, R, HTML, CSS, JavaScript\n- Databases: MySQL, MongoDB\n- Data Analysis: Power BI, Tableau\n- AI/ML: LLMs, NLP, Computer Vision, Recommendation Systems\n- ML Stack: scikit-learn, pandas, NumPy, OpenCV\n- DevOps: Docker, GitHub, basic cloud deployment\n- Data: SQL, ETL, visualization with Power BI"
            },
            {
                "question": "what projects have you worked on",
                "answer": "I've worked on several projects including:\n1) AI Smart File System - LLM-powered semantic search and file operations (LLM, Vector DB, Python)\n2) Smart Home IoT - Connected sensors, control dashboard and automations (IoT, MQTT, Python)\n3) Emotion Detection - Facial/text emotion classification pipeline (CV, NLP, Python)\n4) Movie Recommender - Content-based recommendation using embeddings (Recsys, Python)"
            },
            {
                "question": "what is your education",
                "answer": "I'm pursuing my Bachelor's degree in Computer Science Engineering at Rajalakshmi Institute of Technology, Chennai (2021–2025), with a CGPA of 8.1. I previously studied at Velammal Vidhyashram CBSE, Chennai (2008-2021), with 77.8 percentage."
            },
            {
                "question": "what is your work experience",
                "answer": "My work experience includes:\n- AI Intern at Trident Solutions (Apr 2025 - May 2025) - Worked on LLM-integrated file system and semantic search\n- Data Science Project Intern at YBI Foundation (Sep 2024 - Nov 2024) - Developed movie recommendation system\n- Data Science Intern at NullClass (Aug 2024) - Worked on emotion detection, AI chatbot, and age face recognition"
            },
            {
                "question": "what are your hobbies",
                "answer": "I enjoy fitness activities like weight training and cardio, playing football and chess, exploring AI tools, and contributing to social causes and education initiatives."
            },
            {
                "question": "where are you based",
                "answer": "I'm based in Chennai, India."
            },
            {
                "question": "what is your contact information",
                "answer": "You can contact me via email at arvindguru83@gmail.com or phone at 8778901907. You can also check my LinkedIn profile at https://www.linkedin.com/in/arvind-rk-0a782a224 or GitHub at https://github.com/ArvindGuruRK."
            },
            {
                "question": "what are your achievements",
                "answer": "I've completed 3+ AI internships and worked on 12+ projects in AI, ML, and data science. I've developed skills in LLM applications, machine learning, data analysis, and software development. I also have certifications in Python Development, Data Science, Java in Sololearn, NPTEL Database Management, and IBM Gen AI."
            },
            {
                "question": "hello",
                "answer": "Hello! I'm a simple chatbot that can answer questions about Arvind. Feel free to ask me about his skills, projects, education, or work experience."
            },
            {
                "question": "hi",
                "answer": "Hi there! I'm a simple chatbot that can answer questions about Arvind. How can I help you today?"
            },
            {
                "question": "what is his summary",
                "answer": "Arvind is a motivated fresher seeking an IT role, with a solid foundation in various tools and technologies. He has gained hands-on experience through internships and personal projects, showcasing his ability to learn quickly and adapt. He's eager to apply his existing skills in an IT company and is committed to contributing to organizational growth while enhancing his knowledge and gaining valuable industry experience."
            },
            {
                "question": "what are his skills",
                "answer": "Arvind's technical skills include:\n- Programming: Python, SQL\n- Data Science: NumPy, Pandas, AI Models, LLM, Gen AI, Machine Learning, Matplotlib, scikit-learn\n- Databases: MySQL, Oracle SQL\n- Software Tools: GitHub, MySQL, Oracle SQL, Visual Studio, Power BI, Colab, Tableau, Excel\n- Languages: English, Tamil, Hindi"
            },
            {
                "question": "what projects has he worked on",
                "answer": "Arvind has worked on several projects including:\n1) AI File System (LLM RAG Architecture) - Developed an AI-powered file search engine using FastAPI, FAISS, HuggingFace embeddings, and Ollama Mistral for accurate semantic and keyword-based file retrieval (Apr 2025)\n2) Movie Recommendation System - Developed a personalized movie recommendation system using collaborative and content-based filtering techniques with Pandas, NumPy, Scikit-learn, Matplotlib, and Seaborn (Nov 2024)\n3) Emotion Detection - Developed a system to classify emotions from text and facial expressions using Keras, TensorFlow, NumPy, and OpenCV (Dec 2024)"
            },
            {
                "question": "what is his education",
                "answer": "Arvind is pursuing his Bachelor of Engineering in Computer Science at Rajalakshmi Institute of Technology, Chennai (2021-2025), with a CGPA of 8.1. He previously studied at Velammal Vidhyashram CBSE, Chennai (2008-2021), with 77.8 percentage in X and XII."
            },
            {
                "question": "what is his work experience",
                "answer": "Arvind's professional experience includes:\n- Artificial Intelligence Intern at Trident Solutions (Apr 2025 - May 2025) - Built a smart file search engine with semantic search, keyword retrieval, and AI-powered document querying using FastAPI and HuggingFace embeddings\n- Data Science Project Intern at YBI Foundation (Sep 2024 - Nov 2024) - Developed a movie recommendation system and implemented logistic regression for movie classification\n- Data Science Intern at NullClass (Aug 2024) - Engaged in hands-on projects including emotion detection, AI chatbot development, and age face recognition"
            },
            {
                "question": "where is he based",
                "answer": "Arvind is based in Chennai, India."
            },
            {
                "question": "what is his contact information",
                "answer": "You can contact Arvind via email at arvindguru83@gmail.com or phone at 8778901907. You can also check his LinkedIn profile or GitHub at https://github.com/ArvindGuruRK."
            },
            {
                "question": "what are his achievements",
                "answer": "Arvind has completed multiple AI internships and worked on numerous projects in AI, ML, and data science. He has certifications in Python Development, Data Science, Java in Sololearn, NPTEL Database Management, and IBM Gen AI."
            },
            {
                "question": "what certificates does he have",
                "answer": "Arvind has several certificates including:\n- Python Development\n- Data Science\n- Java in Sololearn\n- NPTEL Database Management\n- Project Certificate\n- IBM Gen AI"
            }
        ]
    }
    return qa_data

# Find the best matching question and return its answer
def find_answer(user_query):
    qa_data = load_qa_data()
    user_query = user_query.lower().strip()
    
    # Direct match first
    for qa in qa_data["questions"]:
        if user_query == qa["question"].lower():
            return qa["answer"]
    
    # Partial match (contains the question)
    for qa in qa_data["questions"]:
        if qa["question"].lower() in user_query:
            return qa["answer"]
    
    # Keyword matching with improved scoring
    best_match = None
    highest_score = 0
    
    # Define important keywords for each topic
    topic_keywords = {
        "identity": ["who", "you", "yourself", "name", "about", "arvind", "summary", "profile"],
        "skills": ["skills", "abilities", "technologies", "programming", "languages", "tools", "tech", "stack", "know"],
        "projects": ["projects", "portfolio", "work", "built", "created", "developed", "applications", "apps"],
        "education": ["education", "degree", "university", "college", "school", "study", "studied", "academic", "qualification"],
        "experience": ["experience", "work", "job", "internship", "intern", "company", "career"],
        "location": ["where", "located", "based", "live", "city", "country", "from"],
        "contact": ["contact", "email", "phone", "linkedin", "github", "reach", "connect"],
        "achievements": ["achievements", "awards", "accomplishments", "recognition", "certifications", "certificates"]
    }
    
    # Check for 'he' pronoun questions
    if "he" in user_query.split() or "his" in user_query.split():
        # Check for direct matches with 'he' or 'his' questions
        for qa in qa_data["questions"]:
            if qa["question"].lower().startswith("what is his") or qa["question"].lower().startswith("what are his") or qa["question"].lower().startswith("where is he"):
                if qa["question"].lower() in user_query:
                    return qa["answer"]
    
    # Check if query contains topic keywords
    matched_topics = []
    for topic, keywords in topic_keywords.items():
        for keyword in keywords:
            if keyword in user_query:
                matched_topics.append(topic)
                break
    
    # If we matched topics, prioritize questions related to those topics
    if matched_topics:
        for qa in qa_data["questions"]:
            question = qa["question"].lower()
            score = 0
            
            # Check if question matches any of our identified topics
            for topic in matched_topics:
                for keyword in topic_keywords[topic]:
                    if keyword in question:
                        score += 1
                        
            # Boost score for pronoun matching (he/his vs you/your)
            if ("he" in user_query.split() or "his" in user_query.split()) and ("he" in question.split() or "his" in question.split()):
                score += 3
            elif ("you" in user_query.split() or "your" in user_query.split()) and ("you" in question.split() or "your" in question.split()):
                score += 3
            
            if score > highest_score:
                highest_score = score
                best_match = qa["answer"]
    
    # If no topic match, fall back to simple word overlap
    if not best_match:
        for qa in qa_data["questions"]:
            question_words = set(qa["question"].lower().split())
            query_words = set(user_query.split())
            common_words = question_words.intersection(query_words)
            
            if len(common_words) > highest_score:
                highest_score = len(common_words)
                best_match = qa["answer"]
    
    if best_match and highest_score > 0:
        return best_match
    
    return "I'm sorry, I don't have information about that. Try asking about Arvind's skills, projects, education, work experience, location, contact information, certificates, or achievements. You can use either 'what are your skills' or 'what are his skills' style questions."

@app.route("/")
def index():
    try:
        return send_file(os.path.join("..", "index.html"))
    except FileNotFoundError:
        return "Index file not found", 404

@app.route("/<path:filename>")
def serve_static(filename):
    # Serve static files from the parent directory
    try:
        return send_from_directory("..", filename)
    except FileNotFoundError:
        return f"File {filename} not found", 404

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    query = data.get("prompt", "")
    
    if not query:
        return jsonify({"response": "Please provide a question."})
    
    answer = find_answer(query)
    return jsonify({"response": answer})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)