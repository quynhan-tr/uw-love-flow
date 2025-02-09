from flask import Flask, request, render_template, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session management

# Get the absolute path to the project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data.txt')

@app.route('/main')
def home():
    return render_template('main.html')

@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        session['name'] = request.form.get('name')
        session['discord'] = request.form.get('discord')
        return redirect(url_for('friendship_quiz'))
    return render_template('join.html')

@app.route('/friendship-quiz', methods=['GET', 'POST'])
def friendship_quiz():
    if request.method == 'POST':
        name = session.get('name')
        discord = session.get('discord')
        
        user_data = {
            'name': name,
            'discord_handle': discord,
            'mbti': request.form.get('mbti'),
            'preferred_gender': request.form.get('preferred-gender'),
            'other_gender': request.form.get('other-gender-input'),
            'communication_style': request.form.get('communication-style'),
            'weekend_activity': request.form.get('weekend-activity'),
            'preference': request.form.get('preference'),
            'movie_genres': request.form.getlist('movie-genres'),
            'party_frequency': request.form.get('party-frequency'),
            'relationship_components': request.form.getlist('relationship-components'),
            'unicorn_belief': request.form.get('unicorn')
        }

        print("User Data:", user_data)  # Debugging line

        # Append user data to data.txt
        try:
            with open(DATA_FILE, 'a') as f:
                f.write(json.dumps(user_data) + '\n')
                print("Data written to file")  # Debugging line
        except Exception as e:
            print("Error writing to file:", e)  # Debugging line

        return redirect(url_for('waiting'))
    return render_template('friendship-quiz.html')

@app.route('/waiting')
def waiting():
    return render_template('waiting.html')

@app.route('/result')
def result():
    # Read names from data.txt
    names = []
    with open('data.txt', 'r') as f:
        for line in f:
            user_data = json.loads(line)
            names.append(user_data['name'])
    
    return render_template('result.html', names=names)


if __name__ == '__main__':
    app.run(debug=True)