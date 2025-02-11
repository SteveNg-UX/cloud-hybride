FROM debian:latest

RUN apt-get update -y && \
    apt-get install python3 python3-pip -y && \
    pip3 install starlette pydantic uvicorn "fastapi[standard]" paramiko --break-system-packages
VOLUME /fastapi/ /fastapi
COPY main.py /
CMD ["/bin/bash"]
EXPOSE 80/tcp
