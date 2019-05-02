"""
    Report object.
"""

class Report(object):
    def __init__(self, name, metadata, entries):
        self.name = name
        self.metadata = metadata
        self.entries = entries

    def append(self, report):
        self.entries.append(report.entries)
