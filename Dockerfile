# Set base image (host OS)
FROM python:3.11.7

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install chromadb
RUN pip install -U langchain-community
# Copy the content of the local src directory to the working directory
COPY app.py .

# Copy other necessary files or directories
COPY static /app/static
COPY templates /app/templates
COPY 48lawsofpower.pdf /app/48lawsofpower.pdf

# Specify the command to run on container start
CMD [ "python", "./app.py" ]
