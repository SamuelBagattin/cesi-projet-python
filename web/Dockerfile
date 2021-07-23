FROM node as builder
COPY . .
RUN apt install python2 -y && cd frontend && yarn install --frozen-lockfile && \
         yarn run build:unix

FROM alpine
WORKDIR /web
COPY --from=builder . .
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python && \
     python3 -m ensurepip && \
     pip3 install --no-cache --upgrade pip setuptools && \
     pip3 install -r requirements.txt && \

ENTRYPOINT ["python3","./app.py"]
