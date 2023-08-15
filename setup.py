from setuptools import setup

setup(
    name='pl-dcm2niix',
    version='1.0.0',
    description='A ChRIS DS plugin wrapper for dcm2niix',
    author='FNNDSC',
    author_email='dev@babyMRI.org',
    url='https://github.com/FNNDSC/pl-dcm2niix',
    py_modules=['dcm2niixw'],
    install_requires=['chris_plugin'],
    license='MIT',
    python_requires='>=3.10.2',
    entry_points={
        'console_scripts': [
            'dcm2niixw = dcm2niixw:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ]
)
