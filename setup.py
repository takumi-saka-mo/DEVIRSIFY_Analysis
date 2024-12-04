import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DiversifyApproach_package",
    version="1.0.0",
    author="Takumi Sakamoto",
    author_email="takumi.saka.mo0107@gmail.com",
    license="MIT",
    description="A package to calculate EXVAL values using finance data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/takumi-saka-mo/DEVIRSIFY_Analysis",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},  # 僕はここにいるよ
    python_requires=">=3.7",
    install_requires=[
        "pandas",
        "yfinance",
    ],
)