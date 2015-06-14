from setuptools import setup, find_packages

setup(

    name='appinit',
    version='0.1.0',
    description='Unified startup for VFX applications.',
    url='http://github.com/sitg/appinit',
    
    packages=find_packages(exclude=['build*', 'tests*']),
    
    author='Mike Boers',
    author_email='appinit@mikeboers.com',
    license='BSD-3',
    
    include_package_data=True,
    entry_points={
        'console_scripts': '''
            appinit-exec   = appinit.exec_:main
            appinit-python = appinit.exec_:main_python
        ''',
        'appinit_maya_sitehook': '''
            000_appinit_initialize = appinit.maya:on_sitehook
        ''',
    }

)
