import yaml
from itertools import combinations

def interest_score(a,b):
    """
    Calculate the interest score for question 1. 

    Args:
        a (int): The first input value.
        b (int): The second input value.

    Returns:
        float: The calculated interest score.
    """
    
    if a == b:
        return 3
    elif abs(a - b) == 1:
        return 2
    elif abs(a - b) == 2:
        return 1
    else:
        return 0
    
def social_score(a,b):
    """
    Calculate the social score for question 2. 

    Args:
        a (int): The first input value.
        b (int): The second input value.
        
    Returns:
        float: The calculated social score.
    """
    
    best_alt_matches ={
        1: [4],
        2: [1,4],
        3: [5],
        4: [1,2],
        5: [3]
    }
    
    medium_alt_matches = {
        1: [2],
        2: [5],
        3: [2],
        4: [5],
        5: [2, 4]
    }
    
    if a == b:
        return 3
    elif b in best_alt_matches[a]:
        return 2
    elif b in medium_alt_matches[a]:
        return 1
    else:
        return 0
    
def total_score(personA, personB, data):
    """
    Calculate the total score based on two sets of answers.

    Args:
        personA (dict): The first person's answers.
        personB (dict): The second person's answers.
        data (list): The data containing question types.

    Returns:
        float: The total calculated score.
    """

    a1, a2 = data[personA]
    b1, b2 = data[personB]
    
    return interest_score(a1, b1) + social_score(a2, b2)

def different_groups(p1, p2, groups):
    return groups[p1] != groups[p2]

def match_peeps(data, groups):
    """
    Match people based on their answers and calculate scores.

    Args:
        data (list): The data containing question types.
        groups (dict): A dictionary mapping person indices to their group identifiers.
        
    Returns:
        match_map: A dictionary with person indices as keys and their best match index as values.
    """
    
    scores = []

    # 1. Compute all pair scores
    for p1, p2 in combinations(data.keys(), 2):
        score = total_score(p1, p2, data)
        scores.append(((p1, p2), score))

    # 2. Sort by score
    scores.sort(reverse=True, key=lambda x: x[1])

    matched = set()
    pairs = []

    # 3. Greedy matching with group restriction
    for (p1, p2), score in scores:
        if p1 not in matched and p2 not in matched:
            if different_groups(p1, p2, groups):  # NEW CHECK
                pairs.append((p1, p2))
                matched.add(p1)
                matched.add(p2)

    # 4. Handle leftovers
    for person in data.keys():
        if person not in matched:
            pairs.append((person, None))

    # 5. Build symmetric mapping
    match_map = {}
    for p1, p2 in pairs:
        match_map[p1] = p2
        if p2 is not None:
            match_map[p2] = p1

    return match_map

if __name__ == "__main__":
    # Load the data from the YAML files
    with open("data.yaml", 'r') as f:
        data = yaml.safe_load(f)
    with open("groups.yaml", 'r') as f:
        groups = yaml.safe_load(f)
        
    # Print the total amount of people
    print("Total people:", len(data))
    

    matches = match_peeps(data, groups)
    # Remove the duplicates, so if X is matched to Y, don't also show Y matched to X
    unique_matches = {}
    for person, match in matches.items():
        if match is None or (match, person) not in unique_matches.items():
            unique_matches[person] = match
    # Put the matches in a yaml file
    with open("matches.yaml", 'w') as f:
        yaml.dump(unique_matches, f)

    print("Total matches made:", len([m for m in unique_matches.values() if m is not None]))