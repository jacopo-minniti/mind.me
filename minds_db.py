import mindsdb_sdk
import time

# connects to the default port (47334) on localhost
server = mindsdb_sdk.connect()

# connects to the specified host and port
server = mindsdb_sdk.connect('http://127.0.0.1:47334')
emotions_db = server.get_database('my_db')
print('Running')

project = server.get_project()

# prepare the training data
# extracting database from MindsDb cloud

# database consists of multiple schemas
# schema consists of multiple tables

emotions_table = emotions_db.get_table('emotions_table')

# printing first 5 rows as a sample to train model
print('First 5 rows of emotions_table:')
print(emotions_table.limit(5).fetch())


# get all models
model_names = [i.name for i in project.list_models()]

# check for one of the builded models in the models

print('Creating emotions_model model')
emotions_model = project.get_model('j_emotions_model')
# emotions_model = project.create_model(
#     name='j_emotions_model',
#     # in table there should be empty column for filling out predictions

#     # in our previous DB that column is named prompt, but to get better predictions we should specify the purpose of column
#     predict='Suggestions/Advices',

#     # specifying on which table's data model should train
#     query=emotions_table
# )

# so we need an m
print('Created emotions_model successfully:')
print(emotions_model)

print('Waiting for model training to complete...please be patient')
for i in range(400):
    print('.', end='')

    # need import time
    time.sleep(0.5)

    # checking for finishing of model training
    if emotions_model.get_status() not in ('generating', 'training'):
        print('\nFinished training emotions_model:')
        break


# get model's details
print(emotions_model.data)

if emotions_model.get_status() == 'error':
    print('Something went wrong while training:')
    print(emotions_model.data['error'])

# make predictions for example 3
emotions_table_limit = emotions_table.limit(3)

# getting predictions as a dataframe which is ret
print('Making prediction on the first 3 rows of emotions_table')
ret = emotions_model.predict(emotions_table_limit)

# giving output as a 3 column results
print(ret[['user_id', 'transcript', 'Heart Rate BPM', 'Suggestions/Advices']])

'''
'''
# python ./hume/minds_db.py
