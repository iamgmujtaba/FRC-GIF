import csv
import os
from config import parse_opts

# Parse configurations
config = parse_opts()

class UCFDataSet:

    def __init__(self):
        # Get the data.
        self.data = self.load_data()

        # Get the classes.
        self.classes = self.extract_classes()

    @staticmethod
    def load_data():
        """Load data from the specified CSV file."""
        with open(os.path.join(config.dataset_path, 'data_file.csv'), 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
        return data

    def extract_classes(self):
        """Extract classes from the loaded data."""
        classes = []
        for item in self.data:
            if item[1] not in classes:
                classes.append(item[1])

        # Sort classes in alphabetical order.
        classes = sorted(classes)
        
        return classes
