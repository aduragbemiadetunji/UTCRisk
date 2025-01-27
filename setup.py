from setuptools import setup, find_packages

setup(
    name="utcrisk",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
        "matplotlib",
        "customtkinter",
    ],
    package_data={"risk_model": ["data/*.json"]},
    description="A risk model package for autonomous ship operations",
    author="Aduragbemi Adetunji",
    author_email="adetunjiaduragbemi1@gmail.com",
    url="https://github.com/aduragbemiadetunji/UTCRisk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)