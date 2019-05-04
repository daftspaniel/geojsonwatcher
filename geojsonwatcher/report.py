"""
    Report object.
"""

class Report(object):
    def __init__(self, name : str, metadata : dict, entries : list = []):
        self.name = name
        self.metadata = metadata
        self.entries = entries

    def append(self, report):
        self.metadata['generated']  = 1556911050000
        self.entries.extend(report.entries)
        
