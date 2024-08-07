from setuptools import setup
import os


def get_version(path):
    fn = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        path, "__init__.py")
    with open(fn) as f:
        for line in f:
            if '__version__' in line:
                parts = line.split("=")
                return parts[1].split("'")[1]


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGELOG = open(os.path.join(here, 'CHANGELOG.rst')).read()


setup(
    name="devpi-findlinks",
    description="devpi-findlinks: find-links view for devpi-server",
    long_description=README + "\n\n" + CHANGELOG,
    url="https://github.com/devpi/devpi-findlinks",
    version=get_version("devpi_findlinks"),
    maintainer="Florian Schulze",
    maintainer_email="florian.schulze@gmx.net",
    license="MIT",
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python"] + [
            "Programming Language :: Python :: %s" % x
            for x in "3 3.8 3.9 3.10 3.11 3.12".split()],
    entry_points={
        'devpi_server': [
            "devpi-findlinks = devpi_findlinks.main"]},
    install_requires=[
        'devpi-server>=5.2.0'],
    include_package_data=True,
    python_requires='>=3.8',
    zip_safe=False,
    packages=['devpi_findlinks'])
