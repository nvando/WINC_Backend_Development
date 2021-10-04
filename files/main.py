__winc_id__ = "ae539110d03e49ea8738fd413ac44ba8"
__human_name__ = "files"


from os import path
import pathlib
import shutil
from zipfile import ZipFile

# using pathlib instead of the os module because:
# - it is easier to read,
# - can use '/' instead of os.path.join
# - paths are represented as objects instead of raw strings,
#   which makes code more easily portable across platforms


CURRENT_DIR = pathlib.Path.cwd()
CACHE_PATH = CURRENT_DIR / "cache"


def clean_cache():
    """Creates an empty folder named cache in the current directory.
    If a cache folder already exists,
    it deletes everything in the cache folder.
    """

    if CACHE_PATH.exists():
        shutil.rmtree(
            CACHE_PATH
        )  # using shutill as it can remove a dir which contains files/folders
        print("Deleting existing cache folder.")

    CACHE_PATH.mkdir()
    print("Creating new cache folder.")


def cache_zip(zip_path, cache_path):
    """Unpacks the indicated zip file into a clean cache folder."""

    with ZipFile(zip_path) as z:
        # using with statement for better error handling
        # and it automatically closes file at end of statement
        z.extractall(path=cache_path)
        print("Unpacked zipfiles in cache folder")


def cached_files():
    """Takes no arguments.
    Iterates over all contents in cache folder, and checks if it is a file.
    Returns a list of all the files in the cache, excludes possible folders.
    """
    data_files = [
        file_path for file_path in CACHE_PATH.iterdir() if file_path.is_file()
    ]

    return data_files


def find_password(data_files):
    """Takes the list of file paths from cached_files as an argument.
    Reads the text in each one to check for the presence of a password
    Once found, find_password should return this password string.
    """

    for file_path in data_files:
        content = file_path.read_text()
        if "password" in content:
            part = content.split("password: ")[1]
            password = part.split("\n")[0]
            return password


if __name__ == "__main__":
    clean_cache()
    cache_zip("data.zip", CACHE_PATH)
    data_files = cached_files()
    print(find_password(data_files))


# The Wincpy program doesn't accept above code as a proper solution as
# cached_files() returns a list of path objects instead of strings.
# This can be resoled by converting 'file_path' in line 53 into a string,
# before adding it to the list (str(file_path)).
# Consequently, within the function find_password,
# the file_path string then needs to converted back to a path object (file_path = pathlib.Path(file_path)),
# before opening the file in text mode.
# Wincpy will than accept this code as a solution,
# but the additional converting seems cumbersome and unneccesary.
