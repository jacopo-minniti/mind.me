# In main.py, most of other scripts are executed or used as helpers.
# The objective is:
#   1. Retrieve audio data from the stroage bucket
#   2. Run the audio data through Hume to get emotions predictios
#   3. Store the emotions predictions in the database


from hume import HumeBatchClient
from hume.models.config import ProsodyConfig
from google.cloud import storage
import database_connection as db

import hume_helpers as hh
import google_storage_helpers as gsh
from api_keys import HUME_API_KEY, GPT3_API_KEY, GOOGLE_APPLICATION_CREDENTIALS

hume_client = HumeBatchClient(HUME_API_KEY)

# Google Cloud Storage was chosen as the storage solution for this project, because:
#   1. It is a cloud-based storage solution, which means it is accessible from anywhere
#   2. It is a cost-effective solution, because it is a pay-as-you-go service
#   3. It is a highly scalable solution
#   4. The data did not need any particular ordering or structure, so a NoSQL was great.
#
storage_client = storage.Client(project=GOOGLE_APPLICATION_CREDENTIALS)
print('Clients initialized')

# The configs, necessary for Hume operations, can speicfy multiple models,
# that take as data different sources (audio, text, etc.). In our  case, considering how
# it would have been cumbersome (and not respectful of privacy at all), we chose to considere
# exclusevely audio recordings.
configs = [ProsodyConfig()]

# in a real context, these would be retrieved from the database.
# In the google cloud storage bucket, the audio files are stored in a folder structure like this:
#   - Hume Recordings
#       - user_id
#           - date
#               - audio_file
# The files are uploaded to Cloud Storage from the Zepp watch, and they are about 3 minutes long each
# The audio files are stored in the bucket in the following format: user_id_date_time
# They are quite short, as batching more requests in one is faster than one giant file with the batch Hume API.


# Examples of user_id (unique integer) and date (string in the format YYYY_MM_DD)
user_id = 1
date = '2023_10_28'

# Retrieve urls, and blob_ids from the storage bucket
# On the database, we store just the public url, not the file itself, as it would be too expensive
[blob_ids, urls] = gsh.blobs_to_update(storage_client, user_id, date)
print('urls retrieved')
print('Running predictions...')

# Run predictions on the retrieved urls.
# The predictions are returned in the format of a list of dictionaries.
emotions_data = hh.get_emotions_data(hume_client, urls, configs)
print('Emotional Data retrieved')

# After having retrieved the emotions data, we can update the database with it.
db.connect_and_execute({'emotions_data': emotions_data, 'user_id': user_id})
