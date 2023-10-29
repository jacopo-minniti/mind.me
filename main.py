from hume import HumeBatchClient
from hume.models.config import ProsodyConfig
from google.cloud import storage
import database_connection as db

import hume_helpers as hh
import google_storage_helpers as gsh
from api_keys import HUME_API_KEY, GPT3_API_KEY, GOOGLE_APPLICATION_CREDENTIALS

hume_client = HumeBatchClient(HUME_API_KEY)
storage_client = storage.Client(project=GOOGLE_APPLICATION_CREDENTIALS)
print('Clients initialized')

configs = [ProsodyConfig()]

# in a real context, these would be retrieved from the database
user_id = 1
date = '2023_10_28'

[blob_ids, urls] = gsh.blobs_to_update(storage_client, user_id, date)
print('urls retrieved')
print('Running predictions...')

emotions_data = hh.get_emotions_data(hume_client, urls, configs)
print('Emotional Data retrieved')


db.connect_and_execute({'emotions_data': emotions_data, 'user_id': user_id})
# python -m mindsdb
# python ./hume/main.py




