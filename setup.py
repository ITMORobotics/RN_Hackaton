import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='rn_hackaton',
    version='0.0.1',
    author='TexnoMann',
    author_email='texnoman@itmo.ru',
    description='Package with RN hackaton solution',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ITMORobotics/RN_Hackaton",
    project_urls={
        "Bug Tracker": "https://github.com/ITMORobotics/RN_Hackaton/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license='MIT',
    download_url = 'https://github.com/ITMORobotics/RN_Hackaton/archive/refs/tags/v0.0.1.tar.gz',
    include_package_data=True,
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    package_data={"": ["README.md", "LICENSE.txt"]},
    install_requires=[
        "numpy",
        "opencv-python",
        "pillow",
        "pysqlite3",
        "pypylon",
        "pyzbar"
   ]
)