FROM python:3.11

# Update package list and install build-essential for compilation support
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install tensorflowjs
RUN pip install tensorflowjs


# Set the working directory in the container
WORKDIR /workspace

# Set the default entrypoint to tensorflowjs_converter
ENTRYPOINT ["tensorflowjs_converter"]