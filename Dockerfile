FROM python:3.7-slim

COPY ./ /tmp/ducksoak
RUN pip install /tmp/ducksoak/

CMD ["--help"]
ENTRYPOINT ["ducksoak"]

