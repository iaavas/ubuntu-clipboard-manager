from setuptools import setup, find_packages

setup(
    name="ubuntu-clipboard-manager",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "PyGObject>=3.42.1",
    ],
    entry_points={
        "console_scripts": [
            "ubuntu-clipboard-manager=ubuntu_clipboard_manager.main:main",
        ],
    },
)
