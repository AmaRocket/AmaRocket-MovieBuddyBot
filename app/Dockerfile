FROM alpine:3.14

#ARG bot_token
#ENV TOKEN=$bot_token

#ARG api_key
#ENV API_KEY=$api_key

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

WORKDIR /usr/src/app/
# copy project
COPY . /usr/src/app/
# install dependencies
RUN pip install -r ../requirements.txt
# run app
CMD ["python", "app.py"]