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