# Use NVIDIA CUDA 12.4 base image
FROM pytorch/pytorch:2.4.1-cuda12.1-cudnn9-runtime

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y \
    python3.11 \
    python3-pip \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Ensure pip points to Python 3.11
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Copy and install remaining requirements
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt


# Copy application code
COPY . .

# Expose app port.
EXPOSE 7860

# Run transcribe script to download the model into the container
RUN python3 transcribe.py

# Run the application
CMD ["python3", "app.py"]