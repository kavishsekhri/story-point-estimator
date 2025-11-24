# 🔢 AI Story Point Estimator

An intelligent assistant that helps agile teams estimate story points using historical data and the Gemini AI model.

## 🚀 Features

*   **AI-Powered Estimation**: Uses Google's Gemini AI to analyze user stories and suggest story points.
*   **Historical Data Analysis**: Learns from your team's past velocity and complexity to provide tailored estimates.
*   **Fibonacci Sequence**: Strictly adheres to the standard Fibonacci scale (1, 2, 3, 5, 8, 13...).
*   **Detailed Rationale**: Provides a breakdown of Uncertainty, Complexity, and Effort for each estimate.
*   **Jira Compatible**: Generates estimates that can be easily integrated into your workflow.

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
