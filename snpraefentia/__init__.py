"""SNPraefentia: SNP Prioritization Tool"""

__version__ = "1.1.0"

# Strict dependency list: all are required for full functionality
REQUIRED_LIBRARIES = [
    "pandas",
    "numpy",
    "requests",
    "ete3",
    "openpyxl",
    "matplotlib",
    "seaborn",
    "adjustText",
]

def check_dependencies(raise_on_missing: bool = False):
    """
    Check for required dependencies.

    Args:
        raise_on_missing (bool): If True, raises ImportError if any required libraries are missing.
    Returns:
        dict: {'missing': [...]} list of missing packages.
    """
    missing = [lib for lib in REQUIRED_LIBRARIES if not _is_importable(lib)]
    if raise_on_missing and missing:
        raise ImportError(f"Required packages missing: {', '.join(missing)}")
    return {"missing": missing}

def _is_importable(lib: str) -> bool:
    try:
        __import__(lib)
        return True
    except ImportError:
        return False