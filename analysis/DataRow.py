"""
Define an object that represents a row in a results CSV.
"""

class DataRow:
    def __init__(self, raw_row: str):
        """
        Parse a CSV row into the appropriate python type data for each datatype.
        """
        raw_row = raw_row.strip()
        accession, length, kingdom, accurate_prediction, time_ms, miss_type, hit_type = raw_row.split(',')
        self.accession = accession
        self.seq_length = int(length)
        self.kingdom = kingdom
        self.accurate = True if accurate_prediction == 'True' else False
        self.time_ms = float(time_ms)

        # Parse text into None object.
        if miss_type == 'None':
            self.miss_type = None
        else:
            self.miss_type = miss_type

        if hit_type == 'None':
            self.hit_type = None
        else:
            self.hit_type = hit_type
