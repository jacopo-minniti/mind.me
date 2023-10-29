import mindsdb_sdk
from api_keys import GPT3_API_KEY

server = mindsdb_sdk.connect()

# connects to the specified host and port
server = mindsdb_sdk.connect('http://127.0.0.1:47334')
# gets the server istance.
emotions_db = server.get_database('emotions_db')
print('Running')

# check if the project exists
# if it does, it access it thoug the get_project('name') method
# otherwise it creates it with the create_project('name') method
project_exists = False
project = ''
# list all the projects istances in the MindsDB server.
for pg in server.list_projects():
    if (pg.name == 'emotions_pj'):
        project_exists = True
        break
if (project_exists):
    project = server.get_project('emotions_pj')
else:
    project = server.create_project('emotions_pj')
    print('Create Project')

# for the sake of simplicity, in our mysql database, we have only one table with all the features to make the desired predictions.
# the table emotions_table has in total 57 columns.
emotions_table = emotions_db.get_table('emotions_table')

# the same procedure is adopted for the model
model_exists = False
model = ''
for md in project.list_models():
    if (md.name == 'babbage-002'):
        model_exists = True
        break
if (model_exists):
    model = project.get_model('babbage-002')
else:
    model = project.create_model(
        name='babbage-002',
        # the column we want to predict is the suggestion/advice.
        # Using the ones already produced by us (integrated learning) and the 50+ predictors of emotions and health records
        # from Zepp watch, we are going to predict how the user can improve his emotional status, though presionalized suggestions
        # and integrations with other apps. In its final form, Mind.me finds pattern and trends, and functions as a personal coach
        # which finds new, interactive, personalized ways to improve the user's emotional status.
        predict='suggestion/advice',
        # The engine was created though the console.
        engine='emotions_engine',
        options={
            'model_name': 'babbage-002',
            # The api key permits to use GPT3.5 Turbo
            'api_key': GPT3_API_KEY,
            # the prompt template is used to train the model. In particular considering we do not have access to GPT4,
            # we generated a very precise and long prompt, to be sure the model does not produce inaccurate or inconsistent results.
            'prompt_template': 'You are a sentiment classifier. Your role is to help users take back control of their emotions. You will inform them of trends, suggest them possible reasons behind some emotional status, and advice on strategies, based on their personality, to improve their emotional status. These advices should be as specific as possible. To make predictions you will use any other column in the table as input. You will analyze the column {{transcript}}, and all the columns with a score about emotions. That score is a number from 0 to 1 which indicates how much the text in the column is related to that emotion. Above all, you will use the column {{Suggestions/Advices}} as input. This is your main source. These suggestions are your labels, how to predict future entries. Your will return {{Suggestions/Advices}} with the appropriate response. If the value of the column is no, it needs to be updated. Do not produce one word answers. Your feedback has to be 3-4 sentences long. Do not create different suggestions for each row, but instead use small batchs of rows to create one suggestion and replicte it for some rows. The output is always a string, between 3-4 sentences. Your returning value is {{Suggestions/Advices}}.',
            # to avoid useless, not-premeditated expenses, the token limit is set to 500.
            'max_tokens': 500
        }
    )
    print('Create Model')

# Possible predictions. These are not useful for the actual product, and are used only for testing purposes.
table_limit = emotions_table.limit(1)
print('Making prediction on the first 1 rows of the table')
ret = model.predict(table_limit)
print(ret['suggestion/advice'])

