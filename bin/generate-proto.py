#!/usr/bin/env python3

import os
import subprocess
import logging

from termcolor_util import cyan, yellow

FOLDER = "grpc"
EXTENSION = ".proto"


def main() -> None:
    for f in os.listdir(FOLDER):
        if not f.endswith(EXTENSION):
            continue

        ui_file = os.path.join(FOLDER, f)
        target_file = find_target_file(ui_file)

        if is_newer(ui_file, target_file):
            print(
                cyan("IGNORED", bold=True),
                cyan(target_file, bold=True),
                cyan("is newer than"),
                cyan(ui_file, bold=True),
            )
            continue

        ui_compile(ui_file, target_file)


def find_target_file(ui_file: str) -> str:
    # 3:-3 - remove FOLDER from prefix, and EXTENSION from suffix of the file
    python_file = ui_file[len(FOLDER) + 1:-(len(EXTENSION))] + ".py"
    return os.path.join("oaas_transport_grpc", FOLDER, "generated", python_file)


def is_newer(base: str, expected_newer: str) -> True:
    """
    Checks if the expected_newer file is newer than base.
    """
    if not os.path.isfile(base):
        raise Exception(f"{base} is not a file")

    if not os.path.isfile(expected_newer):
        return False

    base_last_modified = get_last_modified(base)
    expected_last_modified = get_last_modified(expected_newer)

    if base_last_modified < expected_last_modified:
        return True

    return False


def ui_compile(ui_file, target_file) -> None:
    """
    Compiles the UI using pyside2-uic, the python code generator from
    the UI files.
    """
    print(
        yellow("COMPILING"),
        yellow(ui_file, bold=True),
        yellow("->"),
        yellow(target_file, bold=True),
    )

    subprocess.check_call([
        "python", "-m", "grpc_tools.protoc", "-I", FOLDER,
        "--python_out=oaas_transport_grpc/rpc/",
        "--grpc_python_out=oaas_transport_grpc/rpc",
        "--mypy_out=oaas_transport_grpc/rpc grpc/call.proto",
    ])


def get_last_modified(file_name: str) -> int:
    return os.path.getmtime(file_name)


if __name__ == '__main__':
    main()
