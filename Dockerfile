FROM index.alauda.cn/library/python:2.7
MAINTAINER Kxrr
ENV LANG C.UTF-8
RUN echo Asia/Shanghai > /etc/timezone && dpkg-reconfigure --frontend noninteractive tzdata
RUN sed -i 's/deb.debian.org/mirrors.163.com/g' /etc/apt/sources.list \
    && sed -i 's/httpredir.debian.org/mirrors.163.com/g' /etc/apt/sources.list \
    && sed -i '/security.debian.org/d' /etc/apt/sources.list
RUN apt-get update \
    && apt-get install -y \
    gcc \
    git \
    libmysqlclient-dev \
    build-essential \
    python-dev

RUN mkdir /dist
WORKDIR /dist
