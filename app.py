from flask import Flask, request, render_template, jsonify
import joblib
import requests
import pandas as pd
import numpy as np
import io
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
from pymongo import MongoClient
from flask_cors import CORS
import requests
import json
import os

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing


# Initialize blog_posts
blog_posts = []

# Load your trained models
diabetes_model = joblib.load('model.pkl')
medicine_model = joblib.load('medicine_model.pkl')
medicine_df = pd.read_csv('medicine_data.csv')

# Environment variable for SERPAPI API key
SERPAPI_API_KEY = '8dccb663327a4de4102deae65df095ebc2d229b549bf459de1bb8f5cad1bf4a0'

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['appointment_db']
time_slots_collection = db['time_slots']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/knowpvr')
def knowpvr():
    return render_template('knowyoupvr.html')

@app.route('/blogs')
def blogs():
    return render_template('blogs.html', blog_posts=blog_posts)

@app.route('/blog1')
def blog1():
    return render_template('blog1.html')


# //similary blog2 and 3
@app.route('/blog2')
def blog2():
    return render_template('blog2.html')

@app.route('/blog3')
def blog3():
    return render_template('blog3.html')


@app.route('/diabetes')
def diabetes_prediction_form():
    return render_template('diabetes.html')

@app.route('/add-blog', methods=['POST'])
def add_blog():
    try:
        title = request.form['title']
        content = request.form['content']
        if not title or not content:
            return jsonify({'error': 'Title and content are required'}), 400

        # Add the new blog post to the list
        blog_posts.append({'title': title, 'content': content})
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred while adding the blog'}), 500

@app.route('/calculate-health-score', methods=['POST'])
def calculate_health_score():
    try:
        data = request.get_json()
        BMI = float(data.get('BMI'))
        water_intake = float(data.get('water_intake'))
        smoking = data.get('smoking')
        walking = float(data.get('walking'))
        gender = data.get('gender')
        age = int(data.get('age'))
        sleep_quality = data.get('sleep_quality')
        exercise = data.get('exercise')
        stress_level = float(data.get('stress_level'))

        score = calculate_health_score_logic(BMI, water_intake, smoking, walking, gender, age, sleep_quality, exercise, stress_level)
        return jsonify(score)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def calculate_health_score_logic(BMI, water_intake, smoking, walking, gender, age, sleep_quality, exercise, stress_level):
    if walking > 50000:
        return {"error": "Invalid Input"}
    
    # Normalize BMI
    bmi_score = 1 if 18.5 <= BMI <= 24.9 else 0.5 if 25 <= BMI <= 29.9 else 0
    
    # Normalize Water Intake
    water_score = 1 if water_intake >= 3 else 0.5 if 2 <= water_intake < 3 else 0
    
    # Smoking score
    smoking_score = 1 if smoking.lower() == 'no' else 0
    
    # Normalize Walking
    walking_score = 1 if walking >= 10000 else 0.5 if 5000 <= walking < 10000 else 0
    
    # Gender score
    gender_score = 0.5 if gender.lower() in ['male', 'female'] else 0
    
    # Age score
    age_score = 1 if age < 30 else 0.5 if 30 <= age < 50 else 0
    
    # Sleep Quality score
    sleep_score = 1 if sleep_quality.lower() == 'excellent' else 0.5 if sleep_quality.lower() == 'good' else 0
    
    # Exercise score
    exercise_score = 1 if exercise.lower() == 'yes' else 0
    
    # Normalize Stress Level
    stress_score = (5 - stress_level) / 5
    
    # Weights
    weights = {
        'bmi': 0.15,
        'water': 0.10,
        'smoking': 0.15,
        'walking': 0.10,
        'gender': 0.05,
        'age': 0.05,
        'sleep': 0.15,
        'exercise': 0.10,
        'stress': 0.15
    }
    
    # Calculating weighted score
    score = (bmi_score * weights['bmi'] +
             water_score * weights['water'] +
             smoking_score * weights['smoking'] +
             walking_score * weights['walking'] +
             gender_score * weights['gender'] +
             age_score * weights['age'] +
             sleep_score * weights['sleep'] +
             exercise_score * weights['exercise'] +
             stress_score * weights['stress'])
    
    # Scaling score to 1-10 range
    final_score = score * 10
    
    return {"score": round(final_score, 2)}

@app.route('/predict-diabetes', methods=['POST'])
def predict_diabetes():
    try:
        data = request.get_json()
        print(f"Received data: {data}")  # Debugging: Print the received data

        preg = int(data['pregnancies'])
        glucose = float(data['glucose'])
        bp = float(data['blood_pressure'])
        st = float(data['skin_thickness'])
        insulin = float(data['insulin'])
        bmi = float(data['bmi'])
        dpf = float(data['diabetes_pedigree_function'])
        age = int(data['age'])

        features = [[preg, glucose, bp, st, insulin, bmi, dpf, age]]
        prediction = diabetes_model.predict(features)[0]

        result = 'Positive (Diabetes Detected)' if prediction == 1 else 'Negative (No Diabetes Detected)'
        return result
    except Exception as e:
        print(f"Error: {e}")  # Debugging: Print the error
        return "An error occurred while processing your request.", 500

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')


class SwasthSupportChatbot:
    def __init__(self):
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=AIzaSyAwqVXD03Dtm-r2FPaRnc-VHNR276zHiDQ"
        self.headers = {'Content-Type': 'application/json'}
        self.prompt = """You are स्वस्थ Support a Chatbot designed specifically for the medical/healthcare sector.
You should be able to answer any queries related to health.
You should have knowledge about all the diseases, their cures, symptoms, and what all medicines one should consume in order to get rid of the diseases.
The diseases can be minor or major you should be able to answer everything related to that.
You are deployed in the web and the advice you will give will be held into account for the patients, hence you are supposed to give only the precise/concise answers, no need for context only provide the required information to the user.
Also you are not a real doctor, just provide information if you can and if you are unable to answer the query just say you don't know, do not provide invalid information just for the sake of answering.
You can traverse internet to find best, accurate information and provide a clear and on point response.
One thing to keep in mind is that when any user asks who are you then you are supposed to say that you are स्वस्थ Support Chatbot and nothing else."""

    def get_response(self, user_input):
        data = {
            "contents": [
                {
                    "parts": [
                        {"text": self.prompt + "\nUser: " + user_input}
                    ]
                }
            ]
        }
        response = requests.post(self.api_url, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
            reply = result['candidates'][0]['content']['parts'][0]['text']
            return reply
        else:
            return "Error occurred while getting response from the API."

# Create an instance of the chatbot
chatbot = SwasthSupportChatbot()

@app.route('/send-message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        user_message = data.get('message')
        bot_message = chatbot.get_response(user_message)
        return jsonify({'response': bot_message})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'response': 'An error occurred while processing your request.'})
    

@app.route('/disease')
def disease_prediction_form():
    return render_template('disease-detection.html')

@app.route('/search', methods=['GET'])
def search():
    medicine_name = request.args.get('medicine_name')
    if not medicine_name:
        return jsonify({'error': 'Medicine name is required'}), 400

    try:
        response = requests.get(
            'https://serpapi.com/search',
            params={
                'api_key': SERPAPI_API_KEY,
                'q': medicine_name,
                'engine': 'google',
                'hl': 'en',
                'gl': 'us'
            }
        )
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred while fetching the data'}), 500

# Load the model for pneumonia detection
MODEL_SAVE_PATH = '/home/vansh/Downloads/codeworldhackthon/VGG16_pneumonia_epoch_5.h5'
loaded_model = load_model(MODEL_SAVE_PATH)

@app.route('/pneumonia', methods=['POST'])
def disease_prediction():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        img = load_img(io.BytesIO(file.read()), target_size=(224, 224))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        predictions = loaded_model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)
        class_labels = {0: 'Normal', 1: 'Pneumonia'}
        prediction_label = class_labels.get(predicted_class[0], 'Unknown')

        return jsonify({'prediction': prediction_label})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': f'An error occurred while processing the image'}), 500

@app.route('/appointment')
def appointment():
    states = ['California', 'Texas', 'New York']  # Replace with your actual states list
    return render_template('appointment.html', states=states)

@app.route('/get-cities', methods=['POST'])
def get_cities():
    state = request.json.get('state')
    cities = {
        'California': ['Los Angeles', 'San Francisco'],
        'Texas': ['Houston', 'Dallas'],
        'New York': ['New York City', 'Buffalo']
    }
    return jsonify(cities.get(state, []))

@app.route('/get-time-slots', methods=['POST'])
def get_time_slots():
    city = request.json.get('city')
    doctor = request.json.get('doctor')
    time_slots = time_slots_collection.find({'city': city, 'doctor': doctor})
    slots = [slot['time_slot'] for slot in time_slots]
    return jsonify(slots)

@app.route('/book-appointment', methods=['POST'])
def book_appointment():
    try:
        data = request.get_json()
        state = data['state']
        city = data['city']
        doctor = data['doctor']
        time_slot = data['time_slot']
        # Process the appointment booking logic here
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred while booking the appointment.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
