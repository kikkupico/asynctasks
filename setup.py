from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='asynctasks',
      version='0.1.4',
      description='Asynchronous task scheduler and runner for Python',
      long_description=readme(),
      classifiers=[
        'Programming Language :: Python :: 3.5',
        'Framework :: AsyncIO'
      ],
      keywords='asyncio plan task scheduler async concurrent',
      url='https://github.com/vramakin/asynctasks',
      author='Ram',
      author_email='vramak@gmail.com',
      license='MIT',
      packages=['asynctasks'],
      zip_safe=True)
