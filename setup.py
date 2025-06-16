from setuptools import setup, find_packages

setup(
    name="snap-prioritize",
    version="0.1.0",
    description="SNAP: SNP Prioritization Tool",
    author="Nadeem Khan, Muhammad Muneeb Nasir",
    author_email="muneebgojra@gmail.com",
    url="https://github.com/muneebdev7/SNAP",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
        "requests>=2.22.0",
        "ete3>=3.1.1",
        "openpyxl>=3.1.5",
    ],
    entry_points={
        'console_scripts': [
            'snap=snap.cli:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bioinformatics",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
)