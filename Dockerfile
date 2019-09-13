FROM python:3.7-slim

RUN apt update && \
apt install git -y && \
git clone https://github.com/adamcathersides/ducksoak && \
pip install ducksoak/

ENTRYPOINT ducksoak

