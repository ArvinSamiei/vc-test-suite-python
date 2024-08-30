import json
import os
import logging

import validators
from dateutil import parser

from utils import VERIFIABLE_CREDENTIAL, VERIFIABLE_PRESENTATION, VC_SCHEMA_1, VC_SCHEMA_2, DATE_TIME_TYPE1, \
    DATE_TIME_TYPE2, required_attributes, Restriction, special_reqs

logging.basicConfig(level=logging.INFO)

text = input("Enter a)V2.0 or b)V1.1: c)For generated VC's")
if text == "a":
    with open('v2.txt', 'r') as file:
        json_ld_schema = file.read()
    VC_SCHEMA = 'https://www.w3.org/ns/credentials/v2'
    dir = './tests/input/'
    datetime_type='http://www.w3.org/2001/XMLSchema#dateTime'
if text == "b":
    with open('v1.txt', 'r') as file:
        json_ld_schema = file.read()
    VC_SCHEMA = 'https://www.w3.org/2018/credentials/v1'
    datetime_type='xsd:dateTime'
    dir = './dtt-test-api/tests_scripts/input/'
if text == "c":
    with open('v2.txt', 'r') as file:
        json_ld_schema = file.read()
    VC_SCHEMA = VC_SCHEMA_2
    dir = './generated_vcs/'
    datetime_type = DATE_TIME_TYPE2


class Validator:
    def __init__(self, data, schema):
        self.data = data
        self.schema = schema
        self.type = None
        self.result = True

    def get_type(self, data=None):
        data = data or self.data
        if 'type' in data:
            return data['type']
        elif '@type' in data:
            return data['@type']
        return None

    def log_error(self, error):
        logging.error(error)
        self.result = False

    def is_uri_validators(self, uri):
        if not isinstance(uri, str):
            self.log_error(f'Invalid URI: {uri}')
            return False
        is_valid = validators.url(uri) or validators.email(uri) or validators.domain(uri) or uri.startswith("did:")
        if not is_valid:
            self.log_error(f'Invalid URI: {uri}')
        return is_valid

    def check_id_type(self, value):
        if not isinstance(value, (str, dict)):
            return False
        if isinstance(value, str):
            return self.is_uri_validators(value)
        if isinstance(value, dict):
            if 'id' in value:
                return self.is_uri_validators(value['id'])
        return True

    def is_valid_date(self, date_string):
        try:
            # Parse the date string to a datetime object using dateutil.parser
            date_obj = parser.isoparse(date_string)
            return True
        except ValueError:
            self.log_error(f'invalid date: {date_string}')
            return False

    def check_req_attributes(self, key, value, type):
        logging.info(f'Checking required attributes for {key}.')

        result = True
        if key not in required_attributes:
            return True
        if type == '@id' and isinstance(value, str):
            req_attrs = required_attributes[key]
            if len(req_attrs) == 1 and req_attrs[0] == 'id':
                return True
        if not isinstance(value, (list, object)):
            return False
        if isinstance(value, list):
            for val in value:
                if not self.check_req_attributes(key, val, type):
                    result = False
        else:
            for req_att in required_attributes[key]:
                if req_att not in value:
                    self.log_error(f'attribute: {req_att} is required for {key}')
                    result = False
        return result

    def check_restriction(self, restriction, value):
        if restriction == Restriction.MustBeUrl:
            return self.is_uri_validators(value)
        else:
            return True

    def check_restrictions(self, key, value, type):
        result = True
        if key not in special_reqs:
            return True
        if not isinstance(value, (list, object)):
            return False
        if isinstance(value, list):
            for val in value:
                if not self.check_restrictions(key, val, type):
                    return False
        else:
            for res_att in special_reqs[key]:
                restrictions = special_reqs[key][res_att]
                if not isinstance(value, object):
                    return False
                res_val = value[res_att]
                for restriction in restrictions:
                    if not self.check_restriction(restriction, res_val):
                        self.log_error(f'Restriction {str(restriction)} is not satisfied for {key}')
                        result = False
        return result

    def validate_value(self, type, value, schema):
        logging.info(f'validating value of {value} for {type}')

        result = True
        if isinstance(value, dict) and len(value.keys()) == 0 and type != VERIFIABLE_PRESENTATION:
            self.log_error(f'empty value for {type}')
            return False
        if type == '@id':
            return self.check_id_type(value)
        elif type == 'https://www.w3.org/2001/XMLSchema#nonNegativeInteger':
            return isinstance(value, int) and int(value) < 0
        elif type == datetime_type:
            return self.is_valid_date(value)
        elif value == 'unknown':
            return True
        else:
            for key, new_value in value.items():
                if isinstance(new_value, list):
                    for v in new_value:
                        if not self.check_value(key, v, schema, type):
                            result = False
                else:
                    if not self.check_value(key, new_value, schema, type):
                        result = False

        return result

    def check_value(self, key, value, schema, type):
        result = True
        new_schema = schema[type]['@context']
        new_type = self.get_type(new_schema[key])
        req_attr_exist = self.check_req_attributes(key, value, new_type)
        if not req_attr_exist:
            result = False
        restrictions_satisfied = self.check_restrictions(key, value, new_type)
        if not restrictions_satisfied:
            result = False
        new_schema = schema[type]['@context']
        new_type = self.get_type(new_schema[key])
        is_valid = self.validate_value(new_type, value, new_schema)
        if not is_valid:
            self.log_error(f'{value} for {key} is invalid')
            result = False
        return result

    def validate_context(self):
        if '@context' not in self.data:
            self.log_error(f'missing @context')
        if not isinstance(self.data['@context'], list):
            self.log_error(f'@context must be a list')
        keys_list = []
        if self.data['@context'][0] != VC_SCHEMA:
            self.log_error('missing base context')
        for e in self.data['@context']:

            if not isinstance(e, (str, dict)):
                self.log_error(f'{e} is not a valid value for context')
            if isinstance(e, str):
                self.is_uri_validators(e)
            if isinstance(e, dict):
                keys_list += list(e.keys())
                if VERIFIABLE_CREDENTIAL in keys_list or VERIFIABLE_PRESENTATION in keys_list:
                    self.log_error("reserved keywords can't be used in context")
                for key, value in e.items():
                    if isinstance(value, str):
                        self.is_uri_validators(value)
                    elif isinstance(value, dict):
                        if '@type' not in value:
                            self.log_error(f'missing @type at {key}')
        keys_set = set(keys_list)
        if len(keys_set) != len(keys_list):
            self.log_error('context has redundant keys')
        return True

    def validate(self):
        logging.info("validating context")
        is_context_valid = self.validate_context()
        type = self.get_type()
        if type is None:
            return False
        type_lst = []
        if isinstance(type, str):
            type_lst.append(type)
        if isinstance(type, list):
            for item in type:
                type_lst.append(item)
        if VERIFIABLE_CREDENTIAL in type_lst:
            self.type = VERIFIABLE_CREDENTIAL
        elif VERIFIABLE_PRESENTATION in type_lst:
            self.type = VERIFIABLE_PRESENTATION
        else:
            self.log_error(f'type must include {VERIFIABLE_CREDENTIAL} or {VERIFIABLE_PRESENTATION}')
        self.check_req_attributes(self.type, self.data, self.type)
        new_data = {}
        for key, value in self.data.items():
            if key == '@context' or key == 'type' or key == 'id':
                continue
            new_data[key] = value
        return self.validate_value(self.type, new_data, self.schema['@context'])

files = os.listdir(dir)
for f_name in files:
    with open(dir + f_name) as file:
        print(f_name)
        json_ld_data = file.read()

        data_dict = json.loads(json_ld_data)
        schema_dict = json.loads(json_ld_schema)
        validator = Validator(data_dict, schema_dict)

        data_type = validator.get_type()
        try:
            is_data_valid = validator.validate()
            if 'ok' in f_name:
                if not is_data_valid:
                    print(f'wrong result for {f_name}')
            elif 'fail' in f_name:
                if is_data_valid:
                    print(f'wrong result for {f_name}')
            print(validator.result)
            print('-------------------------------------------')
        except Exception as e:
            print(f'validation failed for file {f_name}')
            print(e)
