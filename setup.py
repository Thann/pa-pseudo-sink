#!/usr/bin/env python
import os
from setuptools import setup, find_packages

description = "Creates a dummy output for PulseAudio so you can isolate sounds from different applications."

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def get_version():
    from subprocess import Popen, PIPE
    try:
        from subprocess import DEVNULL # py3
    except ImportError:
        import os
        DEVNULL = open(os.devnull, 'wb')

    def run(*cmd):
        return (Popen(cmd, stderr=DEVNULL, stdout=PIPE)
                .communicate()[0].decode('utf8').strip())

    return(run('git', 'describe', '--tags').replace('-','.post',1).replace('-','+',1)
        or '0.0.0.post{}+g{}'.format(
            run('git', 'rev-list', '--count', 'HEAD'),
            run('git', 'rev-parse', '--short', 'HEAD')))

setup(
    name = "pa-pseudo-sink",
    version = get_version(),
    author = "Jonathan Knapp",
    author_email = "jaknapp8@gmail.com",
    description = description,
    license = "UNLICENSE",
    keywords = "pulseaudio dummy output",
    url = "http://github.com/thann/pa-pseudo-sink",
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        "Topic :: Multimedia :: Sound/Audio :: Mixers",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
    ],
    packages=[''],
    package_data={'': ['main.ui']},
    include_package_data=True,
    py_modules=["pseudo_sink"],
    install_requires=['wheel', 'PyGObject'],
    entry_points={
        'gui_scripts': [
            'pseudo-sink=pseudo_sink:start',
        ],
    },
    setup_requires=['wheel', 'install_freedesktop>=0.2.0'],
    dependency_links=[
        "https://github.com/thann/install_freedesktop/tarball/master#egg=install_freedesktop-0.2.0"
    ],
    desktop_entries={
        'pseudo-sink': {
            'filename': 'thann.pseudo_sink',
            'Name': 'PseudoSink for PulseAudio',
            'Categories': 'AudioVideo;Audio;Player',
            'Comment': description,
            'Icon': 'audio-volume-high',
        },
    },
)
