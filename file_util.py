import logging
import os
from gcloud import storage
import time

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

# The “folder” where the files you want to download are on google stirage

delimiter='/'
environment = ''
bucket = ''
folder = ''


def uploadOneFile(folder,filename,file):
    logging.info('Inside File Uploads')
    timestamp = int(time.time())
    try:
        blob = bucket.blob(folder+delimiter+filename+'_'+str(timestamp)+'.csv')
        #blob.upload_from_filename('question-answer/filename.csv')
        blob.upload_from_filename(file)
    except Exception as ex:
        logging.error("Exception occurred while trying to upload files " , ex)


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
    logging.info('Inside init',environment)

    if environment == 'LOCAL':
        bucket_name = 'mgmt590-storage'
        storage_client = storage.Client.from_service_account_json('credentials.json')
        bucket = storage_client.get_bucket(bucket_name)
        folder = 'question-answer'
    elif environment == 'PROD':
        bucket_name = os.environ.get('STORAGE_BUCKET')
        storage_client = storage.Client.from_service_account_json(os.environ.get('GCP_SA_KEY'))
        bucket = storage_client.get_bucket(bucket_name)
        folder = 'question-answer'


if __name__ == '__main__':
    init('LOCAL')
    #downloadFiles()
    #deleteFiles()
    #uploadFiles()
    delete_one_file(folder,'testAnswer.csv')


