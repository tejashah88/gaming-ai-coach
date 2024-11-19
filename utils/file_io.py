import os


# Joins all folders together and normalizes the paths
def join_normalized_path(base_dir: str, *paths: str) -> str:
    return os.path.normpath(
        os.path.join(
            base_dir, *paths
        )
    )

# Fetches the file extension from a given path, excluding the dot separator and normalizing to lowercase
def get_file_extension(file_path: str):
    (_, file_ext) = os.path.splitext(file_path)
    # Make sure to exclude the dot separate and convert to lowercase (windows allows .txt and .TXT to be equivalent)
    return file_ext[1:].strip().lower()
