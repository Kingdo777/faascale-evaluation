import boto3
import random
import threading
import time
import json

# probability 表示本地读取的概率，即function位于同一结点的概率
probability = 0


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
        body = s3.get_object(Bucket=BUCKET, Key=File_KEY.format("body"))['Body'].read()
        pass


def write_data():
    local = ts_random.generate_random_boolean()
    if local:
        for i in range(4096):
            byte_buffer[i] = 1
            pass
    else:
        s3.put_object(Bucket=BUCKET, Key=File_KEY.format("body"), Body=byte_buffer)


def lambda_handler(event, context):
    start_time = time.time()
    for i in range(1):
        write_data()
        # read_data()
    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000
    print("use {} ms".format(elapsed_time))
    return {
        'statusCode': 200,
        'body': json.dumps("use {} ms".format(elapsed_time))
    }


if __name__ == '__main__':
    lambda_handler("", "")
