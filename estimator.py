import os
import re
import logging
from typing import Dict, Optional

import pandas as pd
import google.generativeai as genai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
DEFAULT_MODEL = "gemini-1.5-flash"
FIBONACCI = [1, 2, 3, 5, 8, 13, 21]


def validate_and_clean_df(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Validate CSV schema, clean missing values, and enforce Fibonacci mapping.
    
    Args:
        df: DataFrame to validate and clean
        
    Returns:
        Cleaned DataFrame or None if validation fails
    """
    if df is None:
        logger.error("DataFrame is None")
        return None

    # Strip whitespace from column names
    df = df.rename(columns=lambda c: c.strip())
    
    # Check required columns
    required = ['Summary', 'Description', 'AcceptanceCriteria', 'StoryPoints']
    if not all(col in df.columns for col in required):
        logger.error(f"CSV must contain columns: {required}")
        return None

    # Drop rows with missing critical data
    df = df.dropna(subset=['Summary', 'Description', 'StoryPoints'])

    # Convert StoryPoints to float and handle errors
    def safe_to_float(x):
        try:
            return float(x)
        except (ValueError, TypeError):
            return None

    df['StoryPoints'] = df['StoryPoints'].apply(safe_to_float)
    df = df.dropna(subset=['StoryPoints'])

    # Map to nearest Fibonacci number
    def nearest_fibonacci(val):
        """Find the nearest Fibonacci number to the given value."""
        if val <= 0:
            return FIBONACCI[0]
        differences = [(abs(val - f), f) for f in FIBONACCI]
        return min(differences, key=lambda t: t[0])[1]

    df['StoryPoints'] = df['StoryPoints'].apply(nearest_fibonacci)

    # Clean text columns
    for col in ['Summary', 'Description', 'AcceptanceCriteria']:
        df[col] = df[col].astype(str).str.strip()

    logger.info(f"Validated and cleaned {len(df)} historical stories")
    return df


def sanitize_text(text: str, max_len: int = 4000) -> str:
    """
    Remove potential prompt-injection attempts and truncate text.
    
    Args:
        text: Text to sanitize
        max_len: Maximum length of output text
        
    Returns:
        Sanitized text
    """
    if not isinstance(text, str):
        return ""

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Remove common prompt injection patterns
    injection_patterns = [
        r"ignore all previous instructions",
        r"disregard system prompt",
        r"you are now",
        r"ignore these rules",
        r"forget everything",
        r"new instructions"
    ]
    
    for pattern in injection_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    # Truncate if too long
    if len(text) > max_len:
        text = text[:max_len] + "..."
        logger.warning(f"Text truncated to {max_len} characters")

    return text


def load_historical_data(filepath: str) -> Optional[pd.DataFrame]:
    """
    Load and validate historical data from a CSV file.
    
    Args:
        filepath: Path to CSV file
        
    Returns:
        Validated DataFrame or None if loading fails
    """
    if not os.path.exists(filepath):
        logger.error(f"File not found at {filepath}")
        return None
    
    try:
        df = pd.read_csv(filepath)
        return validate_and_clean_df(df)
    except Exception as e:
        logger.error(f"Error reading CSV: {e}")
        return None


def construct_prompt(new_story: Dict[str, str], historical_df: pd.DataFrame) -> str:
    """
    Construct the prompt for the Gemini model with sanitized inputs.
    
    Args:
        new_story: Dictionary with 'summary', 'description', 'acceptance_criteria'
        historical_df: DataFrame with historical story data
        
    Returns:
        Formatted prompt string
    """
    # Sanitize inputs
    summary = sanitize_text(new_story.get('summary', ''))
    description = sanitize_text(new_story.get('description', ''))
    acceptance_criteria = sanitize_text(new_story.get('acceptance_criteria', ''))

    # Validate and clean historical data
    hist_df = validate_and_clean_df(historical_df)
    
    if hist_df is None or hist_df.empty:
        logger.warning("No valid historical data available")
        examples = []
    else:
        # Use first 5 examples (simple approach, can be enhanced with similarity search later)
        examples = hist_df.head(5).to_dict('records')

    # System prompt
    fibonacci_str = ", ".join(str(f) for f in FIBONACCI)
    system_prompt = f"""You are an expert AI Story Point Estimator for agile teams.

Your task is to estimate story points for new user stories based on historical data and the Fibonacci sequence.

**Rules:**
1. Story points MUST be one of: [{fibonacci_str}]
2. Consider: Uncertainty, Complexity, and Effort
3. Use historical examples as reference points
4. Provide clear rationale for your estimate
5. If uncertain, suggest a range of Fibonacci numbers

**Output Format:**
- Estimated Story Points: [number]
- Rationale: [detailed explanation covering uncertainty, complexity, and effort]
- Confidence: [High/Medium/Low]
- Similar Stories: [reference to similar historical examples if applicable]
"""

    # Historical examples
    example_text = ""
    if examples:
        example_text = "\n\n### Historical Examples (for reference):\n"
        for i, ex in enumerate(examples, 1):
            example_text += f"""
{i}. Summary: {sanitize_text(ex.get('Summary', ''))}
   Description: {sanitize_text(ex.get('Description', ''))}
   Acceptance Criteria: {sanitize_text(ex.get('AcceptanceCriteria', ''))}
   Story Points: {ex.get('StoryPoints')}
"""

    # New story to estimate
    new_story_text = f"""

### NEW STORY TO ESTIMATE:

**Summary:** {summary}

**Description:** {description}

**Acceptance Criteria:** {acceptance_criteria}

Please provide your story point estimate following the rules and format above.
"""

    full_prompt = system_prompt + example_text + new_story_text
    return full_prompt


def estimate_story_points():
    """CLI interface for story point estimation (for testing)."""
    print("Welcome to the AI Story Point Estimator (Gemini Powered).")
    
    # 1. Get API Key
    api_key = input("Enter your Gemini API Key: ").strip()
    if not api_key:
        print("API Key is required.")
        return
    
    genai.configure(api_key=api_key)
    
    # 2. Get Historical Data File
    csv_path = input("Enter path to historical data CSV: ").strip()
    if not csv_path:
        print("CSV path is required.")
        return
        
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
        print("\n" + "="*60)
        print(response.text)
        print("="*60)
    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    estimate_story_points()
