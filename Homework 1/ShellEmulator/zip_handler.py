import zipfile, os, tempfile

# Peace of terrible code from cyberforum translated from python 2
# But it works and I don't want to touch it ever again
def extract_zip(path):
    with zipfile.ZipFile(path, "r") as zip_f:
        temp_dir = tempfile.mkdtemp()
        for name in zip_f.namelist():
            try:
                unicode_name = name.encode("utf-8").decode("utf-8")
            except UnicodeDecodeError:
                print(f"Error decoding file name: {name}")
                continue

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
