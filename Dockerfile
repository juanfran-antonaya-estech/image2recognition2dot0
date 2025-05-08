FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt setup_env.sh ./

# Install virtualenv and create a virtual environment
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir --upgrade pip virtualenv \
    && virtualenv venv \
    && . venv/bin/activate \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x setup_env.sh && ./setup_env.sh

EXPOSE 5000

ENV ENV=dev

# Use the virtual environment to run the application
ENTRYPOINT ["/bin/bash", "-c", "source venv/bin/activate && exec python src/main.py \"$@\"", "--"]

