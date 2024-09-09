sudo yum update 
sudo yum install python37
pip install mlflow boto3 psycopg2-binary 
aws configure
aws s3 ls 
mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri postgresql://DB_USER:DB_PASSWORD@DB_ENDPOINT:5432/DB_NAME --default-artifact-root s3://S3_BUCKET_NAME