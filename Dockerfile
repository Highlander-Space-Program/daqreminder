FROM ghcr.io/astral-sh/uv:debian
RUN mkdir -p /daqreminder
WORKDIR /daqreminder
RUN uv venv
COPY pyproject.toml .
COPY uv.lock .
RUN uv sync
COPY . .
CMD ["uv", "run", "daqreminder"]
