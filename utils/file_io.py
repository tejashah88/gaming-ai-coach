import os

# Joins all folders together and normalizes the paths
def join_normalized_path(base_dir, *paths):
    return os.path.normpath(
        os.path.join(
            base_dir, *paths
        )
    )

def ensure_folders(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
