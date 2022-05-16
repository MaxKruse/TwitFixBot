# Dockerize the python project

FROM python:3.10

WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy the project files
COPY . .

# Start the bot
CMD ["python3", "twitfix.py"]