"""
Setup script for the Music Theory Engine package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="music-theory-engine",
    version="1.0.0",
    author="AI Music Engineer",
    author_email="music.engine@example.com",
    description="A comprehensive music theory analysis engine for guitarists and musicians",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/music-theory-engine",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Topic :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": ["pytest>=6.0", "black", "flake8"],
        "build": ["pyinstaller>=6.0.0"],
    },
    entry_points={
        "console_scripts": [
            "music-theory-gui=music_engine.main_gui:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
