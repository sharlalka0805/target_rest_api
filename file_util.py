import logging
import os
from gcloud import storage
import time
import base64
import stat
from werkzeug.utils import secure_filename

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

delimiter='/'
environment = ''
bucket = ''


def uploadOneFile(bucket,filename):
    logging.info('Inside File Uploads')
    try:
        blob = bucket.blob(filename)
        response = blob.upload_from_filename(filename)
    except Exception as ex:
        logging.error("Exception occurred while trying to upload files " , ex)
    return response


def downloadFiles(folder):
    logging.info('Inside Download Files')

    # Create this folder locally if not exists
    if not os.path.exists(folder):
        os.makedirs(folder,mode=0o777)
    try:
        blobs = bucket.list_blobs(prefix=folder)
        for blob in blobs:
            blob.download_to_filename(blob.name)
    except Exception as ex:
        logging.error("Exception occurred while trying to download files " , ex)


def deleteAllFiles(folder):
    logging.info('Inside delete files')
    try:
        bucket.delete_blobs(blobs=list(bucket.list_blobs(prefix=folder)))
    except Exception as ex:
        logging.error("Exception occurred while trying to delete files ",ex)


def delete_one_file(folder,filename):
    logging.info('Inside delete files')
    try:
        blob = bucket.blob(folder+delimiter+filename)
        blob.delete()
    except Exception as ex:
        logging.error("Exception occurred while trying to delete files ",ex)


def init(environment):
    print('Inside init',environment)

    if environment == 'LOCAL':
        bucket_name = 'mgmt590-storage'
        storage_client = storage.Client.from_service_account_json('credentials.json')
        bucket = storage_client.get_bucket(bucket_name)
    elif environment == 'PROD':
        bucket_name = os.environ.get('STORAGE_BUCKET')
        getCrededential()
        print('After get credentials')
        storage_client = storage.Client()
        print('After storage_client')
        bucket = storage_client.get_bucket(bucket_name)
        print('After bucket')
    return bucket


def getCrededential():
    print('Inside getCrededential')
    filecontents = os.environ.get('GCS_CREDS')
    print('Inside getCrededential --> found creds')
    filecontents = filecontents.replace('@', '=')
    print('Inside getCrededential --> replaced creds creds',filecontents)
    decoded_cred = base64.b64decode(filecontents)
    print('Inside getCrededential --> decoded creds creds')
    file = open("/creds.json", "wb")
    file.write(decoded_cred)
    print('Inside getCrededential --> write file')
    file.close()
    os.chmod("/creds.json", stat.S_IRUSR)
    os.chmod("/creds.json", stat.S_IWUSR)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/creds.json"

if __name__ == '__main__':
    bucket = init('LOCAL')
    downloadFiles('/question-answer')
    #deleteFiles()
    #uploadFiles()
    #delete_one_file(folder,'testAnswer.csv')


