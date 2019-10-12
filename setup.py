import setuptools

requires = [
    'requests>=2.22.0,<2.20.0',
    'boto3>=1.9.243,<1.9.1',
    'google-cloud-storage>=1.20.0,<1.19.0'
    'azure-storage-blob>=2.1.0,<2.0.0'
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-ffmpeg-video-streaming",
    version="0.0.13",
    author="Amin Yazdanpanah",
    author_email="contact@aminyazdanpanah.com",
    description="Package media content for online streaming(DASH and HLS) using ffmpeg",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)