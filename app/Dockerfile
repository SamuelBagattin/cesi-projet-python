FROM alpine
WORKDIR /app
COPY . .
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python && \
     python3 -m ensurepip && \
     pip3 install --no-cache --upgrade pip setuptools && \
     pip3 install -r requirements.txt
RUN ls -lat
ENTRYPOINT ["python3","./app.py"]
