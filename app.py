import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from estimator import construct_prompt, validate_and_clean_df

# Page Config
st.set_page_config(page_title="AI Story Point Estimator", page_icon="🔢")

st.title("🔢 AI Story Point Estimator")
st.markdown("Estimate story points using historical data and Gemini AI.")

# Sidebar for Configuration
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Gemini API Key", type="password")

    # Model Selection
    model_name = st.selectbox("Select Model", ["gemini-1.5-flash", "gemini-2.5-flash", "gemini-1.5-pro", "gemini-pro", "gemini-1.0-pro"])
    
    # Data Source - File Upload Only
    uploaded_file = st.file_uploader("Upload Historical Data (CSV)", type="csv")
    
    historical_df = None
    if uploaded_file is not None:
        try:
            raw_df = pd.read_csv(uploaded_file)
            historical_df = validate_and_clean_df(raw_df)
            
            if historical_df is not None and not historical_df.empty:
                st.success(f"✅ Loaded and validated {len(historical_df)} stories")
                st.info(f"📊 Story points range: {historical_df['StoryPoints'].min():.0f} - {historical_df['StoryPoints'].max():.0f}")
            else:
                st.error("❌ CSV validation failed. Please check the format.")
                st.info("Required columns: Summary, Description, AcceptanceCriteria, StoryPoints")
        except Exception as e:
            st.error(f"Error loading CSV: {e}")
    else:
        st.info("Please upload a CSV file with historical story points.")

    st.markdown("---")
    with st.expander("ℹ️ How it Works"):
        st.markdown("""
        **1. Historical Data Analysis**
        *   Uses your closed stories to learn velocity and complexity baselines.
        
        **2. Model Parameters**
        *   Applies a **MAE of 0.53** for confidence ranges.
        *   Detects complexity keywords (e.g., "AR", "VR") to adjust estimates.
        
        **3. Fibonacci Logic**
        *   Enforces the **Fibonacci sequence** (1, 2, 3, 5, 8...).
        *   Evaluates **Uncertainty**, **Complexity**, and **Effort**.
        """)

# Main Content
st.header("New Story Details")

summary = st.text_input("Story Summary", placeholder="e.g., Add Login Page")
description = st.text_area("Description", placeholder="Detailed description of the story...")
acceptance_criteria = st.text_area("Acceptance Criteria", placeholder="- User can login\n- User can logout")

if st.button("Estimate Story Points", type="primary"):
    if not api_key:
        st.error("Please provide a Gemini API Key in the sidebar.")
    elif historical_df is None:
        st.error("Please load historical data.")
    elif not summary:
        st.error("Please provide a story summary.")
    else:
        with st.spinner("Analyzing and Estimating..."):
            try:
                # Configure Gemini
                genai.configure(api_key=api_key)
                
                # Prepare Data
                new_story = {
                    'summary': summary,
                    'description': description,
                    'acceptance_criteria': acceptance_criteria
                }
                
                # Construct Prompt
                # We need to ensure construct_prompt can handle the DF directly or we adapt it.
                # The existing construct_prompt takes a DF.
                prompt = construct_prompt(new_story, historical_df)
                
                # Call API
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                
                # Display Result
                st.markdown("### 🤖 Estimation Result")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Footer
st.markdown("---")
st.caption("Powered by Google Gemini")
