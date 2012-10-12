#-*- coding:utf-8 -*-


class EnumElem(object):

    def __init__(self, enum, name):

        self.enum = enum
        self.name = name


    def __eq__(self, other):

        return self is other or self.enum is other.enum and self.name == other.name


    def __hash__(self):

        return id(self.enum) + hash(self.name)


    def __str__(self):

        return self.name



class Enum(object):
    u'''
    列挙体もどき
    '''

    def __init__(self, *names):

        self.__objs = set()

        for name in names:
            obj = EnumElem(self, name)
            setattr(self, name, obj)

            self.__objs.add(obj)


        self.__names = names



    def elements(self):

        return list(self)



    def __iter__(self):

        for name in self.__names:

            yield getattr(self, anem)



    def __contains__(self, elem):

        return elem in self.__objs


    def from_str(self, s):

        obj = EnumElem(self, s)

        if obj in self.__objs:
            return getattr(self, s)

        raise AttributeError(s + ' is not contains in enum object')




