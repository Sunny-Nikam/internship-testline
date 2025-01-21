# internship-testline
Installation

Clone the repository or download the project files.

Ensure that the JSON data files (historical_quiz_data.json, quiz_submission_data.json, quiz_endpoint.json) are placed in the same directory as the script.

Install the required libraries:

pip install pandas

Running the Project

Open a terminal or command prompt.

Navigate to the directory containing the script.

Run the script using Python:

python main.py

Output

The script outputs:

Insights: Topic-wise accuracy and total questions analyzed.

Recommendations: Suggestions for improving weak areas and maintaining consistency.

Student Persona: A summary of the student's strengths, weaknesses, and overall performance label.

Approach Description

1. Data Loading

The script reads three JSON files containing historical data, quiz metadata, and submission data.

Files are validated, and errors during loading are logged for debugging.

2. Data Analysis

Historical Data:

Processes the response_map to calculate accuracy and performance by topic.

Current Quiz Data:

Extracts topic and difficulty information for ongoing quizzes.

Submission Data:

Evaluates the correctness of responses and aggregates performance insights.

3. Resolving Unknown Topics

When topics are missing or marked as "Unknown," the script iterates through all datasets to find matching question metadata.

4. Generating Insights

Aggregates topic-wise accuracy and identifies weak areas.

Analyzes performance trends based on historical and submission scores.

5. Recommendations

Weak areas (accuracy below 70%) are flagged for improvement.

Performance trends are analyzed to recommend consistent practice.

6. Student Persona

Strengths and weaknesses are identified based on topic accuracy.

A personalized label (e.g., "Focused Learner") is assigned based on performance characteristics.
