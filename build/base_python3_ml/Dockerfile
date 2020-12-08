ARG SV_REGISTRY
FROM ${SV_REGISTRY}/base_python3:1.0.0

RUN \
    pip3 install --upgrade pip && \
    pip3 install opencv-python && \
    pip3 install pandas && \
    pip3 install numpy && \
    pip3 install torch torchvision && \
    pip3 install imgaug && \
    pip3 install albumentations && \
    pip3 install numba

WORKDIR /home/svadm