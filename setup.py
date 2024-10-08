#####################################################################################
#
#  Copyright (C) MCode GmbH
#
#  Unless a separate license agreement exists between you and MCode GmbH (e.g. you
#  have purchased a commercial license), the license terms below apply.
#
#  Should you enter into a separate license agreement after having received a copy of
#  this software, then the terms of such license agreement replace the terms below at
#  the time at which such license agreement becomes effective.
#
#  In case a separate license agreement ends, and such agreement ends without being
#  replaced by another separate license agreement, the license terms below apply
#  from the time at which said agreement ends.
#
#  LICENSE TERMS
#
#  This program is free software: you can redistribute it and/or modify it under the
#  terms of the GNU Affero General Public License, version 3, as published by the
#  Free Software Foundation. This program is distributed in the hope that it will be
#  useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#  See the GNU Affero General Public License Version 3 for more details.
#
#  You should have received a copy of the GNU Affero General Public license along
#  with this program. If not, see <http://www.gnu.org/licenses/agpl-3.0.en.html>.
#
#####################################################################################

import os
import setuptools
from setuptools import setup, find_packages
from distutils.version import LooseVersion

if LooseVersion(setuptools.__version__) < LooseVersion("20.5"):
    import sys
    sys.exit("Installation failed: Upgrade setuptools to version 20.5 or later")

base_dir = os.path.dirname(__file__)
about = {}
if base_dir:
    os.chdir(base_dir)
with open(os.path.join(base_dir, "yc_aws_wrapper", "__about__.py")) as f:
    exec(f.read(), about)

with open(os.path.join(base_dir, "README.md")) as f:
    long_description = f.read()


def parse_requirements_file(filename):
    with open(filename) as fid:
        requires = [ln.strip() for ln in fid.readlines() if not ln.startswith("#")]
    return requires


install_requires = parse_requirements_file("requirements.txt")

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__summary__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=about["__license__"],
    url=about["__uri__"],
    project_urls={
        "Bug Tracker": "https://github.com/mcode-cc/python-yandex-cloud-sdk-wrapper/issues",
    },
    author=about["__author__"],
    author_email=about["__email__"],
    platforms=("Any"),
    install_requires=install_requires,
    packages=find_packages(),
    include_package_data=True,
    data_files=[(".", ["LICENSE", "COPYRIGHT"])],
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 1 - Planning",
        "Environment :: No Input/Output (Daemon)",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet",
        "Topic :: Communications",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: System :: Networking"
    ],
    keywords="Wrapper for yandex cloud services"
)
