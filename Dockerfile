# Start from official slim Python image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /code

# Environment variable: Tell Hugging Face where to cache models
ENV HF_HOME=/code/.cache/huggingface

# (Optional) Authenticate with Hugging Face if you have a token
# ENV HUGGINGFACEHUB_API_TOKEN=your_hf_token_here

# Copy the Python dependencies file
COPY ./requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy application code
COPY ./app/ /code/app/

# Create cache folder (to avoid any permission issues at runtime)
RUN mkdir -p /code/.cache/huggingface

# Expose the port uvicorn will run on (good practice, optional)
EXPOSE 8080

# Default command to run your app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
