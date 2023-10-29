from hume import HumeBatchClient
from hume.models.config import ProsodyConfig


def get_predictions(client, urls, configs):
    job = client.submit_job(configs=configs, urls=urls)
    job.await_complete(timeout=800)
    results = job.get_predictions()
    predictions = []
    for result in results:
        predictions.append(result["results"]['predictions'][0]['models']['prosody']['grouped_predictions'][0]['predictions'])
        return predictions

def get_emotions(predictions):
    total_emotions = []
    for prediction in predictions:
        emotions = []
        for emotion in prediction['emotions']:
            emotions.append(emotion['score'])
        total_emotions.append(emotions)
    return total_emotions

def get_timestamp(predictions):
    timestamps = []
    for prediction in predictions:
        begin = prediction['time']['begin']
        end = prediction['time']['end']
        timestamps.append([begin, end])
    return timestamps

def get_transcript(predictions):
    transcripts = []
    for prediction in predictions:
        transcripts.append(prediction['text'])
    return transcripts

def get_emotions_data(client, urls, configs):
    predictions = get_predictions(client, urls, configs)
    total_emotions = []
    for i in range((len(predictions))):
        file_prediction = predictions[i]
        for j in range(len(file_prediction)):
            segment_prediction = file_prediction[j]
            emotions_data = {}

            emotions_data['transcript'] = segment_prediction['text']
            emotions_data['begin'] = segment_prediction['time']['begin']
            emotions_data['end'] = segment_prediction['time']['end']

            for emotion in predictions[i][j]['emotions']:
                emotions_data[emotion['name']] = emotion['score']
                
            total_emotions.append(emotions_data)

    return total_emotions

