# Step 1: Use an official Python runtime as a parent image.
# Using 'slim' makes the image smaller and more efficient.
FROM python:3.9-slim

# Step 2: Set the working directory inside the container.
WORKDIR /app

# Step 3: Copy the requirements file into the container.
# This is done first to leverage Docker's layer caching.
# If requirements.txt doesn't change, Docker won't reinstall dependencies on subsequent builds.
COPY requirements.txt .

# Step 4: Install the Python dependencies.
# --no-cache-dir makes the image smaller.
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of your application's code into the container.
# This includes your .py files and the 'assets' and 'data' folders.
COPY . .

# Step 6: Expose the port that Streamlit runs on.
EXPOSE 8501

# Step 7: Define the command to run your application when the container starts.
CMD ["streamlit", "run", "main_app.py"]