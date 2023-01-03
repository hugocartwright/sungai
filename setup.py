"""PyPi package setup instructions."""

from setuptools import find_packages, setup

setup_args = dict(
    name='sungai',
    python_requires='>3.10.0',
    version="0.0.1",
    description='Sungai is a directory rating tool',
    license='MIT License',
    packages=find_packages(),
    author='Hugo Cartwright',
    author_email='hugo.cartw@gmail.com',
    keywords=['Python'],
    url='https://github.com/hugocartwright/sungai',
    download_url='https://pypi.org/project/sungai/',
    long_description="""
        Sungai is a tool for rating directories.
        Sungai is a tool for rating directories.
        Sungai is a tool for rating directories.
        Sungai is a tool for rating directories.
    """,
    long_description_content_type='text/markdown',
    project_urls={
        'Source': 'https://github.com/hugocartwright/sungai',
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'console_scripts': [
            'sungai = sungai:run_sungai',
        ]
    }
)

if __name__ == '__main__':
    setup(**setup_args)
