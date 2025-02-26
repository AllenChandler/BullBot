FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y python3 python3-pip && \
    pip install --no-cache-dir torch torchvision torchaudio

CMD ["/bin/bash"]
