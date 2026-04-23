import pandas as pd

def test_pandas_cleaning_logic():
    """Validates that raw CMS API strings are correctly cast to numeric and uppercase."""
    raw_df = pd.DataFrame([{
        'rndrng_prvdr_city': 'houston', 
        'tot_srvcs': '15',
        'avg_mdcr_pymt_amt': '125.50'
    }])
    
    clean_df = pd.DataFrame({
        'provider_city': raw_df['rndrng_prvdr_city'].str.upper(),
        'total_services': pd.to_numeric(raw_df['tot_srvcs'], errors='coerce'),
        'avg_pmt': pd.to_numeric(raw_df['avg_mdcr_pymt_amt'], errors='coerce')
    })
    
    assert clean_df.iloc[0]['provider_city'] == 'HOUSTON'
    assert clean_df.iloc[0]['total_services'] == 15
    assert clean_df.iloc[0]['avg_pmt'] == 125.50