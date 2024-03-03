FROM python:3.12
WORKDIR /app
COPY . /app
RUN pip install Flask
# Install Flask
EXPOSE 9090
# 9090 is the port number for the Flask server
CMD ["python", "FS.py"]