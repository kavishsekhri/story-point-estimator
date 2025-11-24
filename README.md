# 🔢 AI Story Point Estimator

An intelligent assistant that helps agile teams estimate story points using historical data and the Gemini AI model.

## 🚀 Features

*   **AI-Powered Estimation**: Uses Google's Gemini AI to analyze user stories and suggest story points.
*   **Historical Data Analysis**: Learns from your team's past velocity and complexity to provide tailored estimates.
*   **Automatic Data Validation**: Validates CSV files, cleans data, and enforces Fibonacci sequence mapping.
*   **Input Sanitization**: Protects against prompt injection attacks and handles malformed inputs gracefully.
*   **Fibonacci Enforcement**: Automatically maps all story points to the standard Fibonacci scale (1, 2, 3, 5, 8, 13, 21).
*   **Detailed Rationale**: Provides a breakdown of Uncertainty, Complexity, and Effort for each estimate.
*   **Smart Error Handling**: Comprehensive logging and user-friendly error messages.
*   **Jira Compatible**: Generates estimates that can be easily integrated into your workflow.

## 🎥 Product Demo

See the AI Story Point Estimator in action:

https://github.com/kavishsekhri/story-point-estimator/raw/refs/heads/main/Product_demo.webm

## 🛠️ Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/kavishsekhri/story-point-estimator.git
    cd story-point-estimator
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

## 📊 CSV Format Requirements

Your historical data CSV must include these columns:
*   **Summary**: Brief story title
*   **Description**: Detailed story description
*   **AcceptanceCriteria**: Acceptance criteria for the story
*   **StoryPoints**: Actual story points (will be auto-mapped to Fibonacci)

The app will automatically:
*   Validate the CSV structure
*   Clean missing or malformed data
*   Map story points to the nearest Fibonacci number

## 🔑 Configuration

You will need a **Google Gemini API Key** to run this application.
1.  Get your key from [Google AI Studio](https://aistudio.google.com/).
2.  Enter the key in the sidebar when running the app.

## 📦 Deployment

This app is ready to be deployed on **Streamlit Community Cloud**.
1.  Push this code to a GitHub repository.
2.  Log in to [Streamlit Cloud](https://share.streamlit.io/).
3.  Deploy the app from your repository.
4.  **Important:** Add your `GEMINI_API_KEY` in the Streamlit "Secrets" settings.

## 📄 License

[MIT License](LICENSE)
