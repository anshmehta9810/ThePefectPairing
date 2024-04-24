from collections import defaultdict
import math

# Sample data representing user profiles and companion profiles
users = [
    {
        'id': 1,
        'name': 'Alice',
        'interests': ['reading', 'cooking'],
        'hobbies': ['gardening', 'painting'],
        'location': 'New York',
        'availability': 'Weekends'
    },
    {
        'id': 2,
        'name': 'Bob',
        'interests': ['cooking', 'gardening'],
        'hobbies': ['reading', 'painting'],
        'location': 'New York',
        'availability': 'Weekdays'
    },
    {
        'id': 3,
        'name': 'Eve',
        'interests': ['traveling', 'photography'],
        'hobbies': ['hiking', 'photography'],
        'location': 'Los Angeles',
        'availability': 'Weekends'
    }
]

companions = [
    {
        'id': 1,
        'name': 'Charlie',
        'interests': ['reading', 'cooking'],
        'hobbies': ['gardening', 'painting'],
        'location': 'New York',
        'availability': 'Weekends'
    },
    {
        'id': 2,
        'name': 'David',
        'interests': ['cooking', 'sports'],
        'hobbies': ['reading', 'video games'],
        'location': 'Los Angeles',
        'availability': 'Weekends'
    },
    {
        'id': 3,
        'name': 'Frank',
        'interests': ['reading', 'photography'],
        'hobbies': ['cooking', 'gardening'],
        'location': 'New York',
        'availability': 'Weekdays'
    },
    {
        'id': 4,
        'name': 'Grace',
        'interests': ['cooking', 'music'],
        'hobbies': ['painting', 'listening to music'],
        'location': 'New York',
        'availability': 'Weekends'
    },
    {
        'id': 5,
        'name': 'Hannah',
        'interests': ['reading', 'yoga'],
        'hobbies': ['hiking', 'yoga'],
        'location': 'Los Angeles',
        'availability': 'Weekdays'
    }
]

def calculate_similarity(user_profile, companion_profile):
    # Calculate cosine similarity between user and companion profiles
    common_interests = set(user_profile['interests']).intersection(companion_profile['interests'])
    common_hobbies = set(user_profile['hobbies']).intersection(companion_profile['hobbies'])
    
    num_common_interests = len(common_interests)
    num_common_hobbies = len(common_hobbies)
    num_total_attributes = len(user_profile['interests']) + len(user_profile['hobbies'])
    
    similarity = (num_common_interests + num_common_hobbies) / math.sqrt(num_total_attributes)
    
    return similarity

def find_compatible_companions(user_profile, all_companions):
    compatibility_scores = defaultdict(list)
    for companion_profile in all_companions:
        score = calculate_similarity(user_profile, companion_profile)
        compatibility_scores[score].append(companion_profile)
    
    # Sort companions based on compatibility scores
    sorted_scores = sorted(compatibility_scores.keys(), reverse=True)
    compatible_companions = []
    for score in sorted_scores:
        companions_with_score = compatibility_scores[score]
        for companion in companions_with_score:
            compatible_companions.append((companion, score)) 
    return compatible_companions

def print_user_profiles(user_profiles):
    print("Available Users:")
    for user in user_profiles:
        print(user['id'], "-", user['name'])

def select_user(user_profiles):
    while True:
        print_user_profiles(user_profiles)
        user_id = input("Enter the ID of the user you want to find companions for (or type 'exit' to quit): ")
        if user_id.lower() == 'exit':
            return None
        try:
            user_id = int(user_id)
            selected_user = next((user for user in user_profiles if user['id'] == user_id), None)
            if selected_user:
                return selected_user
            else:
                print("Invalid user ID. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid user ID.")

# Example usage
while True:
    selected_user = select_user(users)
    if selected_user:
        print("Selected User:", selected_user['name'])
        compatible_companions = find_compatible_companions(selected_user, companions)
        print("Compatible companions for", selected_user['name'] + ":")
        for companion, score in compatible_companions:
            print(companion['name'], "- Compatibility Score:", score)
    else:
        print("Exiting...")
        break

    choice = input("Do you want to choose another user? (yes/no): ")
    if choice.lower() != 'yes':
        print("Exiting...")
        break
