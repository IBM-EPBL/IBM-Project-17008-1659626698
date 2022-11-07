from flask import Flask, redirect, url_for, render_template, request
import ibm_boto3
from ibm_botocore.client import Config, ClientError
# pip install -U ibm-cos-sdk
# pip install boto3

COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud/"
COS_API_KEY_ID = "nw0BvOD3AvTujQIMR6J6EVRv4psh8k9WBlYzMbfuaC0B"
COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/ffb85495cc3d4405a6f4ee90ce586ccc:3c1cf5ee-2a46-4912-9dd2-93c12f281f81::"




cos = ibm_boto3.resource("s3",
                         ibm_api_key_id=COS_API_KEY_ID,
                         ibm_service_instance_id=COS_INSTANCE_CRN,
                         config=Config(signature_version="oauth"),
                         endpoint_url=COS_ENDPOINT
                         )

app = Flask(__name__)


def get_bucket_contents(bucket_name):
    print("Retrieving bucket contents from: {0}".format(bucket_name))
    try:
        files = cos.Bucket(bucket_name).objects.all()
        files_names = []
        for file in files:
            files_names.append(file.key)
            print("Item: {0} ({1} bytes).".format(file.key, file.size))
        return files_names
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))


@app.route('/')
def index():
    files = get_bucket_contents('storagebucketdemo')
    return render_template('index.html', files=files)


if __name__ == '__main__':
    app.run()