![Xthin Header (1)](https://github.com/jacopo-minniti/mind.me/assets/115539886/faf2fc57-c6f2-4501-bad4-03519f6a1814)
# mind.me

### Your emotions, finally on your side. 

## What is mind.me
Mind.me is a pioneering integrated system designed to enhance users’ emotional awareness and empower them to manage and improve their emotional well-being in both the short and long term.

By collecting data from recordings, heart rate, blood pressure, and other scientifically-based predictors, it tracks your mood throughout the day, 24 hours a day. It uncovers trends and patterns which are then used to generate personalized, detailed, and specific suggestions and advice. These recommendations are interactive and genuinely useful, thanks to numerous integrations with third-party apps.
![Presentation UI](https://github.com/jacopo-minniti/mind.me/assets/115539886/7b1ddacf-de79-44bf-b207-90c0548bcf30)


Using Mind.me is as simple as wearing a watch. It operates in the background and never requires any input from you - it simply provides output.

The data we collect from you remains yours, and we use it solely for your benefit to make predictions.

## How it is built 
![FINALXOVERVIEW](https://github.com/jacopo-minniti/mind.me/assets/115539886/a3b49bbb-035a-4f87-b5a5-86c69b4c0e9b)
Mind.me is a comprehensive system that includes a front-end application, constructed using the Zepp Framework directly on the watch, and a user-exclusive webpage. This webpage provides detailed explanations of the user's emotional status, more refined prompts, and trends and graphs that allow users to understand their long-term emotional trajectory.

Powered by MindsDB, Mind.me enables swift integration of the MySQL database in the backend and machine learning models. It leverages GPT3.5 Turbo, one of the most sophisticated generative AI tools, to construct the most human-like, detailed suggestions.

The system utilizes a total of 57 predictors, which include (i) health data captured through the Zepp Watch sensors (e.g., heart rate), and (ii) emotions mapped throughout the day via the user's voice and discourse.

To convert voice into emotions, Mind.me employs Hume API, which utilizes highly sophisticated, state-of-the-art deep learning models specifically designed for this purpose.

All data is stored in a MySQL database in the backend. To ensure optimal performance, .wav files are stored separately on Google Cloud Storage.

Python scripts are deployed as cloud functions through Google Clouds, and a custom API connects the webpage to the database.


## What's next 
The path is still long. This application has the potential to change the lives of millions of people around the World. The improvements, through third-party integrations and more complex data analytics, will constitute the biggest objective of its future development. 




