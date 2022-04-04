from pathlib import Path

from setuptools import find_packages, setup

with open(Path(__file__).resolve().parent / "README.md") as f:
    readme = f.read()

setup(
    name="extreqs",
    url="https://github.com/clbarnes/extreqs",
    author="Chris L. Barnes",
    description="Parse python requirements.txt files into setuptools extras",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(include=["extreqs"]),
    install_requires=["setuptools"],
    python_requires=">=3.7, <4.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
)
