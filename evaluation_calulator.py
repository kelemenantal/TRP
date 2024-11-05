import json
import os
from statistics import mean

# Define the evaluation calculator
def calculate_scores(file_path):
    # Read the JSON file and extract scores
    with open(file_path, 'r') as f:
        evaluations = json.load(f)
    
    # Initialize score accumulators
    total_relevance = []
    total_completeness = []
    total_accuracy = []
    total_clarity = []
    
    # Extract scores for each answer in the JSON file
    for answer in evaluations:
        total_relevance.append(answer["Relevance"])
        total_completeness.append(answer["Completeness"])
        total_accuracy.append(answer["Accuracy"])
        total_clarity.append(answer["Clarity"])
    
    # Calculate the average scores for each criterion
    avg_relevance = mean(total_relevance)
    avg_completeness = mean(total_completeness)
    avg_accuracy = mean(total_accuracy)
    avg_clarity = mean(total_clarity)
    
    # Define weights for each criterion if needed (example: equal weights)
    weights = {
        "relevance": 1.0,
        "completeness": 1.0,
        "accuracy": 1.0,
        "clarity": 1.0
    }
    
    # Calculate the weighted score
    weighted_score = (
        avg_relevance * weights["relevance"] +
        avg_completeness * weights["completeness"] +
        avg_accuracy * weights["accuracy"] +
        avg_clarity * weights["clarity"]
    ) / sum(weights.values())  # normalize by total weight
    
    return weighted_score, {
        "Relevance": avg_relevance,
        "Completeness": avg_completeness,
        "Accuracy": avg_accuracy,
        "Clarity": avg_clarity,
        "Overall Score": weighted_score
    }

def evaluate_files(file1, file2):
    # Calculate scores for both files
    score1, details1 = calculate_scores(file1)
    score2, details2 = calculate_scores(file2)
    
    # Determine which file is better based on the overall weighted score
    better_file = file1 if score1 > score2 else file2
    
    return better_file, details1, details2

# Specify the JSON file paths
file1 = 'assistant.json'
file2 = 'basic4o.json'

# Evaluate and print the results
better_file, details1, details2 = evaluate_files(file1, file2)
print(f"Better file: {better_file}")
print("\nScores for assistant.json:", details1)
print("\nScores for basic4o.json:", details2)
