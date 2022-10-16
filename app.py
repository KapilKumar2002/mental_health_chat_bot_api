from flask import Flask, jsonify, request, Response
import json
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
from difflib import SequenceMatcher as SM
import os
import pandas as pd
import numpy as np

# body = ""
response = ""

# from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def nameRoute():
    global response
    if(request.method == 'POST'):
        request_data = request.data  # getting the response data
        # converting it from json to key value pair
        request_data = json.loads(request_data.decode('utf-8'))
        name = request_data['name']  # assigning it to name
        body = name
        for dirname, _, filenames in os.walk('/kaggle/input'):
            for filename in filenames:
                print(os.path.join(dirname, filename))
        data = pd.read_csv('Mental_Health_FAQ.csv')
        dataframe = data[['Questions', 'Answers']]
        dataframe['similarity_ratio'] = dataframe.apply(lambda x: SM(None, body, x.Questions).ratio(), axis=1)


        Score = dataframe['similarity_ratio']
        # print(Score.max())
        val = Score.max()
        max_score = Score.idxmax()
        Answer = dataframe['Answers'].iloc[max_score]
        if (val > 0.5): 
            response = Answer
        else: 
            response = "Sorry! we are working on dataset. please, Ask another query from above!"
        # re-assigning response with the name we got from the user
        return ""
    else:
        return jsonify({'name' : response})






if __name__ == "__main__":
    app.run(debug=True)





