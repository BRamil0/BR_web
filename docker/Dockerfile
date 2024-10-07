FROM python:3.12.4-alpine

WORKDIR /usr/app


COPY requirements.txt ./
COPY src ./src
COPY main.py ./
COPY LICENSE ./

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD ["python", "main.py"]