FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    UV_HTTP_TIMEOUT=120 \
    UV_CONCURRENT_DOWNLOADS=1 \
    MPLCONFIGDIR=/tmp/matplotlib

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libgl1 libegl1 libgles2 libglib2.0-0 libsm6 libice6 libdbus-1-3 \
        libfontconfig1 fonts-dejavu-core libx11-xcb1 libxkbcommon0 libxkbcommon-x11-0 \
        libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 \
        libxcb-shape0 libxcb-sync1 libxcb-xfixes0 libxcb-xinerama0 libxcb-xkb1 \
        libportaudio2 libasound2-plugins \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --default-timeout=120 --retries 10 uv

WORKDIR /app

COPY pyproject.toml .
RUN uv pip install --system -r pyproject.toml