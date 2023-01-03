#-*-  coding:utf8   -*-
import setuptools

with open("README.md", "r",encoding="utf8") as fh:
    long_description = fh.read( )
long_description="""
## 针对金字塔决策交易软件的常用功能的辅助小工具
"""
setuptools.setup(
    name="jzt",
    version="0.0.3",
    author="wangpeng",
    author_email="andrew361x@hotmail.com",
    description="a library use for weistock",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    package_data={'jzt':["data/*.txt"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)