import os
import zipfile
from os import getcwd
from pathlib import Path, PurePath
from typing import Callable, Optional


class Extract:
    def __init__(
        self,
        zipfile_obj: zipfile.ZipFile,
        lookup_path: zipfile.Path,
        output_path: Path = Path(getcwd()) / "zip_extract",
        *,
        target_filename: Optional[str] = None,
        filter_function: Optional[Callable[[zipfile.Path], bool]] = None,
        rename_function: Optional[Callable[[zipfile.Path, Path], Path]] = None,
    ):
        self.__zipfile_obj = zipfile_obj

        self.__lookup_path = lookup_path
        self.__output_path = output_path

        self.__target_filename = target_filename
        self.__filter_function = filter_function
        self.__rename_function = rename_function

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
    def output_path(self):
        return self.__output_path

    @output_path.setter
    def output_path(self, value: Path):
        self.__output_path = value

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
    def filter_function(self):
        return self.__filter_function

    @filter_function.setter
    def filter_function(self, value: Path):
        self.__filter_function = value

    @property
    def rename_function(self):
        return self.__rename_function

    @rename_function.setter
    def rename_function(self, value: Path):
        self.__rename_function = value

    def extract_zip_file(self, zip_file: zipfile.Path, target_file: Path):
        print(zip_file, "->", target_file)
        with zip_file.open("rb") as zf, target_file.open("wb") as tf:
            while True:
                chunk = zf.read(4096)
                if not chunk:
                    break
                tf.write(chunk)

    def extract(self):
        subdirs = [p for p in self.lookup_path.iterdir() if p.is_dir()]

        for subdir in subdirs:
            if (
                not (self.filter_function and self.rename_function)
                and self.target_filename
            ):
                target_file_path = subdir / self.target_filename
                output_file_path = (
                    self.output_path / f"{subdir.name}{self.target_filename_ext}"
                )

                if target_file_path.exists():
                    self.extract_zip_file(target_file_path, output_file_path)
            elif self.filter_function and self.rename_function:
                files = [p for p in subdir.iterdir() if p.is_file()]
                for file in files:
                    if not self.filter_function(file):
                        continue

                    output_file_path = self.rename_function(
                        PurePath(str(file)), self.output_path
                    )
                    self.extract_zip_file(file, output_file_path)
