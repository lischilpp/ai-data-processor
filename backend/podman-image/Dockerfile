# Step 1: Use an official Python runtime as the base image
FROM python:3.9-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the requirements.txt file to the working directory
COPY requirements.txt ./

# Step 4: Install the dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the current directory contents into the container at /usr/src/app
COPY . .

# Step 6: Define the command to run the app (this is optional, depends on your app)
CMD ["python", "main.py"]