from celery import Celery
from pathlib import Path
import subprocess
import requests
import time
import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

rabbit_path = 'amqp://user:pass@broker:5672/vhost'
backend = 'db+postgresql://postgres:backend@backend/backend_db'

app = Celery('simulator_tasks', broker=rabbit_path, backend=backend)

queue_name = subprocess.check_output("cat /etc/hostname", shell=True)

app.conf.task_routes = {'simulator_tasks.*': {'queue': queue_name}}


def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


@app.task
def set_model(model_params):
    model_name = model_params['model_name']
    step_size = model_params['step_size']
    final_time = model_params['final_time']
    fmu_path = '/home/deb/code/fmu_location/' + model_name + '/' + model_name + '.fmu'
    auth_token = model_params['Authorization']
    logger.info(f'PATH TO FMU IN SET_MODEL: {fmu_path}')
    time.sleep(5)

    # TODO if file not in /home/deb/code post new model here with modified model_name.append(hostname)
    swarm_check = Path('/home/deb/code/isSwarm.txt')
    if not swarm_check.exists():
        init_url = 'http://0.0.0.0:8000/init_model/'
        hostname = subprocess.check_output("cat /etc/hostname", shell=True)
        model_name = model_name + '_' + str(hostname)

        init_data = {
            'model_name': model_name,  # change name each time script is run!
            'step_size': step_size,  # step size in seconds. 600 secs = 10 mins
            'final_time': final_time,  # 24 hours = 86400 secs
            'container_id': hostname
        }
        header = {'Authorization': auth_token}
        requests.post(init_url, headers=header, data=init_data)

    params = {'model_name': model_name,
              'step_size': step_size,
              'final_time': final_time,
              'fmu_path': fmu_path,
              'Authorization': auth_token}

    with open('./store_incoming_json/model_params.json') as json_file:
        data = json.load(json_file)
        logger.info(f'DATA JSON LOAD IN SET MODEL TASK {data}')

        data['model_params'].append(params)

        logger.info(f'DATA PARAMS IN SET MODEL TASK AFTER APPEND {data}')

    write_json(data, './store_incoming_json/model_params.json')


@app.task  # (ignore_result=True)
def post_output(output_json, header):  # TODO refactor to send output data to api db
    logger.info(f'post_output -> output_json {output_json}')
    output_url = 'http://web:8000/output/'
    logger.info(f'post_output -> output_json {type(output_json)}')

    header['Content-Type'] = 'application/json'
    logger.info(f'post_output -> output_json header {header}')
    logger.info(f'post_output -> output_json header type {type(header)}')

    r = requests.post(output_url, headers=header, data=output_json)
    logger.info(f'post_output -> request status {r.status_code}')
    logger.info(f'post_output -> request text {r.text}')
    return r.text
