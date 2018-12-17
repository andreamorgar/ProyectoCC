#!flask/bin/python
from flask import Flask, jsonify
from flask import make_response
from flask import request
from flask import abort
import weather_class as weather
import json
import os
import logging

import datetime


from predictionDB import getDocument, pushDocument, updateDocument
from predictionDB import get_all_predictions, delete_document

app = Flask(__name__)

# Definimos el nombre del fichero de logs.
log_filename = str(datetime.datetime.now().strftime('%d-%m-%Y')) + '.log'
logger = logging.getLogger('flask-app')

logging.basicConfig(filename=log_filename, filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


predictions = []
predictions_objects = []


@app.route('/')
def get_home():
    return jsonify(status='OK')



 # ------------------------------------------------------------------------------

# Now let's write the second version of the GET method for our predictions resource.
# If you look at the table above this will be the one that is used to return the
# data of a single prediction:
@app.route('/predictions/<int:prediction_id>', methods=['GET'])
def get_prediction(prediction_id):
    if request.method == 'GET':
        # We want to find in the collection the document with the ID equal to




        result = getDocument(prediction_id)
        if result is None:
            abort(404)

        result.pop('_id')
        # we set the format of the log message we want to use
        logging.basicConfig(filename=log_filename, filemode='a', format='%(name)s - %(levelname)s - %(message)s')
        logger.warning('GET request')

        return jsonify(result)
# ------------------------------------------------------------------------------

def get_predictions():

    #first we get all the documents of the database by an empty search
    cursor = get_all_predictions()
    actual_list_of_preds = []

    # We have to look in every document to the cursor to get a list of the
    # documents (we can't just print a cursor type)
    for document in cursor:
        next_dict = document
        next_dict.pop('_id')
        # we add the next document to the list of documents that we are
        # going to print
        actual_list_of_preds.append(next_dict)


    return jsonify({'predictions': actual_list_of_preds })

# ------------------------------------------------------------------------------
# Method with POST
# We are going to add a new prediction
@app.route('/predictions', methods=['GET','PUT', 'POST', 'DELETE'])
def create_prediction():
    #Depending of the especification in curl, we can do different things

    # If we detect we want to do a GET of the prediction we have registered...
    if request.method == 'GET':
        return get_predictions();
    # --------------------------------------------------------------------------

    # If we detect we want to do a PUT of a new prediction ...
    elif request.method == 'PUT':
        # Create an object from class Prediction with the information inserted
        # in the curl
        prediction = weather.Prediction(request.json['city'],request.json['temperature'] )

        # We push the new prediction to the Database
        record = {
            "ID": prediction['ID'],
            "city": prediction['city'],
            "date": prediction['date'],
            "temperature": prediction['temperature']
        }
        pushDocument(record)

        return jsonify(prediction.__dict__)

    # --------------------------------------------------------------------------
    elif request.method == 'POST':

        # We get from the request the value of the attributes we want to update
        id = request.json['ID']
        city = request.json['city']
        temperature = request.json['temperature']

        pred = getDocument(id)
        # If the document we are looking for doesn't exist, we abort the update
        if pred is None:
            return abort(404)

        # We have to build a dictionary with the changes we want to submit
        record = {
            "city": city,
            "temperature": temperature
        }

        # We update the document of the database
        updateDocument(pred,record)

        # We access to the database to get the updated document
        updated_pred = getDocument(id)

        # We are going to show the content of the query, so we have to ommit the
        # id that the database add to our query
        updated_pred.pop('_id')

        return jsonify({'prediction': updated_pred}),201


    # --------------------------------------------------------------------------
    elif request.method == 'DELETE':
        # Search for the prediction with the ID introduced
        id = request.json['ID']
        not_wanted_query = getDocument(id)

        # If the document we are looking for doesn't exist, we do nothing
        if not_wanted_query is None:
            return jsonify({'msg': "Deleted"})

        # If the document we are looking for exists, we can delete it with the
        # function delete_document.
        delete_document(not_wanted_query)


        return jsonify({'msg': "Deleted"})




# ------------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    # logger.info('Starting service at port %s ...', port)
    logger.info('Starting service....')
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port,debug=True)

    logger.info('Flask app have just started!')
    # app.run(debug=True) # pragma: no cover
