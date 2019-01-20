from pymongo import *
import os
import logging
import datetime
log_filename = str(datetime.datetime.now().strftime('%d-%m-%Y')) + '.log'
print(log_filename)

# We put a name to identify the origin of the log
logger = logging.getLogger('mongodb')
logging.basicConfig(filename=log_filename, filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger.info("Trying to connect to database")

# Include URI of MongoDB in localhost
direccion = str(os.environ.get("IP", "10.0.0.4"))
print(direccion)
logger.info("IP of MongoDB database established")
MONGODB_URI = "mongodb://"+ direccion + ":27017/predictions"

# MONGODB_URI = "mongodb://127.0.0.1:27017/predictions"
# MONGODB_URI = "mongodb://test:test_password1@ds123584.mlab.com:23584/predictions"
logger.info("Succesfully connected to database")


client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
db = client.get_database("predictions")
mongoPrediction = db.mongoPrediction

#-------------------------------------------------------------------------------
# Function if we want to get a prediction from the Database
# This function has only one parameter: ID from the prediction that we want to
# get
def getDocument(document_id):

    logger.info("Request to query to the database...")
    predictionDocument = mongoPrediction.find_one({"ID":document_id})
    logger.info("Succesfully got document from collection")
    return predictionDocument

#-------------------------------------------------------------------------------
# Function pushDocument
# With this function, we can add a new document in the collection
def pushDocument(document):
    logger.info("Request to access to the database...")
    mongoPrediction.insert_one(document)
    logger.info("Succesfully pushed document to the collection")
    pass
#-------------------------------------------------------------------------------
# Function updateDocument
# With this function, we can update an existent document from the database
def updateDocument(document, updates):
    logger.info("Request to access to the database...")
    mongoPrediction.update_one({'_id': document['_id']},{'$set': updates}, upsert=False)
    logger.info("Succesfully updated document in the collection")
    pass
#-------------------------------------------------------------------------------
# Function to get a cursor with the whole content of the Database
def get_all_predictions():
    logger.info("Request to query to the database...")
    return mongoPrediction.find({})
    logger.info("Succesfully updated document in the collection")
    pass

#-------------------------------------------------------------------------------
# With this function we can delete from the database the document in the parameter
def delete_document(document):
    logger.info("Request to access to the database...")
    mongoPrediction.delete_one(document)
    logger.info("Succesfully deleted document from collection")
    pass
#-------------------------------------------------------------------------------
# With this function we can get the size of the database in terms of the number
# of documents in the database
def get_number_documents():
    logger.info("Request to query to the database...")
    return mongoPrediction. estimated_document_count()
    logger.info("Succesfully processed side of the collection")

#-------------------------------------------------------------------------------
# Function to delete all the documents in the database. Util when we want to test
# the functionality of the database with not real params
def delete_all_documents():
    logger.info("Request to query to the database...")
    mongoPrediction.delete_many({})
    logger.info("Succesfully deleted all the content of the collection")
    pass
