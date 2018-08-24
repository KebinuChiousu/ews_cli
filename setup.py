from setuptools import setup

setup(name='ews-cli',
      version='0.1.0.8',
      description='Filter email via EWS endpoint',
      url='https://github.com/KebinuChiousu/ews_cli',
      download_url='https://github.com/KebinuChiousu/ews_cli/archive/v0.1.0.8.tar.gz',
      author='Kevin Meredith',
      author_email='kevin@meredithkm.info',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
          'Topic :: Communications :: Email',
      ],
      keywords='owa ews filter',
      packages=['ews_cli'],
      install_requires=[
          'exchangelib==1.11.4',
          'keyring==13.0.0',
          'SecretStorage==3.0.1',
          'PyYAML>=3.12'
      ],
      entry_points={
          'console_scripts': [
          'owa-filter=ews_cli.cli:main',
          'ews-filter=ews_cli.cli:main',
          'ews-cli=ews_cli.cli:main'
        ],
      },
      include_package_data=True,
      zip_safe=False)
