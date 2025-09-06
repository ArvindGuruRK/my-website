import json
import os

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
    
    return "I'm sorry, I don't have information about that. Try asking about Arvind's skills, projects, education, work experience, location, contact information, certificates, or achievements."

def handler(request):
    # Handle CORS preflight requests
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': ''
        }
    
    try:
        # Parse the request body
        body = request.get_json()
        query = body.get('prompt', '') if body else ''
        
        if not query:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({"response": "Please provide a question."})
            }
        
        answer = find_answer(query)
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({"response": answer})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({"response": f"Error: {str(e)}"})
        }
