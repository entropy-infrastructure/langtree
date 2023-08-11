
def get_embedding_content(output):
    """Process the output to return a list of embeddings.

    Each embedding is a list of float values.

    Args:
        output (list of lists): The output containing potential embeddings.

    Returns:
        list of lists: Processed embeddings as lists of float values.
    """
    return [[float(val) for val in emb] for emb in output]
