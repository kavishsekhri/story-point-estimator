import os
import csv
import google.generativeai as genai
import pandas as pd

# Configuration
DEFAULT_MODEL = "gemini-1.5-flash"

def load_historical_data(filepath):
    """Loads historical data from a CSV file."""
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
        return None
    try:
        df = pd.read_csv(filepath)
        # Ensure required columns exist
        required_columns = ['Summary', 'Description', 'AcceptanceCriteria', 'StoryPoints']
        if not all(col in df.columns for col in required_columns):
            print(f"Error: CSV must contain columns: {required_columns}")
            return None
        return df
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None

def construct_prompt(new_story, historical_df):
    """Constructs the prompt for the Gemini model."""
    
    # Load system prompt
    try:
        with open('story_point_agent/system_prompt.md', 'r') as f:
            system_prompt = f.read()
    except FileNotFoundError:
        print("Warning: system_prompt.md not found. Using default.")
        system_prompt = "You are an AI Story Point Estimator."

    # Select a few examples (simple heuristic: random or first few)
    # In a real app, we'd do semantic search here.
    examples = historical_df.head(5).to_dict('records')
    
    example_text = "\n\n### Historical Examples:\n"
    for ex in examples:
        example_text += f"""
- **Summary:** {ex.get('Summary')}
  **Description:** {ex.get('Description')}
  **Acceptance Criteria:** {ex.get('AcceptanceCriteria')}
  **Actual Story Points:** {ex.get('StoryPoints')}
  **Actual Time:** {ex.get('ActualTime', 'N/A')}
"""

    new_story_text = f"""
\n\n### New Story to Estimate:
**Summary:** {new_story['summary']}
**Description:** {new_story['description']}
**Acceptance Criteria:** {new_story['acceptance_criteria']}
"""

    full_prompt = system_prompt + example_text + new_story_text
    return full_prompt

def estimate_story_points():
    print("Welcome to the AI Story Point Estimator (Gemini Powered).")
    
    # 1. Get API Key
    api_key = input("Enter your Gemini API Key: ").strip()
    if not api_key:
        print("API Key is required.")
        return
    
    genai.configure(api_key=api_key)
    
    # 2. Get Historical Data File
    csv_path = input("Enter path to historical data CSV (default: story_point_agent/data/historical_stories.csv): ").strip()
    if not csv_path:
        csv_path = 'story_point_agent/data/historical_stories.csv'
        
    historical_df = load_historical_data(csv_path)
    if historical_df is None:
        return

    # 3. Get New Story Details
    print("\n--- New Story Details ---")
    summary = input("Summary: ").strip()
    description = input("Description: ").strip()
    acceptance_criteria = input("Acceptance Criteria: ").strip()
    
    if not summary:
        print("Summary is required.")
        return

    new_story = {
        'summary': summary,
        'description': description,
        'acceptance_criteria': acceptance_criteria
    }

    # 4. Generate Content
    prompt = construct_prompt(new_story, historical_df)
    
    print("\nAnalyzing and Estimating...")
    
    try:
        model = genai.GenerativeModel(DEFAULT_MODEL)
        response = model.generate_content(prompt)
        print("\n" + "="*30)
        print(response.text)
        print("="*30)
    except Exception as e:
        print(f"Error calling Gemini API: {e}")

if __name__ == "__main__":
    estimate_story_points()
