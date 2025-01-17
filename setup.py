import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DiversifyApproach_package",  # パッケージの名前
    version="0.0.2",
    author="Takumi Sakamoto",
    author_email="takumi.saka.mo0107@gmail.com",
    license='MIT',
    description="A package to calculate EXVAL values using finance data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/takumi-saka-mo/DEVIRSIFY_Analysis",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['calculate_EXVAL'],
    python_requires=">=3.7",
    install_requires=[
        "pandas",
        "numpy",
        "yfinance"
    ],
)