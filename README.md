# zip-extract-rename-util

> This project **has all the features it should have**, PRs/issues for bug fixes etc. are welcome, but **feature requests are not**, thank you for understanding.

If you are tired of extracting & renaming files from `.zip`, try this.

Let's say you have `example.zip`, and the archive structure below:

```
example.zip/directory/example1/file.txt
example.zip/directory/example2/file.txt
example.zip/directory/example3/file.txt
example.zip/directory/example4/file.txt
...
example.zip/directory/example100/file.txt
example.zip/another_directory/...
example.zip/note.txt
example.zip/checksums
```

with this piece of code

```py
import os
import zipfile
from pathlib import Path

from zip_extract_rename_util.extract import Extract

output_path = Path(os.getcwd()) / "extract_files"
output_path.mkdir(parents=True, exist_ok=True)
zipfile_obj = zipfile.ZipFile("/path/to/example.zip")

with zipfile_obj:
    target_path = zipfile.Path(zipfile_obj) / "directory"
    extract = Extract(zipfile_obj, target_path, "file.txt", output_path)
    extract.extract()
```

you will get

```
/example.zip
/extract_files/example1.txt
/extract_files/example2.txt
/extract_files/example3.txt
/extract_files/example4.txt
...
/extract_files/example100.txt
```

We also have large file optimize by using `yield` instead of `file_in_zip.read()` & `file_output.write(...)`, to reduce memory consumption. See [extract.py](./zip_extract_rename_util/extract.py) for details.
