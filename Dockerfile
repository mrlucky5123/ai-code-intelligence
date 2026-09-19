FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
    g++ \
    clang \
    clang-tools \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace