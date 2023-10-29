import os

# Set the path to the credentials file
# THis code needs to be executed just once, and then can be removed.
credential_path = "/Users/USERNAME/.config/gcloud/application_default_credentials.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# blobs are the individual audio files.
# Each blob is divided in a ~ 5 second audio segment, but originally it is a ~ 3 min video file.
# The blobs to update are determined so based on the time.
# In a real world scenario, a cloud function checks when a day or so passed since last report, and analyes the yet not analyzed blobs.
# Thanks to the highly organized structure, you can construct the path easly to get the files.


def blobs_to_update(client, id, date):
    sub_bucket = f'{id}_{date}'
    # this is the constant, first bucket.
    # All recordings are stored in this bucket, but each user has its own sub-bucket.
    bucket = client.get_bucket('hume_recordings')
    blobs = list(bucket.list_blobs(prefix=sub_bucket))
    # When there are other directopries, the first element returned is not a blob.
    blobs = blobs[1:]

    # List to store the public URLs of the blobs
    blob_urls = []
    # List to store the names of the blobs
    blob_names = []
    for blob in blobs:
        blob_names.append(blob.name)
        blob_urls.append(blob.public_url)

    return [blob_names, blob_urls]
