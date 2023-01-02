from setuptools import setup, find_packages

setup_args = dict(
    name='sungai',
    version="0.0.1",
    description='Sungai',
    license='MIT',
    packages=find_packages(),
    author='Hugo Cartwright',
    author_email='hugo.cartw@gmail.com',
    keywords=['Python'],
    url='https://github.com/hugocartwright/sungai',
    download_url='https://pypi.org/project/sungai/'
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    project_urls={
        'Source': 'https://github.com/hugocartwright/sungai',
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
    ],
)

if __name__ == '__main__':
    setup(**setup_args)

