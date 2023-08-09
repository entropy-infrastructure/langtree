import os
import json
from abc import ABC
from langtree.replay_engine.persist import StorageStrategy, StorageStrategySelector


class JSONStore(StorageStrategySelector):

    def get_strategies(self):
        return {
            (True, True): JSONMultiRunIncremental,
            (True, False): JSONMultiRunAbsolute,
            (False, True): JSONSingleRunIncremental,
            (False, False): JSONSingleRunAbsolute
        }


class JSONStorageStrategy(StorageStrategy):
    def __init__(self, filename):
        self.filename = filename

    def write(self, chain):
        # Read existing data
        data = self.preprocess(chain)
        # Write back the data
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)

    def read(self, chain_name=None):
        if not os.path.exists(self.filename):
            return None

        with open(self.filename, 'r') as f:
            data = json.load(f)

        if chain_name is None:
            return data
        else:
            return data.get(chain_name, None)


class JSONSingleRunAbsolute(JSONStorageStrategy):
    def __init__(self, file_path):
        super().__init__(file_path)

    def preprocess(self, chain):
        return {chain.name: chain.records}


class JSONMultiRunAbsolute(JSONStorageStrategy):
    def __init__(self, file_path):
        super().__init__(file_path)

    def preprocess(self, chain):
        multi_run_data = self.read() or {}
        if chain.name not in multi_run_data:
            multi_run_data[chain.name] = []
        multi_run_data[chain.name].append(chain.records)
        return multi_run_data


class JSONSingleRunIncremental(JSONStorageStrategy):
    def __init__(self, file_path):
        super().__init__(file_path)

    def preprocess(self, chain):
        chain_updates = {}
        existing_records = self.read(chain.name) or []
        existing_records.extend(chain.records[len(existing_records):])
        chain_updates[chain.name] = existing_records
        return chain_updates

class JSONMultiRunIncremental(JSONStorageStrategy):
    def __init__(self, file_path):
        super().__init__(file_path)

    def preprocess(self, chain):
        multi_run_data = self.read() or {}
        if chain.name not in multi_run_data:
            multi_run_data[chain.name] = []
        existing_records = multi_run_data[chain.name][-1] if multi_run_data[chain.name] else []
        existing_records.extend(chain.records[len(existing_records):])
        if existing_records:
            multi_run_data[chain.name].append(existing_records)
        return multi_run_data

