

class BaseApp(object):

    @classmethod
    def iter_installed(cls):
        return iter(())

    def __init__(self, path=None, version=None):
        self.path = path
        self.version = version

    def get_python(self):
        return None

    def get_site_packages(self):
        pass
    
    def get_executable(self):
        raise NotImplementedError()

