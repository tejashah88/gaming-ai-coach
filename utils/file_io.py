import os


# Joins all folders together and normalizes the paths
def join_normalized_path(base_dir: str, *paths: str) -> str:
    return os.path.normpath(
        os.path.join(
            base_dir, *paths
        )
    )
