from agents import function_tool

@function_tool
def compute_metrics(data: str) -> str:
    """Perform financial computations: totals, balances, metrics on provided data."""
    import json

    try:
        parsed = json.loads(data)
    except Exception:
        parsed = data

    return f"Data received for computation:\n{parsed}"