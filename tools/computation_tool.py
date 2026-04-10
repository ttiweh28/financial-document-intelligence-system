from agents.tool import CodeInterpreterTool

computation_tool  = CodeInterpreterTool(
    tool_config={
        "timeout": 30
    }
)

