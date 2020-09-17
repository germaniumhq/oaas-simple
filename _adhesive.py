import germanium_py_exe  # type: ignore


germanium_py_exe.pipeline(
    {
        "repo": "git@github.com:bmustiata/oaas_simple.git",
        "binaries": {
            "name": "Python 3.7 on Linux x64",
            "platform": "python:3.7",
            "publish_pypi": "sdist",
        },
    }
)
