from autogen_core.tools import FunctionTool

from utils.xsoar import *

tool_get_xsoar_incident_by_sentinel_incident_number = FunctionTool(
    name="get_xsoar_incident_by_sentinel_incident_number",
    description="Retrieve an Cortex XSOAR incident with a Microsoft Sentinel incident number.",
    func=get_xsoar_incident,
)