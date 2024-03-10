from setuptools import setup

setup(
    name='greeter',
    version='0.1',
    packages=['cli'],
    maintainer='Simon Nganga',
    maintainer_email='simongash@gmail.com',
    description='My first click package',
    author='Simon Nganga',
    author_email='simongash@gmail.com',
    keywords=['greeter', 'click-greeter'],
    requires=['click'],
    password='MyPassword',
    entry_points='''
    [console_scripts]
    greeter=cli:greet_cli
    '''
)
