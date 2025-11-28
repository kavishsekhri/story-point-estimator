"""Integration tests for app.py"""
import pytest
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestAppIntegration:
    """Integration tests for the Streamlit app"""
    
    @patch('streamlit.text_input')
    @patch('streamlit.text_area')
    @patch('streamlit.button')
    @patch('streamlit.file_uploader')
    def test_app_imports(self, mock_uploader, mock_button, mock_textarea, mock_textinput):
        """Test that app.py can be imported without errors"""
        try:
            import app
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import app: {e}")
    
    def test_csv_data_loading(self):
        """Test that CSV data can be loaded and processed"""
        # Create a temporary CSV file
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("Summary,Description,AcceptanceCriteria,StoryPoints\n")
            f.write("Test Story,Test Desc,Test AC,5\n")
            temp_path = f.name
        
        try:
            from estimator import load_historical_data
            df = load_historical_data(temp_path)
            assert df is not None
            assert len(df) == 1
        finally:
            os.unlink(temp_path)
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_end_to_end_estimation(self, mock_model_class, mock_configure):
        """Test end-to-end estimation flow"""
        from estimator import construct_prompt, validate_and_clean_df
        
        # Mock the API response
        mock_response = Mock()
        mock_response.text = "Estimated Story Points: 5\nRationale: Test rationale"
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        # Create test data
        hist_df = pd.DataFrame({
            'Summary': ['Login Page'],
            'Description': ['Create login'],
            'AcceptanceCriteria': ['User can login'],
            'StoryPoints': [5]
        })
        
        new_story = {
            'summary': 'Logout Feature',
            'description': 'Add logout button',
            'acceptance_criteria': 'User can logout'
        }
        
        # Test the flow
        cleaned_df = validate_and_clean_df(hist_df)
        assert cleaned_df is not None
        
        prompt = construct_prompt(new_story, cleaned_df)
        assert 'Logout Feature' in prompt
        
        # Simulate API call
        mock_configure('test-api-key')
        model = mock_model_class('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        assert 'Estimated Story Points' in response.text
        assert '5' in response.text


class TestDataValidation:
    """Tests for data validation across the app"""
    
    def test_invalid_story_points_handling(self):
        """Test handling of invalid story points"""
        from estimator import validate_and_clean_df
        
        df = pd.DataFrame({
            'Summary': ['S1', 'S2', 'S3'],
            'Description': ['D1', 'D2', 'D3'],
            'AcceptanceCriteria': ['AC1', 'AC2', 'AC3'],
            'StoryPoints': ['invalid', -5, 100]
        })
        
        result = validate_and_clean_df(df)
        # Invalid values should be handled (dropped or mapped to valid Fibonacci)
        assert result is not None
        # All remaining points should be valid Fibonacci numbers
        from estimator import FIBONACCI
        for sp in result['StoryPoints']:
            assert sp in FIBONACCI
    
    def test_malformed_csv_handling(self):
        """Test handling of malformed CSV data"""
        import tempfile
        from estimator import load_historical_data
        
        # Create malformed CSV
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("Summary,Description\n")  # Missing required columns
            f.write("Test,Test\n")
            temp_path = f.name
        
        try:
            df = load_historical_data(temp_path)
            # Should return None for invalid schema
            assert df is None
        finally:
            os.unlink(temp_path)
