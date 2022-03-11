import paho.mqtt.client as mqtt
import json as jasoane
import influxdb as tsdb
import os as systemUtils
import datetime as timeMachine
import logging as loger


# def on_connect(client, userdata, flags, rc):
#     print("Connected with result code "+str(rc))


def on_message(client, userdata, msg):

    counter = 0
    slash_counter = 0
    locatie = ""
    statie = ""
    # Verificarea corectitudinii formatului topicului si separarea locatiei de statie
    for c in msg.topic:
        print(f'Caracterul curent este {c} \n')
        if c == '/':
            if counter == 0:
                return
            slash_counter = slash_counter + 1
            counter = 0
        else:
            counter = + 1
            if slash_counter == 0:
                locatie = locatie + c
            if slash_counter == 1:
                statie = statie + c
    if slash_counter != 1:
        return

    loger.info(f"Received a message by topic [{locatie}/{statie}]")

    listing = jasoane.loads(msg.payload)
    ts = ""

    if 'timestamp' in listing:
        ts = timeMachine.datetime.strptime(
            listing['timestamp'], '%-d %B %Y, %H:%M:%S %p')
        ts = ts.strftime('%Y-%m-%dT%H:%M:%S%z')
        loger.info(f"Data timestamp i s : {listing['timestamp']}")
    else:
        ts = timeMachine.datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
        loger.info("Data timestamp is NOW")

    loger.info(f"{ts}")

    to_insert_rows = []
    # Crearea unei inregistrari pentru fiecare camp din mesajul curent
    for key in listing.keys():
        if type(listing[key]) != float and type(listing[key]) != int:
            continue
        to_insert_rows.append({
            'measurement': f'{statie}.{key}',
            'tags': {
                'location': locatie,
                'station': statie
            },
            'time': ts,
            'fields': {
                'value': float(listing[key])
            }
        })

        loger.info(f"{locatie}.{statie}.{key} {listing[key]}")

    if len(to_insert_rows) > 0:
        userdata.write_points(to_insert_rows)


influxdb_client = tsdb.InfluxDBClient(host="tema3stack_tsdb")

try:
    influxdb_client.switch_database("collector")
except:
    influxdb_client.create_database('collector')
    influxdb_client.switch_database("collector")

logger_on = systemUtils.getenv("DEBUG_DATA_FLOW")

if(logger_on == 'da'):
    loger.basicConfig(
        level=loger.INFO,
        format='%(asctime)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
else:
    loger.basicConfig(
        level=loger.ERROR,
        format='%(asctime)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

broker_client = mqtt.Client(userdata=influxdb_client)

broker_client.on_message = on_message

broker_client.connect("tema3stack_mosquitto")

broker_client.subscribe('#')

broker_client.loop_forever()
