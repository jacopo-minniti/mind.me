from hume import HumeBatchClient
from hume.models.config import ProsodyConfig

# the following function uses the Hume API to get the predictions
# each emotions is a value from 0 to 1; the higher, the more intense the emotion.
# It is important to note how the values of all the emotions do not sum up to 1, as one can be at the same time highly calm and happy, for example.
# The emotions are 48 in total.


def get_predictions(client, urls, configs):
    job = client.submit_job(configs=configs, urls=urls)
    # timeout is increased signficicantly. COnsidering this operation is to be executed once per day (for each user),
    # there is no excessive need for speed, and it is more important that the transaction is completed.
    # notice this is an async block
    job.await_complete(timeout=800)
    results = job.get_predictions()
    predictions = []
    for result in results:
        # This long line is to get the actual predictions from the results.
        # The structure of the json file retrieved is highlt complex and convulted.
        # Considering that most of the data is useless for our purposes, we reduce the data to be sent to the database considerably.
        # Fundamentally, we are only interested in the final dictionary with the emotions mapped.
        predictions.append(result["results"]['predictions'][0]['models']
                           ['prosody']['grouped_predictions'][0]['predictions'])
        return predictions

# The following functions are used to get the specific components of the predictions list.
# Remember as audio files are segnmented in  ~ 5 second audio files, so the list will grow linearly with longer videos.

# Returns a list of maps.
# Each map is a dictionary with the emotions as keys and the values as the score of the emotion


def get_emotions(predictions):
    total_emotions = []
    for prediction in predictions:
        emotions = []
        for emotion in prediction['emotions']:
            emotions.append(emotion['score'])
        total_emotions.append(emotions)
    return total_emotions

# Returns a list of lists.
# Each list is [begin, end] timestamp for the specific segment of the audio file.


def get_timestamp(predictions):
    timestamps = []
    for prediction in predictions:
        begin = prediction['time']['begin']
        end = prediction['time']['end']
        timestamps.append([begin, end])
    return timestamps


# Returns a list of strings.
# Each string is the transcript of the specific segment of the audio file.
def get_transcript(predictions):
    transcripts = []
    for prediction in predictions:
        transcripts.append(prediction['text'])
    return transcripts

# Returns the cohmprensive data.
# The others function are needed in specific contexts, while this returns the data in a format that can be easily used for the database.
# It returns everything we need to uploda from Hume.


def get_emotions_data(client, urls, configs):
    predictions = get_predictions(client, urls, configs)
    total_emotions = []
    for i in range((len(predictions))):
        file_prediction = predictions[i]
        for j in range(len(file_prediction)):
            segment_prediction = file_prediction[j]
            # create a dictionary to store the data of the single file.
            emotions_data = {}
            # add the individual parts
            emotions_data['transcript'] = segment_prediction['text']
            emotions_data['begin'] = segment_prediction['time']['begin']
            emotions_data['end'] = segment_prediction['time']['end']

            for emotion in predictions[i][j]['emotions']:
                emotions_data[emotion['name']] = emotion['score']

            total_emotions.append(emotions_data)

    return total_emotions
