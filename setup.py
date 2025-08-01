from setuptools import setup, find_packages

setup(
    name="fountaincurve",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "matplotlib",
        "yfinance",
        "seaborn"
    ],
    entry_points={
        "console_scripts": [
            "fountaincurve=scripts.vix_suppression_plot:main"
        ]
    }
)
