# ==================================================================
# module list
# ------------------------------------------------------------------
# python        3.6    (apt)
# tensorflow    1.15 (pip)
# ==================================================================

FROM tensorflow/tensorflow:1.15.4-gpu
ENV LANG C.UTF-8
RUN APT_INSTALL="apt-get install -y --no-install-recommends" && \
    PIP_INSTALL="pip --no-cache-dir install --upgrade" && \
    GIT_CLONE="git clone --depth 10" && \

    apt-get update && \

# ==================================================================
# tools
# ------------------------------------------------------------------

    DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
        apt-utils \
        build-essential \
        ca-certificates \
        openssh-server \
        net-tools \
        iputils-ping \
        cmake \
        wget \
        git \
        vim \
        libssl-dev \
        libxss1 \
        libgl1-mesa-glx \
        htop \
        curl \
        unzip \
        unrar \
        && \

# ==================================================================
# python
# ------------------------------------------------------------------

    DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
        software-properties-common \
        && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
        python3.6 \
        python3.6-dev \
        python3-distutils-extra \
        && \
    wget -O ~/get-pip.py \
        https://bootstrap.pypa.io/get-pip.py && \
    python3.6 ~/get-pip.py && \
    rm -r -f /usr/local/bin/python* && \
    ln -s /usr/bin/python3.6 /usr/local/bin/python3 && \
    ln -s /usr/bin/python3.6 /usr/local/bin/python && \
    $PIP_INSTALL \
        psutil \
        numpy \
        scipy \
        pandas \
        cloudpickle \
        Cython \
        tqdm \
        && \

# ==================================================================
# tensorflow
# ------------------------------------------------------------------

    $PIP_INSTALL \
        tensorflow-gpu==1.15.4 \
        tensorflow-probability~=0.7 \
        && \

# ==================================================================
# framework
# ------------------------------------------------------------------

    $PIP_INSTALL \
        pyarrow \
        pyzmq \
        opencv-python \
        atari-py \
        gym \
        horovod \
        psutil \
        influxdb \
        && \

# ==================================================================
# config & cleanup
# ------------------------------------------------------------------

    ldconfig && \
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/* /tmp/* ~/*

EXPOSE 6006