"""Create system prompts."""


def prompts(v: int = 1) -> str:
    """Create system prompts.

    Args:
        v: Version of the prompt.

    Returns:
        A string of the prompt.
    """
    if v == 1:
        prompt = """
        You are a critical and creative scientist with deep domain knowledge.
        As a scientist, you are very good at distilling complex information.
        """
    return prompt
