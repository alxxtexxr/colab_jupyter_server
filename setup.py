from setuptools import setup, find_packages

setup(
    name = 'colab_jupyter_server',
    version = '0.8.1', # Versioning follows the pattern MAJOR.MINOR.PATCH
    author = 'alxxtexxr',
    author_email = 'alimtegar404@gmail.com',
    description='Colab/Kaggle as Jupyter a server and kernel',
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/alxxtexxr/colab_jupyter_server',
    packages = find_packages(), # Automatically find and include the package
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    entry_points = {
        'console_scripts': [
            'colab_jupyter_server=colab_jupyter_server.core:main'
        ],
    },
    install_requires = [
        # 'jupyter',
        'fire',
        'patool',
        'requests',
        'jupyter-server>=2.14',
    ],
)