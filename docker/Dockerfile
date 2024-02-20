FROM ros:noetic-ros-base-focal

# libGL.so.1 
# source: https://stackoverflow.com/questions/55313610/importerror-libgl-so-1-cannot-open-shared-object-file-no-such-file-or-directo
RUN apt update && apt install ffmpeg libsm6 libxext6 python3-pip -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip && python3 -m pip install opencv-python tqdm

WORKDIR /data

