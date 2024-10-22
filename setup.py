from setuptools import setup, find_packages

setup(
    name = 'colab_jupyter_server',
    version = '0.1',
    packages = find_packages(), # Automatically find and include the package
    entry_points = {
        'console_scripts': [
            'colab_jupyter_server=colab_jupyter_server.core:main'
        ],
    },
)