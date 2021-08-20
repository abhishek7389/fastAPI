import os
from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel
from google.cloud import pubsub

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "/home/abhisheksharma/Downloads/voval_key.json"

app = FastAPI()

sensors = {
  1: {
        "sensor_type" : "GPS Sensor",
        "value_1": "123",
        "value_2": "456"
  }
}

class Sensor(BaseModel):
    sensor_type: str
    value_1: int
    value_2: int

class UpdateSensor(BaseModel):
    sensor_type: Optional[str] = None
    value_1: Optional[int] = None
    value_2: Optional[int] = None

@app.get("/")
def main():
    return {'name': 'your name'}

@app.get("/get-sensor/{sensor_type}")
def get_sensor(sensor_type: int = Path(None, description="Please add the sensor type you want to get response", gt=0)):
    return sensors[sensor_type]

@app.get("/sensor-type")
def sensor_details(*, value: Optional[str] = None, test_value: Optional[int] = None):
    for sensor_id in sensors:
        if sensors[sensor_id]["sensor_type"] == value:
            return sensors[sensor_id]
        
    return {"data": "Data Not Found Please Try Another One"}

@app.get("/sensor-type/{sensor_type}")
def sensor_details_2(*, sensor_type: int, value: Optional[str] = None, test_value: Optional[int] = None):
    '''for sensor_id in sensors:
        if sensors[sensor_id]["sensor_type"] == value:'''
    return sensors[sensor_type]
        
    #eturn {"data": "Data Not Found Please Try Another One"}

@app.post("/add-sensor/{sensor_id}")
def add_sensor(sensor_id: int, sensor: Sensor):
    if sensor_id in sensors:
        return{"Error": "Already Present in the Database"}

    sensors[sensor_id] = sensor
    return sensors[sensor_id]

@app.put("/update-data/{sensor_id}")
def update_data(sensor_id: int, sensor: UpdateSensor):
    if sensor_id not in sensors:
        return {"Error": "Sensor is not present in the database"}
    if sensor.sensor_type != None:
        sensors[sensor_id].sensor_type = sensor.sensor_type

    if sensor.value_1 != None:
        sensors[sensor_id].value_1 = sensor.value_1

    if sensor.value_2 != None:
        sensors[sensor_id].value_2 = sensor.value_2

    return sensors[sensor_id]

@app.delete("/delete/{sensor_id}")
def delete_data(sensor_id: int):
    if sensor_id not in sensors:
        return {"Error": "Given input in not present in the Database"}

    del sensors[sensor_id]
    return {"Message": "Your data is successfully deleted from the records"}

@app.post("/post-data/{sensor_id}")
def publish_msg(sensor_id: int, sensor: Sensor):
    from google.cloud import pubsub_v1
    if sensor_id in sensors:
        return{"Error": "Already Present in the Database"}

    sensors[sensor_id] = sensor
    # TODO(developer)
    project_id = "searce-playground"
    topic_id = "trail_pubsubtopic"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    data = f"{sensors}"
    data = data.encode("utf-8")
    future = publisher.publish(
            topic_path, data, origin="test trail", username="Abhishek-local"
        )
    '''for n in range(1, 10):
        data = f"Message number {n}"
        # Data must be a bytestring
        data = data.encode("utf-8")
        # Add two attributes, origin and username, to the message
        future = publisher.publish(
            topic_path, data, origin="test trail", username="Abhishek-local"
        )'''
    return {"Output": future.result()}