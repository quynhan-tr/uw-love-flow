from flask import Flask, request, render_template, redirect, url_for, jsonify, session
import json
import os

app = Flask(__name__)
app.secret_key = 'uw_dsc_speed_dating' 

# Get the absolute path to the project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data.txt')

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/main')
def main():
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
            'gender': request.form.get('gender'),
            'preferred_gender': request.form.getlist('preferred-gender'),
            'other_gender': request.form.get('other-gender-input'),
            'communication_style': request.form.get('communication-style'),
            'weekend_activity': request.form.get('weekend-activity'),
            'preference': request.form.get('preference'),
            'movie_genres': request.form.getlist('movie-genres'),
            'party_frequency': request.form.get('party-frequency'),
            'relationship_components': request.form.getlist('relationship-components'),
            'fate_belief': request.form.get('fate')
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

@app.route('/pre_result')
def pre_result():
    return render_template('pre_result.html')

@app.route('/check_result')
def check_result():
    result_file = 'result.txt'
    
    # Check if the file exists and has content
    if os.path.exists(result_file) and os.path.getsize(result_file) > 0:
        return jsonify(hasResult=True)
    else:
        return jsonify(hasResult=False)

@app.route('/host')
def host():
    return render_template('host.html')

@app.route('/result')
def result():
    # Get name from query parameter
    name = request.args.get('name')
    if not name:
        return redirect(url_for('pre_result'))

    # Read names for floating animation and check existence
    names = []
    name_exists = False
    with open('data.txt', 'r') as f:
        for line in f:
            user_data = json.loads(line)
            names.append(user_data['name'])
            if user_data['name'] == name:
                name_exists = True

    if not name_exists:
        return render_template('pre_result.html', error="Name not found. Please re-enter your name.")

    # Search for match in result.txt
    match_name = ""
    match_discord = ""
    is_round_2 = False
    no_match = False

    with open('result.txt', 'r') as f:
        for line in f:
            if name in line:
                if "No match found" in line:
                    no_match = True
                    break
                    
                parts = line.strip().split(' - ')
                if "Round 2" in parts[0]:
                    is_round_2 = True
                    
                # Find the match name and discord
                if parts[1].split(' (')[0] == name:
                    match_name = parts[2].split(' (')[0]
                    match_discord = parts[2].split('(')[1].rstrip(')')
                else:
                    match_name = parts[1].split(' (')[0]
                    match_discord = parts[1].split('(')[1].rstrip(')')
                break

    if no_match:
        return render_template('result.html', 
                             match_name=False, 
                             names=names)
    elif is_round_2:
        return render_template('result.html', 
                             match_name=match_name,
                             match_discord=match_discord,
                             round_2_message="We're sorry that some of your preferences might not be satisfied due to gender ratio",
                             names=names)
    else:
        return render_template('result.html',
                             match_name=match_name, 
                             match_discord=match_discord,
                             names=names)

if __name__ == '__main__':
    app.run(debug=True)
