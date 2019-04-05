import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-ffmpeg-video-streaming",
    version="0.0.1",
    author="Amin Yazdanpanah",
    author_email="contact@aminyazdanpanah.com",
    description="Package media content for online ffmpeg_streaming(DASH and HLS) using ffmpeg",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aminyazdanpanah/python-ffmpeg-video-ffmpeg_streaming",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)