from datetime import datetime, timedelta


# import os
# credential_path = "/Users/jacopominniti/.config/gcloud/application_default_credentials.json"
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


def blobs_to_update(client, id, date):
    sub_bucket = f'{id}_{date}'
    bucket = client.get_bucket('hume_recordings')
    blobs = list(bucket.list_blobs(prefix=sub_bucket))
    blobs = blobs[1:]

    # Get the current time
    now = datetime.now()

    # List to store the public URLs of the blobs
    blob_urls = []
    blob_names = []
    for blob in blobs:
        blob_names.append(blob.name)
        blob_urls.append(blob.public_url)

    # for blob in blobs:
    #     # Get the blob's updated time
    #     blob_updated_time = blob.updated
    #     # Check if the blob was updated in the last day
    #     if (now - blob_updated_time.replace(tzinfo=None)) < timedelta(days=1):
    #         blob_urls.append(blob.public_url)
    
    return [blob_names, blob_urls]
