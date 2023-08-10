import os
import zipfile
from os import getcwd
from pathlib import Path


class Extract:
    def __init__(
        self,
        zipfile_obj: zipfile.ZipFile,
        lookup_path: zipfile.Path,
        target_filename: str,
        output_path: Path = Path(getcwd()) / "zip_extract",
    ):
        self.__zipfile_obj = zipfile_obj

        self.__lookup_path = lookup_path
        self.__target_filename = target_filename
        self.__output_path = output_path

    @property
    def zipfile_obj(self):
        return self.__zipfile_obj

    @zipfile_obj.setter
    def zipfile_obj(self, value: zipfile.ZipFile):
        self.__zipfile_obj = value

    @property
    def lookup_path(self):
        return self.__lookup_path

    @lookup_path.setter
    def lookup_path(self, value: zipfile.Path):
        self.__lookup_path = value

    @property
    def target_filename(self):
        return self.__target_filename

    @target_filename.setter
    def target_filename(self, value: str):
        self.__target_filename = value

    @property
    def target_filename_ext(self):
        return os.path.splitext(self.target_filename)[1]

    @property
    def output_path(self):
        return self.__output_path

    @output_path.setter
    def output_path(self, value: Path):
        self.__output_path = value

    def extract(self):
        subdirs = [p for p in self.lookup_path.iterdir() if p.is_dir()]

        for subdir in subdirs:
            target_file_path = subdir / self.target_filename
            output_file_path = (
                self.output_path / f"{subdir.name}{self.target_filename_ext}"
            )

            if target_file_path.exists():
                with (
                    target_file_path.open("rb") as source_file,
                    open(output_file_path, "wb") as dest_file,
                ):
                    print(target_file_path, "->", output_file_path)
                    while True:
                        chunk = source_file.read(4092)
                        if not chunk:
                            break
                        dest_file.write(chunk)
