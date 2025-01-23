FROM node:22-alpine AS frontend

WORKDIR /usr/app/

COPY package.json ./package.json
COPY package-lock.json ./package-lock.json
COPY src/frontend ./src/frontend

RUN npm install

RUN npm run build

FROM python:3.12.7-alpine AS backend

WORKDIR /usr/app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . /usr/app

COPY --from=frontend /usr/app/src/frontend/static /usr/app/src/frontend/static

EXPOSE 8080

CMD ["python", "main.py"]
