from setuptools import find_packages
from setuptools import setup

setup(
    name="dashboard",
    version="1.0.0",
    description="Test",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    setup_requires=["Flask", "flask-cors", "numpy", "pandas"],
    install_requires=["Flask", "flask-cors", "numpy", "pandas", "requests", "urllib3", "matplotlib"],
)
