# Starts from the python 3.10 official docker image
FROM python:3.10-slim

# Create a folder "app" at the root of the image
RUN mkdir /app

# set workdir
WORKDIR /app

# copy requirements and code
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Expose port for Streamlit (8501) and FastAPI (8000) — choose one when running
EXPOSE 8501
EXPOSE 8000

# Default command - start Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]