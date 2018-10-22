from future.utils import with_metaclass
from builtins import (str, super)

import abc

from copy import deepcopy

from . import Container


class Properties(with_metaclass(abc.ABCMeta, Container)):
    '''Abstract base class for an object with descriptive properties.

    '''
    def __init__(self, properties=None, source=None, copy=True):
        '''**Initialization**

:Parameters:

    properties: `dict`, optional
        Set descriptive properties. The dictionary keys are property
        names, with corresponding values. Ignored if the *source*
        parameter is set.

          *Example:*
             ``properties={'standard_name': 'altitude'}``
        
        Properties may also be set after initialisation with the
        `properties` and `set_property` methods.

    source: optional
        Override the *properties* parameter with
        ``source.properties()``.

        If *source* does not have this method then the *properties*
        parameter is not set.
        
    copy: `bool`, optional
        If False then do not deep copy input parameters prior to
        initialization By default parameters are deep copied.

        '''
        super().__init__()

        self._set_component('properties', {}, copy=False)
        
        if source is not None:
            try:
                properties = source.properties()
            except AttributeError:
                properties = None
        #--- End: if
        
        if properties:
            self.properties(properties, copy=copy)
    #--- End: def
        
    def __deepcopy__(self, memo):
        '''x.__deepcopy__() -> Deep copy of data.

Used if copy.deepcopy is called on the object.

        '''
        return self.copy()
    #--- End: def

    def __repr__(self):
        '''x.__repr__() <==> repr(x)

        '''
        return '<{0}: {1}>'.format(self.__class__.__name__, str(self))
    #--- End: def

    # ----------------------------------------------------------------
    # Methods
    # ----------------------------------------------------------------
    def copy(self):
        '''Return a deep copy.

``f.copy()`` is equivalent to ``copy.deepcopy(f)``.

:Examples 1:

>>> g = f.copy()

:Returns:

    out:
        The deep copy.

        '''
        return type(self)(source=self, copy=True)
    #--- End: def

    def del_property(self, prop):
        '''Remove a property.

A property describes an aspect of the construct that is independent of
the domain and may have any name and value. Some properties correspond
to CF-netCDF attributes, such as 'standard_name', 'history', etc.

.. seealso:: `get_property`, `has_property`, `properties`, `set_property`

:Examples 1:

>>> x = f.del_property('standard_name')

:Parameters:

    prop: `str`
        The name of the property to be removed.

:Returns:

     out:
        The removed property, or `None` if the property was not set.

:Examples 2:

>>> f.set_property('project', 'CMIP7')
>>> f.has_property('project')
True
>>> f.get_property('project')
'CMIP7'
>>> f.del_property('project')
'CMIP7'
>>> f.has_property('project')
False
>>> print(f.del_property('project'))
None
>>> print(f.get_property('project', None))
None

        '''
        return self._get_component('properties').pop(prop, None)
    #--- End: def

    def get_property(self, prop, *default):
        '''Return a property.

A property describes an aspect of the construct that is independent of
the domain and may have any name and value. Some properties correspond
to CF-netCDF attributes, such as 'standard_name', 'history', etc.

.. seealso:: `del_property`, `has_property`, `properties`, `set_property`

:Examples 1:

>>> x = f.get_property('method')

:Parameters:

    prop: `str`
        The name of the property to be returned.

    default: optional
        Return *default* if the property has not been set.

:Returns:

    out:
        The value of the property. If the property has not been then
        the *default* parameter is returned, if provided.

:Examples 2:

>>> f.set_property('project', 'CMIP7')
>>> f.has_property('project')
True
>>> f.get_property('project')
'CMIP7'
>>> f.del_property('project')
'CMIP7'
>>> f.has_property('project')
False
>>> print(f.del_property('project'))
None
>>> print(f.get_property('project', None))
None

        '''
        try:
            return self._get_component('properties')[prop]
        except KeyError:
            if default:
                return default[0]

            raise AttributeError("{!r} has no {!r} property".format(
                self.__class__.__name__, prop))
    #--- End: def

    def has_property(self, prop):
        '''Whether a property has been set.

A property describes an aspect of the construct that is independent of
the domain and may have any name and value. Some properties correspond
to CF-netCDF attributes, such as 'standard_name', 'history', etc.

.. seealso:: `del_property`, `get_property`, `properties`, `set_property`

:Examples 1:

>>> x = f.has_property('long_name')

:Parameters:

    prop: `str`
        The name of the property.

:Returns:

     out: `bool`
        True if the property has been set, otherwise False.

:Examples 2:

>>> f.set_property('project', 'CMIP7')
>>> f.has_property('project')
True
>>> f.get_property('project')
'CMIP7'
>>> f.del_property('project')
'CMIP7'
>>> f.has_property('project')
False
>>> print(f.del_property('project'))
None
>>> print(f.get_property('project', None))
None

        '''
        return prop in self._get_component('properties')
    #--- End: def

    def properties(self, properties=None, copy=True):
        '''Return or replace all properties.

A property describes an aspect of the construct that is independent of
the domain and may have any name and value. Some properties correspond
to CF-netCDF attributes, such as 'standard_name', 'history', etc.

.. seealso:: `del_property`, `get_property`, `has_property`,
             `set_property`

:Examples 1:

>>> p = f.properties()

:Parameters:

    properties: `dict`, optional   

        Replace all existing properties with those specified in the
        dictionary. If the dictionary is empty then all properties
        will be removed.

          *Example:*
             ``properties={'standard_name': 'altitude', 'foo': 'bar'}``
        
          *Example:*
             ``properties={}``        

    copy: `bool`, optional
        If False then any property values provided by the *properties*
        parameter are not copied before insertion. By default they are
        deep copied.

:Returns:

    out: `dict`
        The properties prior to being changed, or the current
        properties if no changes were specified.

:Examples 2:

>>> p = f.properties({'standard_name': 'altitude', 'foo': 'bar'}, copy=False)

        '''
        out = self._get_component('properties').copy()

        if properties is not None:
            if copy:
                properties = deepcopy(properties)                
            else:
                properties = properties.copy()

            self._set_component('properties', properties, copy=False)

        return out
    #--- End: def

    def set_property(self, prop, value, copy=True):
        '''Set a property.

A property describes an aspect of the construct that is independent of
the domain and may have any name and value. Some properties correspond
to CF-netCDF attributes, such as 'standard_name', 'history', etc.

.. seealso:: `del_property`, `get_property`, `has_property`, `properties`

:Examples 1:

>>> f.set_property('standard_name', 'time')

:Parameters:

    prop: `str`
        The name of the property to be set.

    value:
        The value for the property.

:Returns:

     `None`

:Examples 2:

>>> f.set_property('project', 'CMIP7')
>>> f.has_property('project')
True
>>> f.get_property('project')
'CMIP7'
>>> f.del_property('project')
'CMIP7'
>>> f.has_property('project')
False
>>> print(f.del_property('project'))
None
>>> print(f.get_property('project', None))
None

        '''
        if copy:
            value = deepcopy(value)
            
        self._get_component('properties')[prop] = value
    #--- End: def

#--- End: class