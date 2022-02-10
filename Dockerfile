FROM alpine:3.14



RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

WORKDIR /usr/src/app/
# copy project
COPY ./app/ /usr/src/app/
# install dependencies
COPY ./requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt && rm -f /tmp/requirements.txt
# run app
CMD ["python", "app.py"]
