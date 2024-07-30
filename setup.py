from setuptools import find_packages, setup

setup(
    name="segmented_docstring",
    version="0.4.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    project_urls={
        "Documentation": "https://robin-collins.github.io/segmented_docstring/",
        "Source": "https://github.com/robin-collins/segmented_docstring/",
    },
)
