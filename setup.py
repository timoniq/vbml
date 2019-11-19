import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="vbml",
    version="0.3",
    author="timoniq",
    description="Way to check",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/timoniq/vbml",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    install_requires=["poetry"],
)
