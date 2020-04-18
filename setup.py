import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
        name = 'crowd-dannygale',
        version = '0.0.1',
        author = 'Danny Gale',
        author_email = 'danny.gale@gale-labs.com',
        description = 'agent based modeling framework',
        long_description = long_description,
        long_description_content_type = 'text/markdown',
        url = 'https://github.com/dannygale/crowd',
        packages = setuptools.find_packages(),
        classifiers = [
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            ],
        python_requires='>=3.7',
)

