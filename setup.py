from setuptools import setup, find_packages

setup(
    name = "ducksoak",
    version = "0.0.1",
    author = "Adam Cathersides",
    author_email = "adamcathersides@gmail.com",
    description = ("Launch a bunch of tsduck instances to perform a tests on multiple streams"),
    packages = ['ducksoak'],
    include_package_data = True,
    install_requires = [
        'click',
        'pyyaml',
        'docker'
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
    entry_points={
          'console_scripts': [
              'ducksoak = ducksoak.ducksoak:run'
          ]
      }
)
