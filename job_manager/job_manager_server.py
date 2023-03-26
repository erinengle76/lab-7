from flask import Flask, request, jsonify
from job_tasks import countInput, celery_app
from celery.result import AsyncResult

app = Flask(__name__)

@app.route('/count', methods=["POST"])
def countText():
    inputText = request.get_json()
    text = inputText["text"]
    result = countInput.delay(text)
    return jsonify({"id": result.id})

@app.route('/status/<id>', methods=["GET"])
def checkStatus(id):
    try:
        id_record = AsyncResult(id, app=celery_app)

        if id_record.status == "SUCCESS":
            count = id_record.get()
            return jsonify({"Count": count}), 200
        elif id_record.status == "FAILURE":
            return jsonfiy({"Error": "The task was not completed due to an error"}), 400
        elif id_record.status == "PENDING":
            return jsonify({"Pending": "The task is waiting for execution."}), 400
        elif id_record.status == "STARTED":
            return jsonify({"Started": "The task has begun but has not completed"}), 400
        else:
            return jsonify({"Retry": "The task is to be retried. Possible failure"}), 400
    except:
        return jsonify({"Error": "No task with this ID has been instantiated"}), 404
