"""Parsers that parse snapshot raw data.\n
How to add a new message queue Driver?
To add a new parser, named myparser, add a file in this package named parse_myparser.py
In that file implement the following function:

def parse_myparser(raw_data):
    Returns the result in json. The dictionary must have also the keys: 'user_id', 'datetime', myparser.
    
    :param raw_data: The raw_data as consumed from the message queue
    :type raw_data: json
    :return: json dumps of a dictionary with the keys: 'user_id', 'datetime', myparser
    :rtype: json

And add to that function the fields that the parser uses:
parse_myparser.fields = {field1, field2}
"""
import os
import pathlib
import sys
from sphere.utils import load_parsers

root = pathlib.Path(os.path.dirname(__file__))
parsers = load_parsers(root)

fields = {'datetime'}
for parser in parsers.values():
    fields = fields.union(parser.fields)
fields = list(fields)

def run_parser(parser_name, data):
    return parsers[parser_name](data)