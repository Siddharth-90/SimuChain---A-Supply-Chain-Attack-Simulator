from setuptools import setup, find_packages
import sys

print("** Simulated malicious payload executed during install (demo only) **")

setup(
    name="malpkg-demo",
    version="0.0.1",
    description="Safe demo package to illustrate install-time hooks",
    packages=find_packages(),
    install_requires=[],
)
