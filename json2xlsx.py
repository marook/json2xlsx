#!/usr/bin/python2

import json
import openpyxl
import sys

def main(json_path, xlsx_path):
    json_data = read_json(json_path)

    o2r = ObjectToRow()

    for json_object in json_data:
        o2r.build_columns(json_object)

    workbook = openpyxl.Workbook()
    worksheet = workbook.create_sheet(0)

    worksheet.append(o2r.get_header_row())

    for json_object in json_data:
        worksheet.append(o2r.convert(json_object))

    workbook.save(xlsx_path)

def read_json(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)

class ObjectToRow(object):

    def __init__(self):
        # key: json object property name
        # value: column index
        self.property_columns = {}

    def build_columns(self, obj):
        for property_key in obj.iterkeys():
            if(property_key in self.property_columns):
                continue

            self.property_columns[property_key] = len(self.property_columns)

    def get_header_row(self):
        return [property_key for property_key, property_index in sorted(self.property_columns.iteritems(), key=lambda i: i[1])]

    def convert(self, obj):
        row = [None,] * len(self.property_columns)

        for property_key, property_value in obj.iteritems():
            property_index = self.property_columns[property_key]

            row[property_index] = unicode(property_value)

        return row

if __name__ == '__main__':
    args = sys.argv
    
    main(args[1], args[2])
