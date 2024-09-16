# Use the official AWS Lambda Python 3.9 base image
FROM public.ecr.aws/lambda/python:3.10
# Copy requirements file and install dependencies
COPY requirements.txt .
# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
# Create a directory for AWS credentials
RUN mkdir -p /root/.aws 
# Copy the AWS credentials file from your local machine to the container
COPY [ "lambda_function.py", "model.py","./" ]
CMD ["lambda_function.lambda_handler"]