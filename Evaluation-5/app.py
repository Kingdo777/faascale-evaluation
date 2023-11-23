import os
import random
import threading
import time

from flask import Flask, request
import requests
from datetime import datetime, timedelta

import aiohttp
import asyncio
import function_info

import boto3

# probability 表示本地读取的概率，即function位于同一结点的概率
probability = 0.2


class ThreadSafeRandom:
    def __init__(self):
        self.lock = threading.Lock()

    def generate_random_boolean(self):
        with self.lock:
            random_value = random.uniform(0, 1)
            return random_value < probability


ts_random = ThreadSafeRandom()

byte_buffer = bytearray(4096)
byte_value = 0
data_from_redis = None

for index in range(4096):
    byte_buffer[index] = 1

BUCKET = 'kingdo-serverless'
File_KEY = 'faastlane/sentiment/{}'

AWS_ACCESS_KEY_ID = "AKIA2EGUEMCVKZGPBGIC"
AWS_SECRET_KEY_ID = "w9zEt8hTXOkKKbOIc+gWC8FaXfYAkm23b8YhOQ/3"
S3_REGION_NAME = "us-west-2"

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_KEY_ID,
                  region_name=S3_REGION_NAME)


def read_data():
    local = ts_random.generate_random_boolean()
    global byte_value
    global data_from_redis
    if local:
        for i in range(4096):
            byte_value = byte_buffer[i]
        pass
    else:
        # body = s3.get_object(Bucket=BUCKET, Key=File_KEY.format("body"))['Body'].read()
        sleep_microseconds(256 * 1000)
        pass


def write_data():
    local = ts_random.generate_random_boolean()
    if local:
        for i in range(4096):
            byte_buffer[i] = 1
            pass
    else:
        # s3.put_object(Bucket=BUCKET, Key=File_KEY.format("body"), Body=byte_buffer)
        sleep_microseconds(258 * 1000)
        pass


def sleep_microseconds(microseconds):
    end_time = datetime.now() + timedelta(microseconds=microseconds)

    while datetime.now() < end_time:
        pass


async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


app = Flask(__name__)


@app.route('/compose_post')
def compose_post_():
    usetime = request.args.get('usetime', default=0, type=int)
    read_data()
    sleep_microseconds(usetime)
    return "compose_post"


@app.route('/media')
def media():
    sleep_microseconds(function_info.MediaUsetime)
    read_data()
    response = requests.get(
        f"http://127.0.0.1:{function_info.ComposePostPort}/compose_post?usetime={function_info.MediaComposePostUsetime}")
    write_data()
    return "media-" + response.text


@app.route('/user')
def user():
    sleep_microseconds(function_info.UserUsetime)
    read_data()
    response = requests.get(
        f"http://127.0.0.1:{function_info.ComposePostPort}/compose_post?usetime={function_info.UserComposePostUsetime}")
    write_data()
    return "user-" + response.text


@app.route('/unique_id')
def unique_id():
    sleep_microseconds(function_info.UniqueIdUsetime)
    read_data()
    response = requests.get(
        f"http://127.0.0.1:{function_info.ComposePostPort}/compose_post?usetime={function_info.UniqueIdComposePostUsetime}")
    write_data()
    return "unique_id-" + response.text


@app.route('/url_shorten')
def url_shorten():
    sleep_microseconds(function_info.UrlShortenUsetime)
    read_data()
    response = requests.get(
        f"http://127.0.0.1:{function_info.ComposePostPort}/compose_post?usetime={function_info.UrlShortenComposePostUsetime}")
    write_data()
    return "url_shorten-" + response.text


@app.route('/user_mention')
def user_mention():
    sleep_microseconds(function_info.UserMentionUsetime)
    read_data()
    response = requests.get(
        f"http://127.0.0.1:{function_info.ComposePostPort}/compose_post?usetime={function_info.UserMentionComposePostUsetime}")
    write_data()
    return "user_mention-" + response.text


@app.route("/user_timeline")
def user_timeline():
    sleep_microseconds(function_info.UserTimelineUsetime)
    read_data()
    return "user_timeline"


@app.route("/post_storage")
def post_storage():
    sleep_microseconds(function_info.PostStorageUsetime)
    read_data()
    return "post_storage"


async def fetch_upload_text():
    url_user_timeline = f"http://127.0.0.1:{function_info.UserTimelinePort}/user_timeline"
    url_post_storage = f"http://127.0.0.1:{function_info.PostStoragePort}/post_storage"

    tasks = [fetch_data(url_user_timeline), fetch_data(url_post_storage)]

    return await asyncio.gather(*tasks)


@app.route('/upload_text')
def upload_text():
    sleep_microseconds(function_info.UploadTextUsetime)
    read_data()
    results = asyncio.run(fetch_upload_text())
    write_data()
    write_data()
    return "upload_text-[{}]".format(";".join(results))


async def fetch_text():
    url_url_shorten = f"http://127.0.0.1:{function_info.UrlShortenPort}/url_shorten"
    url_user_mention = f"http://127.0.0.1:{function_info.UserMentionPort}/user_mention"
    url_upload_text = f"http://127.0.0.1:{function_info.UploadTextPort}/upload_text"

    tasks = [fetch_data(url_url_shorten), fetch_data(url_user_mention), fetch_data(url_upload_text)]

    return await asyncio.gather(*tasks)


@app.route('/text')
def text():
    sleep_microseconds(function_info.TextUsetime)
    read_data()
    results = asyncio.run(fetch_text())
    write_data()
    write_data()
    write_data()
    return "text-[{}]".format(";".join(results))


async def fetch():
    url_media = f"http://127.0.0.1:{function_info.MediaPort}/media"
    url_user = f"http://127.0.0.1:{function_info.UserPort}/user"
    url_unique_id = f"http://127.0.0.1:{function_info.UniqueIdPort}/unique_id"
    url_text = f"http://127.0.0.1:{function_info.TextPort}/text"

    tasks = [fetch_data(url_media), fetch_data(url_user), fetch_data(url_unique_id), fetch_data(url_text)]

    return await asyncio.gather(*tasks)


@app.route('/')
def front():
    results = asyncio.run(fetch())

    write_data()
    write_data()
    write_data()
    write_data()
    return "front-[{}]\n".format(";".join(results))


@app.route('/hello')
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
