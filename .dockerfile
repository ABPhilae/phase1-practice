# === BASE IMAGE ===
# python:3.11-slim is a lightweight version of Python.
# 'slim' means it doesn't include extras like compilers,
# making the final image smaller (faster to download/deploy).
FROM python:3.11-slim

# === WORKING DIRECTORY ===
# This is where your code will live inside the container.
# Like choosing which room in a house to set up your kitchen.
WORKDIR /app

# === INSTALL DEPENDENCIES FIRST ===
# IMPORTANT: We copy requirements.txt BEFORE copying the rest of the code.
# Why? Docker caches each step. If your code changes but dependencies
# don't, Docker reuses the cached dependencies instead of reinstalling.
# This saves MINUTES on every build.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# === COPY APPLICATION CODE ===
# Now copy everything else. Changes here only rebuild from this step.
COPY . .

# === EXPOSE PORT ===
# This documents which port your app uses.
# It doesn't actually open the port - that happens at run time.
EXPOSE 8000

# === START COMMAND ===
# This is what runs when the container starts.
# --host 0.0.0.0 makes it accessible from outside the container.
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
