#!/usr/bin/env python3
"""
Setup script for Text Helper IA

Author: Alexandre Riuti Wada
Email: alexandre.rwada@gmail.com
GitHub: https://github.com/alexandrewada/text-helper-ia
License: MIT
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="text-helper-ia",
    version="1.0.0",
    author="Alexandre Riuti Wada",
    author_email="alexandre.rwada@gmail.com",
    description="Aplicação desktop para processamento de texto com inteligência artificial",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/alexandrewada/text-helper-ia",
    project_urls={
        "Bug Reports": "https://github.com/alexandrewada/text-helper-ia/issues",
        "Source": "https://github.com/alexandrewada/text-helper-ia",
        "Documentation": "https://github.com/alexandrewada/text-helper-ia#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Text Processing",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    scripts=["text_helper_ia_wrapper.py"],
    include_package_data=True,
    zip_safe=False,
    keywords="text processing, ai, openai, gpt, desktop application, gui, tkinter",
    license_files=["LICENSE"],
)