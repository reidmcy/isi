from recordParse import *

#Consider deleteing _fieldDict entries when used

def lazy(f):
    def wrapper(self, *arg, **kwargs):
        if not hasattr(self, "_" + f.__name__):
            setattr(self, "_" + f.__name__, f(self, *arg, **kwargs))
        return getattr(self, "_" + f.__name__)
    return wrapper

class Record(object):
    def __init__(self, inpaper):
        self.bad = False
        if type(inpaper) == dict:
            self._fieldDict = inpaper
        elif type(inpaper) == str:
            try:
                self._fieldDict = isiParser(inpaper)
            except BadPaper as b:
                self.bad = True
                self.error = b
        else:
            raise TypeError

    def authors(self):
        """
        Uses AF then AU fields
        """
        print "SEGDRDGGFGDFGD"
        if 'AF' in self._fieldDict:
            self._authors = self._fieldDict['AF']
        elif 'AU' in self._fieldDict:
            self._authors = self._fieldDict['AU']
        else:
            self._authors = None
        return self._authors
