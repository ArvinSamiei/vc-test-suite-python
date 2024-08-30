import datetime
import itertools
import json
import os
import random

from utils import VERIFIABLE_CREDENTIAL, required_attributes, VERIFIABLE_PRESENTATION, BIT_STRING_STATUS_URL, \
    get_json_schema, VC_SCHEMA_2


class ValidVCGenerator:
    def __init__(self):
        self.ignored_attrs = ['@protected', '@id', '@type']
        self.level = 0

    def generate_id_string(self):
        return 'http://1edtech.edu/credentials/3732'

    def generate_type_string(self):
        return 'random-string'

    def generate_basic_type(self, attr_schema):
        def generate_value(attr_type):
            if attr_type == '@id':
                return [self.generate_id_string(), {'id': self.generate_id_string()}]
            elif attr_type == 'http://www.w3.org/2001/XMLSchema#dateTime':
                return [datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')]

        if isinstance(attr_schema, str):
            return generate_value(attr_schema)
        return generate_value(attr_schema['@type'])

    def generate_attribute(self, parent_attr_name, attr_name, attr_schema):
        req_attributes_map = {}
        arbitrary_atts_map = {}
        logger = GeneratorLogger(attr_name, self.level)
        logger.log_generation_start()
        level_increased = False
        if '@context' in attr_schema:
            if attr_name in required_attributes:
                req_atts = required_attributes[attr_name]
                self.level += 1
                level_increased = True
                for ra in req_atts:
                    req_attributes_map[ra] = self.generate_attribute(attr_name, ra, attr_schema['@context'][ra])

            for key, value in attr_schema['@context'].items():
                if key in self.ignored_attrs:
                    continue
                if attr_name in required_attributes:
                    if key in required_attributes[attr_name]:
                        continue
                if not level_increased:
                    level_increased = True
                    self.level += 1
                arbitrary_atts_map[key] = self.generate_attribute(attr_name, key, attr_schema['@context'][key])
        else:
            if attr_name == 'credentialStatus':
                value = [{'type': BIT_STRING_STATUS_URL}]
                logger.log_value_generation(value)
                return value
            if attr_name in required_attributes:
                req_atts = required_attributes[attr_name]
                if len(req_atts) == 1 and req_atts[0] == 'id':
                    value = [self.generate_id_string()]
                    logger.log_value_generation(value)
                    return value
                for ra in req_atts:
                    if ra == 'id':
                        req_attributes_map[ra] = self.generate_id_string()
                    else:
                        req_attributes_map[ra] = self.generate_type_string()
                    logger.log_child_value_generation(ra, req_attributes_map[ra])
                # for now, we consider if an attr without context has req attributes, it doesnt have arbitrary attributes
                value = [req_attributes_map]
                logger.log_value_generation(value)
                return value
            value = self.generate_basic_type(attr_schema)
            logger.log_value_generation(value)
            return value
        results = []
        required_combinations = list(itertools.product(*req_attributes_map.values()))
        arbitrary_attrs_choices = {}
        for key, values in arbitrary_atts_map.items():
            # arbitrary types are not supported yet
            if values is None:
                arbitrary_attrs_choices[key] = ['unknown']
                continue
            new_values = [v for v in values]
            # An arbitrary value may not be in the VC.
            new_values.append(None)
            arbitrary_attrs_choices[key] = new_values
        arb_combinations = list(itertools.product(*arbitrary_attrs_choices.values()))
        combined_keys_unique = list(req_attributes_map.keys()) + list(arbitrary_atts_map.keys())

        total_combinations = list(itertools.product(required_combinations, arb_combinations))
        flattened_combinations = [list(itertools.chain(*combination)) for combination in total_combinations]

        for c in flattened_combinations:
            results.append({})
            if attr_name == VERIFIABLE_CREDENTIAL or attr_name == VERIFIABLE_PRESENTATION:
                results[-1]['@context'] = [VC_SCHEMA_2]

            for i in range(len(c)):
                if c[i] is None:
                    continue
                results[-1][combined_keys_unique[i]] = c[i]
            if attr_name == VERIFIABLE_CREDENTIAL:
                results[-1]['type'] = VERIFIABLE_CREDENTIAL
            else:
                results[-1]['type'] = VERIFIABLE_PRESENTATION

        return results


class GeneratorLogger:
    def __init__(self, attr_name, level):
        self.level = level
        self.attr_name = attr_name

    def log_generation_start(self):
        indentation = ' ' * self.level
        print(f'{indentation}•generating attribute {self.attr_name}')

    def log_value_generation(self, value):
        indentation = ' ' * (self.level + 1)
        print(f'{indentation}◦{value} assigned to {self.attr_name}')

    def log_child_value_generation(self, attr_name, value):
        indentation = ' ' * (self.level + 1)
        print(f'{indentation}•generating attribute {attr_name}')
        print(f'{indentation + " "}◦{value} assigned to {attr_name}')


generator = ValidVCGenerator()

json_ld_schema = get_json_schema(2)

results = generator.generate_attribute("", VERIFIABLE_CREDENTIAL, json_ld_schema['@context'][VERIFIABLE_CREDENTIAL])

random_items = random.sample(results, 50)

folder = './generated_vcs/'

if not os.path.exists(folder):
    os.makedirs(folder)

for i in range(len(random_items)):
    with open(folder + str(i) + '.json', 'w') as file:
        file.write(json.dumps(random_items[i]))
