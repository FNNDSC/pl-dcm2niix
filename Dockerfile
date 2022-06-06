# Caution: this Dockerfile is prone to fail on niche bugs,
# make sure your docker and QEMU binfmt setup are up to date.


# compile dcm2niix from source
FROM alpine:3.16 as builder

RUN apk add build-base git cmake make

WORKDIR /tmp
ADD https://github.com/rordenlab/dcm2niix/archive/refs/tags/v1.0.20211006.tar.gz /tmp/v1.0.20211006.tar.gz
RUN tar xf /tmp/v1.0.20211006.tar.gz

RUN mkdir /tmp/dcm2niix-1.0.20211006/build
WORKDIR /tmp/dcm2niix-1.0.20211006/build
RUN cmake ..
RUN make


# install Python ChRIS plugin
FROM docker.io/python:3.10.4-alpine3.16

LABEL org.opencontainers.image.authors="FNNDSC <dev@babyMRI.org>" \
      org.opencontainers.image.title="pl-dcm2niix" \
      org.opencontainers.image.description="A ChRIS ds plugin wrapper for dcm2niix"

WORKDIR /usr/local/src/pl-dcm2niix

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install .

COPY --from=builder /tmp/dcm2niix-1.0.20211006/build/bin/dcm2niix /usr/local/bin/dcm2niix

CMD ["dcm2niixw", "--help"]
