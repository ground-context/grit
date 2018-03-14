#!/usr/bin/env python

import csv
import json
import os
import sys

""" The purpose of this class is to provide an abstraction for reading records.
    Under the hood, the records are backed by a CSV file. Our iterator simply
    fetches the next record in the file until we reach the end.
"""
class RecordIterator(object):
    
    """ records_file needs to be the full path to the file containing the records of a specific query result. """
    def __init__(self, records_file):
        f = open(records_file, 'r')
        csvreader = csv.reader(f, delimiter=',')
        self.records_file = f
        self.csvreader = csvreader
        
    def get_next_record(self):
        next_record = self.csvreader.next()
        
        # No more records, we close the file.
        if not next_record:
            self.records_file.close()
            return None
        
        return next_record
        