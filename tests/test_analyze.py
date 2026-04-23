import pandas as pd
from unittest.mock import patch
from pipeline.analyze import get_top_procedures

@patch('pipeline.analyze.pd.read_sql')
def test_get_top_procedures(mock_read_sql):
    """Mocks the database connection to verify the analyze module returns a DataFrame."""
    # Create a mock dataframe that simulates the SQL return
    mock_read_sql.return_value = pd.DataFrame({
        'procedure_desc': ['Mock Procedure'], 
        'avg_pmt': [500.0],
        'total_utilization': [50]
    })
    
    df = get_top_procedures()
    
    assert not df.empty
    assert len(df.columns) == 3
    assert df.iloc[0]['procedure_desc'] == 'Mock Procedure'