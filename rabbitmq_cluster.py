#!/bin/env python
# -*- coding:utf-8 -*-

import json,requests

parameters_list = []

with open('log.txt', 'r') as log_file:
    for queue in log_file.readlines():
        queue = queue.strip()
        parameters_list.append({'value': {'src-uri': 'amqp://admin:CxxBFtjnSXZ6iLTh@10.30.2.3:55672', 'src-queue': queue,
                                    'dest-uri': 'amqp://admin:CxxBFtjnSXZ6iLTh@localhost:5672', 'dest-queue': queue,
                                    'add-forward-headers': False, 'ack-mode': 'on-confirm', 'delete-after': 'never'},
                          'vhost': '/', 'component': 'shovel', 'name': queue})

policies = '''
{"policies":[{"vhost":"/","name":"Ha-all","pattern":"^q.*","apply-to":"all",
"definition":{"ha-mode":"all","ha-sync-mode":"automatic"},"priority":0}]}
'''
policies_list = json.loads(policies)['policies']

with open('rabbit.json') as old_json_file:
    rabbit_dict = json.loads(old_json_file.read())

rabbit_dict['rabbit_version'] = '3.8.2-management'
rabbit_dict['parameters'] = parameters_list
rabbit_dict['policies'] = policies_list

with open('log.json', 'w') as json_file:
    json_file.write(json.dumps(rabbit_dict))