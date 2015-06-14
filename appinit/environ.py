
class Environ(dict):

    def append(self, key, value):
        if key in self:
            self[key] = '%s:%s' % (self[key], value)
        else:
            self[key] = value

