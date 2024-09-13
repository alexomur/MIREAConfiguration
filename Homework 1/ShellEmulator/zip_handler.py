import zipfile, os, tempfile
from Configs import Config
from __main__ import config

# Peace of terrible code from cyberforum translated from python 2
# But it works and I don't want to touch it ever again
def extract_zip():
    with zipfile.ZipFile(config["path_to_zip"], "r") as zip_f:
        temp_dir = tempfile.mkdtemp()
        for name in zip_f.namelist():
            unicode_name = name.encode("cp437").decode("cp866")
            fullpath = os.path.join(temp_dir, unicode_name)
            if name.endswith('/'):
                os.makedirs(fullpath, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(fullpath), exist_ok=True)
                with zip_f.open(name, "r") as f:
                    content = f.read()
                    with open(fullpath, "wb") as output_file:
                        output_file.write(content)
    return temp_dir