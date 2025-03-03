import boto3
import random
import time
import json
from datetime import datetime, timedelta

# S3 Configuration
S3_BUCKET = "fraud-detection-storage-mk"  
S3_KEY = "synthetic-transaction-data/transactions.json"  

# Generate synthetic transaction data
def generate_transaction(is_fraud):
    return {
        "transaction_id": f"T{random.randint(1000, 9999)}",
        "user_id": f"U{random.randint(10000, 99999)}",
        "timestamp": "2025-01-01T12:00:00Z",
        "amount": round(random.uniform(10.0, 5000.0) * (1.5 if is_fraud else 1), 2),  
        "device_type": random.choice(["mobile", "desktop"]),
        "location": random.choice(["B", "G"]) if is_fraud else random.choice(["A", "C", "D", "E", "F", "H"]),
        "is_vpn": random.choice([True, False]) if not is_fraud else True,  
        "card_type": "credit" if is_fraud else random.choice(["credit", "debit"]),
        "status": "approved" if is_fraud else random.choice(["approved", "declined"]),
        "is_fraud": is_fraud
    }

# Generate and save data to S3
def generate_and_upload_data(num_records=1000):
    
    transactions = [generate_transaction(0) for _ in range(1000)] + [generate_transaction(1) for _ in range(1000)]
    s3 = boto3.client("s3")
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=S3_KEY,
        Body=json.dumps(transactions),
        ContentType="application/json"
    )
    print(f"Uploaded {num_records} synthetic transactions to s3://{S3_BUCKET}/{S3_KEY}")

# Main function
if __name__ == "__main__":
    generate_and_upload_data(num_records=10000) 