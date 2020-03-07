from setuptools import setup, find_packages

with open('README.rst', encoding='UTF-8') as f:
    readme = f.read()

setup(
    name='pgbackup',
    version='0.1.0',
    description='Database backups locally or to OCI',
    long_description=readme,
    author='Ravi',
    author_email='ravi.v.vittal@oracle.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires = ['oci'],
    entry_points={
        'console_scripts': [
            'pgbackup=pgbackup.cli:main',
        ],
    }
)
