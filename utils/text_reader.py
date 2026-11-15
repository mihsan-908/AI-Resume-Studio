def read_text(file_path: str) -> str:
    """
    Read a text file.

    Args:
        file_path (str): Path to the text file.

    Returns:
        str: File content.
    """

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()

    except Exception as e:
        raise Exception(f"Error reading text file: {e}")