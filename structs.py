# -*- coding: utf-8 -*-
"""Boilerplate:
Created on Mon Jun  7 15:43:06 2021

@author: Timothe
"""

import os

####### CUSTOM TYPES AND OBJECTS

# class sdict(dict):

#     def __init__(self,value=None):
#         """
#         A class for a modified version of python built in dictionnary,
#         with enhanced indexation abilities : get or set values with lists or ':' operator.
#         This requires a more rigorous aproach regarding variable order while writing to it,
#         but is this downside is neglected when used inside a class wich takes care of the acess,
#         as in "TwoLayerDict" declared below.

#         Parameters
#         ----------
#         value : TYPE, optional
#             DESCRIPTION. The default is None.

#         Returns
#         -------
#         None.

#         Timothe Jost - 2021
#         """
#         if value is None:
#             value = {}
#         super(sdict, self).__init__(value)
#         self._dyn_attrs = []
#         #self._update_attrs()

#     def _update_attrs(self):
#         [ self.__delattr__(key) for key in self._dyn_attrs ]
#         self._dyn_attrs = [ key for key in super(sdict, self).keys() ]
#         [ self.__setattr__(key, super(sdict, self).__getitem__(key) ) if not isinstance( super(sdict, self).__getitem__(key),dict ) else self.__setattr__(key, sdict(super(sdict, self).__getitem__(key)) ) for key in self._dyn_attrs]

#     @staticmethod
#     def _assert_index_single(index):
#         return True if isinstance(index,(str,int,float)) else False

#     @staticmethod
#     def _assert_index_iter(index):
#         return True if isinstance(index,(list,tuple)) else False

#     @staticmethod
#     def _assert_index_dict(index):
#         return True if isinstance(index,(dict,set)) else False

#     @staticmethod
#     def _assert_index_dotslice(index):
#         if isinstance(index,slice):
#             if index.start is None and index.step is None and index.stop is None :
#                 return True
#             else :
#                 raise ValueError("Only ':' slice operator is allowed for whole selection as sliceable_dict is unordered")
#         return False

#     @staticmethod
#     def _assert_key_match(subset,masterset):
#         if set(subset) & (set(masterset)) != set(subset) :
#             raise KeyError("A key provided for indexing doesn't exist in data")

#     @staticmethod
#     def _assert_iter_len_match(one,two):
#         if not isinstance(one,(list,tuple)) or not isinstance(two,(list,tuple)) or len(one) != len(two) :
#             raise ValueError("sizes must match")

#     def __getitem__(self,index):
#         if self._assert_index_single(index):
#             return super().__getitem__(index)
#         elif self._assert_index_iter(index):
#             self._assert_key_match(index,self.keys())
#             return sdict({ key : self[key] for key in index })
#         elif self._assert_index_dotslice(index):
#             return self
#         raise TypeError(f"Unsupported indexer :{index}")

#     def __setitem__(self,index,value):
#         if self._assert_index_single(index):
#             super().update({index:value})
#         elif self._assert_index_iter(index):
#             if self._assert_index_dict(value):
#                 self._assert_key_match(index,value.keys())
#                 [super(sdict, self).update({key : value[key]}) for ix, key in enumerate(index)]
#             else :
#                 self._assert_iter_len_match(index,value)
#                 [super(sdict, self).update({key : value[ix]}) for ix, key in enumerate(index)]
#         elif self._assert_index_dotslice(index):
#             if self._assert_index_dict(value):
#                 self.clear()
#                 super().update(value)
#             else :
#                 raise ValueError("A dictionnary must be provided when overwriting values with ':' slicing operator")
#         else :
#             raise TypeError(f"Unsupported indexer :{index}")
#         #self._update_attrs()

#     def update(self,*value):
#         super().update(*value)
#         #self._update_attrs()

#     class _default_proxy():
#         """
#         Just an empty class to fake a default condition equal to no other possible value the user could enter.
#         (because we want to preserve None as a possible user value in this case)
#         """
#         pass

#     _default_holder = _default_proxy()#Placeholder for a "None" default arg value, to allow None or any other value as an optionnal argument
    
#     def pop(self,value,default = _default_holder):
#         _inner_default_holder = self._default_proxy()
#         local_super = super()
#         def _pop_helper(key,_default = _inner_default_holder):
#             if not isinstance(default,sdict._default_proxy):
#                 return local_super.pop(key,default)
#             else :
#                 return local_super.pop(key)
                
#         if self._assert_index_single(value):
#             retval = _pop_helper(value,default)
#         elif self._assert_index_iter(value):
#             retval = {val:_pop_helper(val,default) for val in value}
#         elif self._assert_index_dict(value):
#             iterkeys = list(value.keys())
#             retval = {val:_pop_helper(val,value[val]) for val in iterkeys}
#         elif self._assert_index_dotslice(value):
#             iterkeys = list(self.keys())
#             retval = {val:_pop_helper(val,default) for val in iterkeys}
            
#         #self._update_attrs()
#         return retval

class sdict(dict):
    pass


class TwoLayerDict(sdict):
    def __init__(self,value=None):
        """
        A class for a forced two layer indexing dictionnary.
        Usefull to access config files with section param value architecture
        and read-write to them seamlessly from this python object as if it was
        only a nested dictionnary.
        Based on sdict and inheriting from it's indexation abilities.

        Parameters
        ----------
        value : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        Timothe Jost - 2021
        """
        if value is None:
            value = {}
        else :
            self._assert_two_layers(value)
        super().__init__(value)


    
    def pop(self, *args):#fisrt argument is indices (or index) second argument is default value
        index = args[0] 
        try :
            outindex, inindex = self._assert_index(index)
        except ValueError:
            outindex, inindex = index, None
            
        if inindex is None :
            c_args = ( outindex ,*args[1:])
            default = super().pop(*c_args)
        else  :
            try :
                c_args = (inindex ,*args[1:])
                default = self[outindex].pop(*c_args)
            except KeyError: #outindex is not in self.keys()
                try :
                    default =  args[1] #return default value if supplied 
                except IndexError :
                    raise KeyError(f"Key pair {outindex}, {inindex} not in dictionnary")
                    
        self._values_changed_callback()    
        return default
    
    
    def get(self,outer,inner,*args):
        try :
            return super().__getitem__(outer)[inner]
        except KeyError:
            try:
                return args[0]#return default argument if it exists
            except IndexError:
                raise KeyError(f"Key pair {outer}, {inner} not in dictionnary")
    
    def update(self,value):
        
        self._assert_two_layers(value)
        for key, val in value.items():
            try :
                self[key].update(val)
            except KeyError :
                super().__setitem__(key, val)
        self._values_changed_callback()
            
    def __getitem__(self, index):
        try :
            outindex, inindex = self._assert_index(index)
        except ValueError :
            return super().__getitem__(index)#only one index supplied, return the whole second layer correspuunding to outer key
        
        return super().__getitem__(outindex).__getitem__(inindex)#double indexing : two keys for value access
            
    def __setitem__(self, index, value):
        try :
            outindex, inindex = self._assert_index(index)
        except ValueError:#only one index supplied, acess the whole second layer correspuunding to outer key
            outindex, inindex = index, None
        
        if inindex is None :
            if isinstance(value,dict):
                super().__setitem__(outindex, value)
            else :
                raise ValueError("Cannot assign a non dictionnary to a single key")
        else :
            try : 
                self[outindex].update({inindex:value})
            except KeyError : #if outindex is not in self.keys()
                super().__setitem__(outindex,{inindex:value})
            
        self._values_changed_callback()
        
    def __getattr__(self,key):
        if key in self.keys():
            return self[key]
        else :
            raise KeyError(f"TwoLayerDict has no key {key} at first level")
        
    def __setattr__(self,key,value):
        if not isinstance(value,dict):
            raise TypeError("a value assigned to a section must be a dictionnary")
                
        if key in self.keys():
            self[key].update(value)
        else :
            self[key] = value
        self._values_changed_callback()

    def _values_changed_callback(self):
        pass #an empty callback called whenever a value changed. Cen be used in class deriving, and in particular ConfigFiles

    @staticmethod 
    def _assert_two_layers(value): #verifies that value is a valid two layer dictionnary
        if isinstance(value,TwoLayerDict):
            return True
        if not isinstance(value,dict):
            raise TypeError("A TwoLayerDict dictionnary must be dictionnary")
        for key in value.keys():
            if not isinstance(value[key],dict):
                raise ValueError(f"Each value in a TwoLayerDict must have two keys, not the case for key :'{key}'")

    @staticmethod
    def _assert_index(index): #verifies that the index has two separate keys. First one being outer layer and second one being inner
        if isinstance(index,(list,tuple)) or len(index) == 2:
            return index[0],index[1]
        else :
            raise ValueError("TwoLayerDict must be indexed with two keys")

    def __str__(self):
        out = "{\n"
        for key in self.keys():
            out += str(key) + " : {\n"
            for skey in self[key]:
                out += "\t" + str(skey) + " : " + str(self[key][skey]) + ",\n"
            out += "\t},\n"
        out += "}"
        return out
        
    def __repr__(self):
        return self.__str__()
        


################# USEFULL METHODS


def get_properties_names(cls):
    """
    Get a list of all the names of the properties of a given class.
    (usefull for copying all variables/parameters of an object programatically with eval)

    Parameters
    ----------
    cls : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        All properties that are not callable
        (= most of the existing variables except some dumb variables like the
         callable ones i created, (like nan_padded_array).
    """
    def stringiscallable(string,cls):
        return callable(eval(f"cls.{string}"))
    return [ a for a in dir(cls) if not a.startswith('__') and not stringiscallable(a,cls) ]


class func_io_typematch():
    """Converts a type back to the one it had entering a function.
    """
    def __init__(self,*args):
        self.casts = [type(arg) for arg in args]

    def cast(self,*args):

        if len(args) != len(self.casts):
            raise ValueError("Argument amount lengths must match between construction and cast call")

        try :
            return [self.casts[index](args[index]) for index, _ in enumerate(args) ] if len(args)>1 else self.casts[0](args[0])
        except Exception as e:
            raise TypeError(f"Cannot convert this specific type back.\nOriginal error : {e}")
            #return args if len(args)>1 else args[0]

import _dependancies as _deps

try :
    import numpy as np
except ImportError as e :
    np = _deps.default_placeholder("numpy",e)
    _deps.dep_miss_warning(np)

class memarray(np.memmap):
    def __new__(cls, input_array,**kwargs):
        import random
        rdir = kwargs.pop("root",os.path.abspath("memaps")) 
        if not os.path.isdir(rdir):
            os.makedirs(rdir)
        while True :   
            filename = os.path.join(rdir,"".join([ chr(65+int(random.random()*26)+int(random.random()+0.5)*32) for _ in range(10)]) + ".mmp")
            if not os.path.isfile(filename):
                break       
                
        memobj = super().__new__(cls, filename, shape = input_array.shape , mode = kwargs.pop("mode","w+"), **kwargs )
        whole_slices = tuple([slice(None)]*len(input_array.shape))
        memobj[whole_slices] = input_array[whole_slices]
        
        return memobj
    
    def close(self):
        try :
            self.flush()
            if self._mmap is not None:
                self._mmap.close()
        except ValueError :
            return


if __name__ == "__main__" :
    print(TwoLayerDict({"toast":{"test":1, "truc": 2},"fal":{"test":1, "truc": 2}}))