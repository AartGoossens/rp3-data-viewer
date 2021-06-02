FROM python:3.9

WORKDIR /tmp
RUN python -m pip install --upgrade pip

COPY requirements.txt /tmp/
RUN python -m pip install -r requirements.txt

RUN mkdir /app
WORKDIR /app
COPY . /app/

ENV PORT 8080
EXPOSE 8080

CMD streamlit run --server.enableCORS false --server.port=8080 main.py
