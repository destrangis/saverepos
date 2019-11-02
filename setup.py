from setuptools import setup

import saverepos

setup(
    name="saverepos",
    version=saverepos.VERSION,
    py_modules=["saverepos"],
    entry_points = {
        'console_scripts': ['saverepos=saverepos:main'],
    },
    author="Javier Llopis",
    author_email="javier@llopis.me",
    url="https://github.com/destrangis/saverepos",
    description=saverepos.__doc__,
    install_requires = [
        "requests>=2.18.4",
        "beautifulsoup4>=4.8.1",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: System :: Archiving :: Mirroring",
        "Topic :: Utilities",
        ]
    )
