import os

def read_queries_file():
    """
    Reads the queries.txt file and returns its content as text.
    """
    file_path = os.path.join(os.path.dirname(__file__), "../files/queries.txt")
    with open(file_path, 'r') as file:
        content = file.read()
    return content