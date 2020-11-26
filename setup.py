import setuptools
import cooldown

with open("README.md", "r") as fh:
    long_description = fh.read()

# python setup.py bdist_wheel --universal (BUILD)
# python -m twine upload dist/* (UPDATE)

setuptools.setup(
    name="cooldown", 
    version=cooldown.__version__,
    author="Lukas Canter, Leo Rooney",
    author_email="lilcanter07@gmail.com, bigpuppy99991@gmail.com",
    description="Cooldowns that dont reset on bot off time.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bigpuppy9999/dpycooldowns",
    packages=setuptools.find_packages("pymongo"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
