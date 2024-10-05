# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose any necessary ports (if applicable)
# EXPOSE 8080

# Define environment variable
# ENV NAME World

# Run the main.py script when the container launches
CMD ["python", "src/main.py"]

