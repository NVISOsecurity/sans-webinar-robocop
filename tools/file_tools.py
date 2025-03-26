from autogen_core.tools import FunctionTool

from utils.file import *

tool_get_kql_query_examples = FunctionTool(
    name="get_kql_query_examples",
    description="Retrieve the KQL query examples from the queries.txt file.",
    func=read_queries_file,
)