#FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
FROM ubuntu:22.04
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apt-get update
RUN apt-get install gcc musl-dev vim build-essential software-properties-common python3 python3-pip -y
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install -Uqq fastai
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
EXPOSE 9191
COPY . .
CMD ["python3", "main.py"]
