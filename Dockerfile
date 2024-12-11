# Use a base image with Python 3.8
FROM python:3.8.5-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    && apt-get clean

# Upgrade pip and install required Python packages
RUN pip install --upgrade pip \
    && pip install scispacy==0.5.5 \
    && pip install spacy==3.4.4 \
    && pip install jupyter \
    && pip install networkx matplotlib \
    && pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.1/en_core_sci_sm-0.5.1.tar.gz

# Expose Jupyter notebook port
EXPOSE 8888

# Default command to run Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]

