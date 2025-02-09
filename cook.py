import json
from itertools import combinations
from models import db, User, MatchResult

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

def calculate_compatibility(user1, user2):
    score = 0

    # Question 1: MBTI
    score += calculate_mbti_compatibility(user1.mbti, user2.mbti)

    # Question 2 & 3: Gender Preference
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

    return score

def calculate_all_compatibilities():
    users = User.query.all()
    all_compatibilities = {}

    for user1 in users:
        user_scores = {}
        for user2 in users:
            if user1.id != user2.id:
                score = calculate_compatibility(user1, user2)
                user_scores[user2.id] = score
        all_compatibilities[user1.id] = user_scores

    return all_compatibilities

def find_best_matches(all_compatibilities):
    matched_users = set()
    matches = []
    round2_participants = []

    # Round 1: Find matches with balanced compatibility scores
    while True:
        best_pair = None
        best_avg_score = -1
        
        # Check all possible pairs
        for user1 in all_compatibilities:
            if user1 in matched_users:
                continue
                
            for user2, score1 in all_compatibilities[user1].items():
                if user2 in matched_users:
                    continue
                    
                # Get reverse compatibility score
                score2 = all_compatibilities[user2][user1]
                avg_score = (score1 + score2) / 2
                
                # Check if scores are balanced (within 5 points of average)
                if abs(score1 - avg_score) <= 5 and abs(score2 - avg_score) <= 5:
                    if avg_score > best_avg_score:
                        best_avg_score = avg_score
                        best_pair = (user1, user2, avg_score)
        
        # If no valid pair found, break
        if best_pair is None:
            break
            
        # Add pair to matches
        user1, user2, score = best_pair
        matches.append((user1, user2, score, "Round 1"))
        matched_users.add(user1)
        matched_users.add(user2)
    
    # Collect unmatched users for Round 2
    for user in all_compatibilities:
        if user not in matched_users:
            round2_participants.append(user)
    
    # Round 2: Match remaining users ignoring gender/communication preferences
    if round2_participants:
        round2_matches = []
        round2_matched = set()
        
        for user1 in round2_participants:
            if user1 in round2_matched:
                continue
                
            best_match = None
            best_score = -1
            
            for user2 in round2_participants:
                if user1 != user2 and user2 not in round2_matched:
                    score1 = all_compatibilities[user1][user2]
                    score2 = all_compatibilities[user2][user1]
                    avg_score = (score1 + score2) / 2
                    
                    if avg_score > best_score:
                        best_score = avg_score
                        best_match = (user2, avg_score)
            
            if best_match:
                user2, score = best_match
                round2_matches.append((user1, user2, score, "Round 2"))
                round2_matched.add(user1)
                round2_matched.add(user2)
        
        matches.extend(round2_matches)
        
        # Add unmatched users to matches list
        for user in round2_participants:
            if user not in round2_matched:
                matches.append((user, None, 0, "No Match"))
    
    return matches

def main():
    # Clear previous match results
    MatchResult.query.delete()

    # Calculate compatibilities and find matches
    compatibilities = calculate_all_compatibilities()
    matches = find_best_matches(compatibilities)

    # Store matches in the database
    for user1_id, user2_id, score, round_type in matches:
        match_result = MatchResult(user1_id=user1_id, user2_id=user2_id, score=score, round_type=round_type)
        db.session.add(match_result)
    db.session.commit()

if __name__ == "__main__":
    main()