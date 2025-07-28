FROM python:3.9-slim

WORKDIR /app

# Install required libraries
RUN pip install pymupdf nltk

# Copy everything into the container
COPY offline_paper.py /app/
COPY nltk_data /usr/local/nltk_data

# Set environment variable so nltk looks here
ENV NLTK_DATA=/usr/local/nltk_data

# Create input/output folders
RUN mkdir /app/input /app/output

CMD ["python", "offline_paper.py"]
