#initialize gclud
#gcloud init

#authenticate gclud
#gcloud auth configure-docker

#to build image
#docker build -t object-detector-image .

#tag the iamge to gcr service
#docker tag object-detector-image gcr.io/dental-xray-analyzer/object-detector-image

#pushing the image to gcr
#docker push gcr.io/dental-xray-analyzer/object-detector-image

#docker push gcr.io/dental-xray-analyzer/object-detector-image

#image urll for gcr
#gcr.io/dental-xray-analyzer/object-detector-image:latest



# Use a base image with Python installed
FROM python:3.8

# Set the working directory inside the container
WORKDIR /app

# Copy necessary files and directories
COPY object_detector.py /app/
COPY index.html /app/
COPY species.pt /app/
COPY diseases.pt /app/
COPY requirements.txt /app/



# Install system dependencies
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx

# Upgrade pip and install Python dependencies
RUN pip3 install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose port 8080 to the outside world
EXPOSE 8080

# Command to run the Flask server when the container starts
CMD ["python3", "/app/object_detector.py", "--host=0.0.0.0", "--port=8080"]
