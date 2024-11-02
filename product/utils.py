
import boto3
import pandas as pd
import json
from datetime import datetime
BUCKET_NAME = 'stockio-dods'

# Initialize S3 client globally to reuse across functions
s3 = boto3.client('s3')

def fetch_data_from_s3(tickers, limit=100):
    data = []
    for ticker in tickers:
        prefix = f"{ticker}/"
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
        objects = response.get('Contents', [])[-limit:]
        
        for obj in objects:
            file_data = s3.get_object(Bucket=BUCKET_NAME, Key=obj['Key'])
            content = json.loads(file_data['Body'].read())
            
            # Check and add Datetime if missing
            if 'Datetime' not in content:
                content['Datetime'] = datetime.now().isoformat()
                
            data.append(content)
    
    return pd.DataFrame(data)