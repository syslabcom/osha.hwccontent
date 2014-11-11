from setuptools import setup, find_packages

version = '1.0.13'

long_description = (
    open('README.txt').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='osha.hwccontent',
      version=version,
      description="Content types for OSHA Health at Work Campaign",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='gpl',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['osha', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.RedirectionTool',
          'collective.z3cform.datagridfield>=0.15',
          'plone.api',
          'plone.app.contenttypes',
          'plone.app.event',
          'plone.app.multilingual[dexterity]>=1.0',
          'plone.app.referenceablebehavior',
          'plone.multilingual>=1.0',
          'plone.multilingualbehavior>=1.0',
          'plone.namedfile[blobs]',
          'reportlab',
          'slc.xliff',
          'xlrd',
          'xlwt',
      ],
      extras_require={'test': ['plone.app.testing[robot]>=4.2.2',
                               'plone.app.robotframework[reload]']},
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
