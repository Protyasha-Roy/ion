from setuptools import setup, find_packages

setup(
    name="ion",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "google-genai",
        "rich",
        "python-dotenv"
    ],
    entry_points={
        "console_scripts": [
            "ion=ion.main:main",
        ],
    },
    author="Protyasha Roy",
    author_email="protyasharoy369@gmail.com",
    description="An AI-powered shell assistant that executes OS commands based on natural language.",
    license="GPL-3.0+NC",
    url="https://github.com/Protyasha-Roy/ion",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
