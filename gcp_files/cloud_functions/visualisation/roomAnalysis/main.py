import csv
import io
import json
import pandas as pd
from google.cloud import storage
from flask_cors import cross_origin

client = storage.Client()
bucketName = "visualizations5401"

def openFileAndAddData(row):
    def addData(roomData, data):
        roomData = roomData.append(data, ignore_index=True)
        return roomData
    try:
        bucket = client.get_bucket(bucketName)
        blob = bucket.blob("roomAnalysis.csv")
        csvBytes = io.BytesIO(blob.download_as_string())
        roomDF = pd.read_csv(csvBytes)
        roomDF = addData(roomDF, row)
        bucket.blob("roomAnalysis.csv").upload_from_string(roomDF.to_csv(index=False), 'text/csv')
        return "SUCCESS"
    except Exception as e:
        return str(e)

@cross_origin()
def process_request(request):
    try:
        request_json = request.get_json()
        print(request_json)
        return {"debug": openFileAndAddData(request_json)}
    except Exception as e:
        return "ERROR" + str(e)