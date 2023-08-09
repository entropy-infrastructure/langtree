def flatten_records(records):
    """
    Flattens the nested records into a simple list.

    Parameters:
        records (list): The list of nested records.

    Returns:
        list: The flattened list of records.
    """
    flat_list = []
    for run in records:
        for record in run:
            # Add the current record to the flat list
            flat_list.append({
                'function': record['function'],
                'input': record['input'],
                'output': record['output'],
                'errors': record['errors']
            })
            # Recursively add the child records to the flat list
            flat_list.extend(flatten_records(record['children']))
    return flat_list
