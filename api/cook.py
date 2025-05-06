from flask import Flask, request, render_template, redirect, url_for, jsonify, session
import json
import os
from .models import db, User, MatchResult 
import logging
from scipy.optimize import linear_sum_assignment
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import numpy as np

app = Flask(__name__)

def calculate_mbti_compatibility(mbti1, mbti2):
    # Convert MBTIs to uppercase and validate format
    mbti1 = mbti1.upper()
    mbti2 = mbti2.upper()
        
    # Compatibility matrix from image (converted to decimals)
    matrix = {
        'ENFJ': {'ENFJ': 0.86, 'ENFP': 0.91, 'ENTJ': 0.42, 'ENTP': 0.73, 'ESFJ': 0.64, 'ESFP': 0.80, 'ESTJ': 0.22, 'ESTP': 0.41, 'INFJ': 0.74, 'INFP': 0.73, 'INTJ': 0.16, 'INTP': 0.35, 'ISFJ': 0.30, 'ISFP': 0.40, 'ISTJ': 0.18, 'ISTP': 0.09},
        'ENFP': {'ENFJ': 0.91, 'ENFP': 0.97, 'ENTJ': 0.37, 'ENTP': 0.86, 'ESFJ': 0.42, 'ESFP': 0.93, 'ESTJ': 0.27, 'ESTP': 0.76, 'INFJ': 0.51, 'INFP': 0.73, 'INTJ': 0.15, 'INTP': 0.36, 'ISFJ': 0.11, 'ISFP': 0.49, 'ISTJ': 0.04, 'ISTP': 0.14},
        'ENTJ': {'ENFJ': 0.42, 'ENFP': 0.37, 'ENTJ': 0.91, 'ENTP': 0.81, 'ESFJ': 0.53, 'ESFP': 0.51, 'ESTJ': 0.87, 'ESTP': 0.74, 'INFJ': 0.25, 'INFP': 0.13, 'INTJ': 0.65, 'INTP': 0.47, 'ISFJ': 0.29, 'ISFP': 0.06, 'ISTJ': 0.66, 'ISTP': 0.41},
        'ENTP': {'ENFJ': 0.73, 'ENFP': 0.85, 'ENTJ': 0.81, 'ENTP': 0.94, 'ESFJ': 0.32, 'ESFP': 0.87, 'ESTJ': 0.70, 'ESTP': 0.92, 'INFJ': 0.11, 'INFP': 0.36, 'INTJ': 0.22, 'INTP': 0.51, 'ISFJ': 0.05, 'ISFP': 0.14, 'ISTJ': 0.11, 'ISTP': 0.35},
        'ESFJ': {'ENFJ': 0.64, 'ENFP': 0.42, 'ENTJ': 0.53, 'ENTP': 0.32, 'ESFJ': 0.94, 'ESFP': 0.40, 'ESTJ': 0.77, 'ESTP': 0.37, 'INFJ': 0.74, 'INFP': 0.17, 'INTJ': 0.32, 'INTP': 0.05, 'ISFJ': 0.79, 'ISFP': 0.57, 'ISTJ': 0.71, 'ISTP': 0.19},
        'ESFP': {'ENFJ': 0.80, 'ENFP': 0.93, 'ENTJ': 0.51, 'ENTP': 0.87, 'ESFJ': 0.40, 'ESFP': 0.70, 'ESTJ': 0.39, 'ESTP': 0.75, 'INFJ': 0.43, 'INFP': 0.58, 'INTJ': 0.22, 'INTP': 0.38, 'ISFJ': 0.15, 'ISFP': 0.58, 'ISTJ': 0.08, 'ISTP': 0.26},
        'ESTJ': {'ENFJ': 0.22, 'ENFP': 0.27, 'ENTJ': 0.87, 'ENTP': 0.70, 'ESFJ': 0.77, 'ESFP': 0.39, 'ESTJ': 0.96, 'ESTP': 0.78, 'INFJ': 0.14, 'INFP': 0.03, 'INTJ': 0.33, 'INTP': 0.22, 'ISFJ': 0.48, 'ISFP': 0.22, 'ISTJ': 0.79, 'ISTP': 0.55},
        'ESTP': {'ENFJ': 0.41, 'ENFP': 0.76, 'ENTJ': 0.74, 'ENTP': 0.92, 'ESFJ': 0.37, 'ESFP': 0.75, 'ESTJ': 0.78, 'ESTP': 0.95, 'INFJ': 0.05, 'INFP': 0.24, 'INTJ': 0.17, 'INTP': 0.39, 'ISFJ': 0.12, 'ISFP': 0.43, 'ISTJ': 0.20, 'ISTP': 0.62},
        'INFJ': {'ENFJ': 0.74, 'ENFP': 0.51, 'ENTJ': 0.25, 'ENTP': 0.11, 'ESFJ': 0.74, 'ESFP': 0.43, 'ESTJ': 0.14, 'ESTP': 0.05, 'INFJ': 0.96, 'INFP': 0.86, 'INTJ': 0.66, 'INTP': 0.50, 'ISFJ': 0.80, 'ISFP': 0.58, 'ISTJ': 0.52, 'ISTP': 0.23},
        'INFP': {'ENFJ': 0.73, 'ENFP': 0.73, 'ENTJ': 0.13, 'ENTP': 0.36, 'ESFJ': 0.17, 'ESFP': 0.58, 'ESTJ': 0.03, 'ESTP': 0.24, 'INFJ': 0.86, 'INFP': 0.97, 'INTJ': 0.84, 'INTP': 0.84, 'ISFJ': 0.46, 'ISFP': 0.76, 'ISTJ': 0.21, 'ISTP': 0.48},
        'INTJ': {'ENFJ': 0.16, 'ENFP': 0.15, 'ENTJ': 0.65, 'ENTP': 0.22, 'ESFJ': 0.32, 'ESFP': 0.22, 'ESTJ': 0.33, 'ESTP': 0.17, 'INFJ': 0.66, 'INFP': 0.84, 'INTJ': 0.89, 'INTP': 0.89, 'ISFJ': 0.79, 'ISFP': 0.45, 'ISTJ': 0.93, 'ISTP': 0.78},
        'INTP': {'ENFJ': 0.35, 'ENFP': 0.36, 'ENTJ': 0.47, 'ENTP': 0.51, 'ESFJ': 0.05, 'ESFP': 0.38, 'ESTJ': 0.22, 'ESTP': 0.39, 'INFJ': 0.50, 'INFP': 0.84, 'INTJ': 0.89, 'INTP': 0.96, 'ISFJ': 0.38, 'ISFP': 0.43, 'ISTJ': 0.51, 'ISTP': 0.81},
        'ISFJ': {'ENFJ': 0.30, 'ENFP': 0.11, 'ENTJ': 0.29, 'ENTP': 0.05, 'ESFJ': 0.79, 'ESFP': 0.15, 'ESTJ': 0.48, 'ESTP': 0.12, 'INFJ': 0.80, 'INFP': 0.46, 'INTJ': 0.79, 'INTP': 0.38, 'ISFJ': 0.95, 'ISFP': 0.76, 'ISTJ': 0.93, 'ISTP': 0.62},
        'ISFP': {'ENFJ': 0.40, 'ENFP': 0.49, 'ENTJ': 0.06, 'ENTP': 0.14, 'ESFJ': 0.57, 'ESFP': 0.58, 'ESTJ': 0.22, 'ESTP': 0.43, 'INFJ': 0.58, 'INFP': 0.76, 'INTJ': 0.45, 'INTP': 0.43, 'ISFJ': 0.76, 'ISFP': 0.97, 'ISTJ': 0.47, 'ISTP': 0.78},
        'ISTJ': {'ENFJ': 0.18, 'ENFP': 0.04, 'ENTJ': 0.66, 'ENTP': 0.11, 'ESFJ': 0.71, 'ESFP': 0.08, 'ESTJ': 0.79, 'ESTP': 0.20, 'INFJ': 0.52, 'INFP': 0.21, 'INTJ': 0.93, 'INTP': 0.51, 'ISFJ': 0.93, 'ISFP': 0.47, 'ISTJ': 0.96, 'ISTP': 0.78},
        'ISTP': {'ENFJ': 0.09, 'ENFP': 0.14, 'ENTJ': 0.41, 'ENTP': 0.35, 'ESFJ': 0.19, 'ESFP': 0.26, 'ESTJ': 0.55, 'ESTP': 0.62, 'INFJ': 0.23, 'INFP': 0.48, 'INTJ': 0.78, 'INTP': 0.81, 'ISFJ': 0.62, 'ISFP': 0.78, 'ISTJ': 0.78, 'ISTP': 0.96}
    }

    # Get compatibility score from matrix
    compatibility_score = (matrix.get(mbti1, {}).get(mbti2, -1)) * (10/9.7)
    
    return compatibility_score

def calculate_compatibility(user1, user2, include_gender=True): 
    score = 0

    # Question 1: MBTI
    score += calculate_mbti_compatibility(user1.mbti, user2.mbti)

    # Question 2 & 3: Gender Preference
    if include_gender:
        if user1.gender not in user2.preferred_gender or user2.gender not in user1.preferred_gender:
            return 0

    # Question 4: Conversationalist or Listener
    if user1.communication_style != user2.communication_style:
        score += 5
    else:
        score += 3

    # Question 5: Weekend Activities
    activity_scores = {
        ('Active', 'Active'): 5,
        ('Active', 'Chill'): 2,
        ('Active', 'Spontaneous'): 4,
        ('Active', 'Alone'): 2,
        ('Chill', 'Chill'): 5,
        ('Chill', 'Spontaneous'): 3,
        ('Chill', 'Alone'): 4,
        ('Spontaneous', 'Spontaneous'): 5,
        ('Spontaneous', 'Alone'): 3,
        ('Alone', 'Alone'): 5
    }
    score += activity_scores.get((user1.weekend_activity, user2.weekend_activity), 0)

    # Question 6: Money or Freedom
    if user1.preference == user2.preference:
        score += 5

    # Question 7: Movie Genres
    user1_genres = set(user1.movie_genres.split(','))
    user2_genres = set(user2.movie_genres.split(','))
    common_genres = user1_genres.intersection(user2_genres)
    if len(common_genres) == 3:
        score += 5
    elif len(common_genres) == 2:
        score += 4
    elif len(common_genres) == 1:
        score += 3
    else:
        score += 1

    if 'Anime' in common_genres:
        score += 1
    if 'Horror/Thriller' in user1_genres and 'Horror/Thriller' not in user2_genres:
        score -= 1
    if 'Horror/Thriller' in user2_genres and 'Horror/Thriller' not in user1_genres:
        score -= 1

    # Question 8: Party Frequency
    party_levels = ['Never', 'Rarely', 'Sometimes', 'Usually']
    level_diff = abs(party_levels.index(user1.party_frequency) - party_levels.index(user2.party_frequency))
    if level_diff == 0:
        score += 5
    elif level_diff == 1:
        score += 4
    elif level_diff == 2:
        score += 2

    # Question 9: Relationship Components
    user1_components = set(user1.relationship_components.split(','))
    user2_components = set(user2.relationship_components.split(','))
    common_components = user1_components.intersection(user2_components)
    if len(common_components) == 3:
        score += 5
    elif len(common_components) == 2:
        score += 4
    elif len(common_components) == 1:
        score += 3
    else:
        score += 1

    # Question 10: Belief in Fate
    fate_levels = ['Nonsense', 'Depends', 'Yes']
    level_diff = abs(fate_levels.index(user1.fate_belief) - fate_levels.index(user2.fate_belief))
    if level_diff == 0:
        score += 5
    elif level_diff == 1:
        score += 3

    # Decrease score if either user is dummy
    if user1.name == 'dummy' or user2.name == 'dummy':
        score -= 20

    return score

def calculate_all_compatibilities(users, include_gender=True):
    all_compatibilities = {}

    for user1 in users:
        user_scores = {}
        for user2 in users:
            if user1.id != user2.id:
                score = calculate_compatibility(user1, user2, include_gender)
                user_scores[user2.id] = score
        all_compatibilities[user1.id] = user_scores

    return all_compatibilities

def find_best_matches(users):
    dummy_user = None  # Initialize dummy_user to None

    # Add a dummy user if the number of users is odd
    if len(users) % 2 != 0:
        dummy_user = User(
            name="dummy",
            discord_handle="dummy",
            mbti="ESTP",
            gender="Male",
            preferred_gender="Male,Female",
            communication_style="Listener",
            weekend_activity="Chill",
            preference="Money",
            movie_genres="Action/Adventure,Drama,Comedy",
            party_frequency="Sometimes",
            relationship_components="Trust,Communication,Respect",
            fate_belief="Depends",
            message="This is a dummy user for balancing."
        )
        users.append(dummy_user)

    # Round 1: Consider gender preferences
    compatibilities = calculate_all_compatibilities(users, include_gender=True)
    matches = apply_hungarian_algorithm(compatibilities)

    # Identify unmatched users
    matched_users = set(matches.keys()).union(set(matches.values()))
    unmatched_users = [user for user in users if user.id not in matched_users]

    # Round 2: Ignore gender preferences for unmatched users
    if unmatched_users:
        unmatched_compatibilities = calculate_all_compatibilities(unmatched_users, include_gender=False)
        unmatched_matches = apply_hungarian_algorithm(unmatched_compatibilities)
        matches.update(unmatched_matches)

    # Remove dummy user from matches if it exists
    if dummy_user:
        matches = {k: v for k, v in matches.items() if k != dummy_user.id and v != dummy_user.id}

    return matches

def apply_hungarian_algorithm(compatibilities):
    user_ids = list(compatibilities.keys())
    n = len(user_ids)

    # Create a cost matrix for the Hungarian algorithm
    cost_matrix = np.zeros((n, n))
    for i, user1 in enumerate(user_ids):
        for j, user2 in enumerate(user_ids):
            if user1 != user2:
                # Use negative scores because the algorithm finds the minimum cost
                cost_matrix[i, j] = -compatibilities[user1].get(user2, 0)

    # Apply the Hungarian Algorithm
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    # Create matches based on the assignment
    matches = {}
    for i, j in zip(row_ind, col_ind):
        if i != j:  # Ensure no self-matching
            user1_id = user_ids[i]
            user2_id = user_ids[j]
            matches[user1_id] = user2_id

    return matches

def main():
    users = User.query.all()

    # Clear previous match results
    MatchResult.query.delete()

    # Find matches
    matches = find_best_matches(users)

    # Store matches in the database
    for user1_id, user2_id in matches.items():
        match_result = MatchResult(user1_id=user1_id, user2_id=user2_id, score=0, message="")
        db.session.add(match_result)
    db.session.commit()

def get_gender_ratio():
    total_users = User.query.count()
    if total_users == 0:
        return {"Male": 0, "Female": 0}
    
    male_count = User.query.filter_by(gender="Male").count()
    female_count = User.query.filter_by(gender="Female").count()
    
    return {
        "Male": round((male_count/total_users) * 100, 1),
        "Female": round((female_count/total_users) * 100, 1)
    }

@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        try:
            user = User(
                name=request.form.get('name'),
                discord_handle=request.form.get('discord'),
                mbti=request.form.get('mbti'),
                gender=request.form.get('gender'),
                preferred_gender=request.form.get('preferred_gender'),
                communication_style=request.form.get('communication_style'),
                weekend_activity=request.form.get('weekend_activity'),
                preference=request.form.get('preference'),
                movie_genres=','.join(request.form.getlist('movie_genres')),
                party_frequency=request.form.get('party_frequency'),
                relationship_components=','.join(request.form.getlist('relationship_components')),
                fate_belief=request.form.get('fate_belief')
            )
            db.session.add(user)
            db.session.commit()
            
            # Add gender ratio to session
            session['gender_ratio'] = get_gender_ratio()
            return redirect(url_for('waiting'))
        except Exception as e:
            logging.error("Error adding user: %s", e)
            return "An error occurred", 500
    return render_template('join.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)