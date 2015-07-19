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
            appinit = appinit.command:main
        ''',
        'sitehooks': '''
            appinit = appinit:sitehook
        ''',
        'appinit_apps': '''
            houdini = appinit.apps.houdini:Houdini
            it = appinit.apps.it:IT
            mari = appinit.apps.mari:Mari
            maya = appinit.apps.maya:Maya
            nuke = appinit.apps.nuke:Nuke
        ''',
        'appinit.maya': '''
            000_standalone_initialize = appinit.apps.maya:standalone_initialize
            zzz_gui_initialize = appinit.apps.maya:gui_initialize
        ''',
        'appinit.houdini': '''
            appinit_houdini_gui_idle = appinit.apps.houdini.runtime:_defer_gui_idle_trigger
        ''',
    }

)
