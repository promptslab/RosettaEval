import typing as typ
from functools import wraps
from pathlib import Path

T = typ.TypeVar("T")


def load_from_file(file_extension: str) -> typ.Callable:
    """Load a file from a path."""

    def decorator(func: typ.Callable) -> typ.Callable:
        @wraps(func)
        def wrapper(cls: type[T], path: str) -> typ.Callable:
            path_to_file = Path(path)
            if not path_to_file.exists():
                msg = f"Could not find file: {path_to_file}"
                raise FileNotFoundError(msg)
            if path_to_file.suffix != file_extension:
                msg = f"File must be a {file_extension} file: {path_to_file}"
                raise ValueError(msg)
            with path_to_file.open() as f:
                return func(cls, f)

        return wrapper

    return decorator
