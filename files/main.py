__winc_id__ = "ae539110d03e49ea8738fd413ac44ba8"
__human_name__ = "files"


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
        # using shutill as it can remove a directory which contains files/folders
        shutil.rmtree(CACHE_PATH)
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
        (file_path) for file_path in CACHE_PATH.iterdir() if file_path.is_file()
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


# Tried to create cache and zipfile paths,
# which were relative to files/main.py (script) location.
# instead dof being relative to the 'current directory'.
# The 'current directory' can change depending on where invoking python and wincpy from,
# while data.zip and 'cache' folder need to be in same folder as files/main.py (the files folder)

# The below will create the cache folder en read data.zip no matter from where you run your script
# but unfortunatly Wincpy runs into errors when it's checks this code

# SCRIPT_DIRECTORY = pathlib.Path(__file__).parent.absolute()
# CACHE_PATH = SCRIPT_DIRECTORY / "cache"
# ZIP_PATH = SCRIPT_DIRECTORY / "data.zip"
