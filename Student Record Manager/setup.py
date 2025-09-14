#!/usr/bin/env python3
"""
Setup script for Student Record Manager
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
    name="student-record-manager",
    version="1.0.0",
    author="Sunil Sharma",
    author_email="sunil.sharma@example.com",
    description="A comprehensive Python-based CRUD system for managing student records",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/sunbyte16/student-record-manager",
    project_urls={
        "Bug Reports": "https://github.com/sunbyte16/student-record-manager/issues",
        "Source": "https://github.com/sunbyte16/student-record-manager",
        "Documentation": "https://github.com/sunbyte16/student-record-manager#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Education",
        "Topic :: Database",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "student-manager=student_manager:main",
            "student-manager-simple=simple_student_manager:main",
            "student-manager-demo=quick_demo:quick_demo",
            "student-manager-data=demo_data:main",
        ],
    },
    keywords="student, records, crud, management, education, csv, json, database",
    include_package_data=True,
    zip_safe=False,
)
