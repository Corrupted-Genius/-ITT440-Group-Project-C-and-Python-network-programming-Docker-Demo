FROM gcc:latest

RUN apt-get update && apt-get install -y default-libmysqlclient-dev

WORKDIR /app

COPY server.c .

RUN gcc server.c -o server -lmysqlclient

CMD ["./server"]