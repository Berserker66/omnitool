from functools import total_ordering

@total_ordering
class Version():
        """Organization Class for comparable Version System
        Version integer uses decimal shift:
        2 digits major version, 2 digits minor version, 2 digits micro version
        170100 -> 17.1.0
        """
        def __init__(self, integer):
            if type(integer) == str:
                self.int = int(integer)
            elif type(integer) == int:
                self.int = integer
            else:
                raise TypeError("Version accepts int or str, not "+str(type(integer)))

        def get_version_tuple(self):
            major, minor = divmod(self.int,10000)
            minor, micro = divmod(minor, 100)
            return major, minor, micro
        
        def get_name(self):
            major, minor, micro = tup = self.get_version_tuple()
            return ".".join((str(i) for i in tup))
        
        def __repr__(self):
            return self.name

        def __str__(self):
            return str(self.int)
        
        def __eq__(self, other):
            if isinstance(other, Version):
                return self.int == other.int
            return self.int == other
        
        def __lt__(self, other):
            if isinstance(other, Version):
                return self.int < other.int
            return self.int < other
        
        def __int__(self):return self.int
        
        name = property(get_name)
        as_tuple = property(get_version_tuple)

current = Version(100)


if __name__ == "__main__":
    print (current)
    print (current > 200)
    print (current < 100)
    print (current > Version(50))
    assert(Version(100) > 99)
    assert(99 < Version(100))
    assert(100 == Version(100))
    assert(100 != Version(99))
    assert(Version(100) == Version(100))
    assert(Version(str(Version(100))) == Version(100))
