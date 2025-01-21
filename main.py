import json
import pandas as pd
from collections import defaultdict

# File paths for the provided JSON data
historical_data_path = 'historical_qiz_data.json'
quiz_submission_data_path = 'quiz_submission_data.json'
current_quiz_data_path = 'quiz_endpint.json'

# Load the data from files
def load_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
        return None

# Load all datasets
historical_data = load_data(historical_data_path)
quiz_submission_data = load_data(quiz_submission_data_path)
current_quiz_data = load_data(current_quiz_data_path)

# Helper function to resolve "Unknown" topics
def resolve_unknown_topic(question_id, datasets):
    for dataset in datasets:
        if isinstance(dataset, dict):
            # Check if dataset has a "quiz" key with questions
            questions = dataset.get("quiz", {}).get("questions", [])
            for question in questions:
                if question["id"] == question_id:
                    return question.get("topic", "Unknown")
    return "Unknown"

# Analyze the data
def analyze_data(historical_data, quiz_submission_data, current_quiz_data):
    insights = {}

    # Aggregate performance by topic and difficulty
    topic_performance = defaultdict(lambda: {"correct": 0, "total": 0})

    # List of datasets for resolving unknown topics
    datasets = [historical_data, quiz_submission_data, current_quiz_data]

    # Historical Data Analysis
    if historical_data:
        for question_id, response in historical_data.get("response_map", {}).items():
            topic = resolve_unknown_topic(int(question_id), datasets)
            correct_option_id = next(
                (q.get("options", [{}])[0].get("id") for q in current_quiz_data.get("quiz", {}).get("questions", []) if q["id"] == int(question_id)),
                None
            )
            if correct_option_id is not None:
                is_correct = response == correct_option_id
                topic_performance[topic]["total"] += 1
                if is_correct:
                    topic_performance[topic]["correct"] += 1

    # Submission Data Analysis
    if quiz_submission_data:
        for question_id, response in quiz_submission_data.get("response_map", {}).items():
            topic = resolve_unknown_topic(int(question_id), datasets)
            correct_option_id = next(
                (q.get("options", [{}])[0].get("id") for q in current_quiz_data.get("quiz", {}).get("questions", []) if q["id"] == int(question_id)),
                None
            )
            if correct_option_id is not None:
                is_correct = response == correct_option_id
                topic_performance[topic]["total"] += 1
                if is_correct:
                    topic_performance[topic]["correct"] += 1

    # Generate insights on weak areas and trends
    insights["topic_insights"] = {
        topic: {
            "accuracy": (data["correct"] / data["total"] * 100) if data["total"] > 0 else 0,
            "total_questions": data["total"],
        }
        for topic, data in topic_performance.items()
    }

    # Generate trends from historical and submission scores
    scores = [
        historical_data.get("score", 0),
        quiz_submission_data.get("score", 0),
    ]
    insights["score_trend"] = "improving" if scores == sorted(scores) else "fluctuating"

    return insights

# Generate recommendations
def generate_recommendations(insights):
    recommendations = []

    # Suggest topics to focus on
    weak_topics = [
        topic for topic, data in insights["topic_insights"].items() if data["accuracy"] < 70
    ]
    if weak_topics:
        recommendations.append(
            "Focus on improving the following topics: " + ", ".join(weak_topics)
        )

    # Encourage consistency if score trend is fluctuating
    if insights["score_trend"] == "fluctuating":
        recommendations.append("Work on consistent practice to stabilize performance.")

    return recommendations

# Main execution
if historical_data and quiz_submission_data and current_quiz_data:
    insights = analyze_data(historical_data, quiz_submission_data, current_quiz_data)
    recommendations = generate_recommendations(insights)

    # Display results
    print("\nInsights:")
    insights_df = pd.DataFrame.from_dict(insights["topic_insights"], orient="index")
    print(insights_df)

    print("\nRecommendations:")
    for recommendation in recommendations:
        print(f"- {recommendation}")
else:
    print("Failed to load all required data.")
