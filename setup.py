import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    description = f.read()

setuptools.setup(
    name="tourpy",
    version="0.0.1",
    author="William Nguyen",
    author_email="william.360@hotmail.com",
    description=description,
    package_dir={"": "src"},
    pacakges=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
