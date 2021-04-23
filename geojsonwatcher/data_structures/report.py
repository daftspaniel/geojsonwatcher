"""
    Report object.
"""


class Report:
    def __init__(self, name: str, metadata: dict, entries: list = []):
        self.name = name
        self.metadata = metadata
        self.entries = entries
        self.updates = 1
        self.metadata['generated'] = 1556911050000

    def sort_entries(self):
        self.entries = sorted(self.entries,
                              key=lambda feature: feature.mag, reverse=True)

    def append(self, report):
        self.updates += 1
        self.metadata['generated'] = 1556911050000
        self.entries.extend(report.entries)
        visited = set()
        self.entries = [e for e in self.entries
                        if e.url not in visited
                        and not visited.add(e.url)]
        self.sort_entries()
