import abc

from copy import deepcopy

import mixin
from .propertiesdata import PropertiesData


class PropertiesDataBounds(mixin.Ancillaries, PropertiesData):
    '''Base class for a data array with bounds and with descriptive
properties.

    '''
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, properties={}, data=None, bounds=None,
                 cell_type=None, ancillaries=None, source=None,
                 copy=True, _use_data=True):
        '''**Initialization**

:Parameters:

    properties: `dict`, optional
        Set descriptive properties. The dictionary keys are property
        names, with corresponding values. Ignored if the *source*
        parameter is set.

          *Example:*
             ``properties={'standard_name': 'longitude'}``
        
        Properties may also be set after initialisation with the
        `properties` and `set_property` methods.
  
    data: `Data`, optional
        Set the data array. Ignored if the *source* parameter is set.
        
        The data array also may be set after initialisation with the
        `set_data` method.
  
    bounds: `Bounds`, optional
        Set the bounds array. Ignored if the *source* parameter is
        set.
        
        The bounds array also may be set after initialisation with the
        `set_bounds` method.
  
    source: optional
        Initialise the *properties*, *data* and *bounds* parameters
        from the object given by *source*.
  
    copy: `bool`, optional
        If False then do not deep copy arguments prior to
        initialization. By default arguments are deep copied.

        '''
        # Initialise properties and data
        super(PropertiesDataBounds, self).__init__(
            properties=properties,
            data=data,
            source=source,
            copy=copy,
            _use_data=_use_data)

        if source is not None:
            try:
                bounds = source.get_bounds(None)
            except AttributeError:
                bounds = None
                
            try:
                cell_type = source.get_cell_type(None)
            except AttributeError:
                cell_type = None
                
            try:
                ancillaries = source.get_ancillaries()
            except AttributeError:
                ancillaries = None
        #--- End: if

        # Initialise bounds
        if bounds is not None:
            if copy or not _use_data:
                bounds = bounds.copy(data=_use_data)
                
            self.set_bounds(bounds, copy=False)
        #--- End: if

        if cell_type is not None:
            self.set_cell_type(cell_type)

        if ancillaries is None:
            ancillaries = {}
        elif copy or not _use_data:
            ancillaries = ancillaries.copy()
            for key, value in ancillaries.items():
                try:
                    ancillaries[key] = value.copy(data=_use_data)
                except AttributeError:
                    ancillaries[key] = deepcopy(value)
        #--- End: if
            
        self.ancillaries(ancillaries, copy=False)
    #--- End: def

    @property
    def bounds(self):
        '''
        '''
        return self.get_bounds()
    #--- End: def

    def copy(self, data=True):
        '''Return a deep copy.

``c.copy()`` is equivalent to ``copy.deepcopy(c)``.

:Examples 1:

>>> d = c.copy()

:Parameters:

    data: `bool`, optional
        If False then do not copy the data nor bounds. By default the
        data and bounds are copied.

:Returns:

    out:
        The deep copy.

:Examples 2:

>>> d = c.copy(data=False)

        '''
        return super(PropertiesDataBounds, self).copy(data=data)
    #--- End: def

    def del_bounds(self):
        '''Delete the bounds.

.. seealso:: `del_data`, `get_bounds`, `has_bounds`, `set_bounds`

:Examples 1:

>>> c.del_bounds()

:Returns: 

    out: `Bounds` or `None`
        The removed bounds, or `None` if the data was not set.

:Examples 2:

>>> c.has_bounds()
True
>>> print c.get_bounds()
PPPPPPPPPPPPPPPPPPPPP
>>> d = c.del_bounds()
>>> print d
PPPPPPPPPPPPPPPPPPPPP
>>> c.has_bounds()
False
>>> print c.del_bounds()
None

        '''
        return self._del_component('bounds')
    #--- End: def

    def del_bounds(self):
        '''Delete the bounds type.

.. seealso:: `del_data`, `get_bounds`, `has_bounds`, `set_bounds`

:Examples 1:

:Returns: 

    out: `str` or `None`

:Examples 2:

        '''
        return self._del_component('cell_type')
    #--- End: def

    def get_bounds(self, *default):
        '''Return the bounds.

.. seealso:: `get_array`, `get_data`, `has_bounds`, `set_bounds`

:Examples 1:

>>> b = c.get_bounds()

:Parameters:

    default: optional
        Return *default* if and only if the bounds have not been set.

:Returns:

    out:
        The bounds. If the bounds have not been set, then return the
        value of *default* parameter if provided.

:Examples 2:

>>> b = c.del_bounds()
>>> c.get_bounds('No bounds')
'No bounds'

        '''
        return self._get_component('bounds', None, *default)
    #--- End: def

    def get_cell_type(self, *default):
        '''Return the bounds type.

.. seealso:: `get_array`, `get_data`, `has_bounds`, `set_bounds`

:Examples 1:

:Parameters:

    default: optional
        Return *default* if and only if the bounds have not been set.

:Returns:

    out:

:Examples 2:

        '''
        return self._get_component('cell_type', None, *default)
    #--- End: def

#    def get_bounds_mapping(self, *default):
#        '''???????
#
#.. seealso:: `bounds_mapping`, `del_bounds_mapping`, `set_bounds_mapping`
#
#:Examples 1:
#
#>>> bm = c.get_bounds_mapping()
#
#:Parameters:
#
#    default: optional
#        Return *default* if and only if the bounds have not been set.
#
#:Returns:
#
#    out:
#
#
#:Examples 2:
#
#        '''
#        return self._get_component('bounds_mapping', None, *default)
#    #--- End: def
#
#    def get_cell_extent(self, *default):
#        '''???????
#
#.. seealso:: `cell_extent`, `del_cell_extent`, `set_cell_extent`
#
#:Examples 1:
#
#>>> e = c.get_cell_extent()
#
#:Parameters:
#
#    default: optional
#        Return *default* if and only if the bounds have not been set.
#
#:Returns:
#
#    out:
#
#
#:Examples 2:
#
#        '''
#        return self._get_component('cell_extent', None, *default)
#    #--- End: def

    def has_bounds(self):
        '''True if there are bounds.
        
.. seealso:: `del_bounds`, `get_bounds`, `has_data`, `set_bounds`

:Examples 1:

>>> x = f.has_bounds()

:Returns:

    out: `bool`
        True if there are bounds, otherwise False.

:Examples 2:

>>> if c.has_bounds():
...     print 'Has bounds'

        '''
        return self._has_component('bounds')
    #--- End: def

    def has_cell_type(self):
        '''True if there is a bounds type.
        
.. seealso:: `del_bounds`, `get_bounds`, `has_data`, `set_bounds`

:Examples 1:

>>> x = f.has_cell_type()

:Returns:

    out: `bool`

:Examples 2:

        '''
        return self._has_component('cell_type')
    #--- End: def

    def set_bounds(self, bounds, copy=True):
        '''Set the bounds.

.. seealso: `del_bounds`, `get_bounds`, `has_bounds`, `set_data`

:Examples 1:

>>> c.set_bounds(b)

:Parameters:

    data: `Bounds`
        The bounds to be inserted.

    copy: `bool`, optional
        If False then do not copy the bounds prior to insertion. By
        default the bounds are copied.

:Returns:

    `None`

:Examples 2:

>>> c.set_data(b, copy=False)

        '''
        if copy:
            bounds = bounds.copy()

        self._set_component('bounds', None, bounds)
    #--- End: def

    def set_cell_type(self, value):
        '''Set the bounds type.

.. seealso: `del_bounds`, `get_bounds`, `has_bounds`, `set_data`

:Examples 1:

:Parameters:

    value: `str`

:Returns:

    `None`

:Examples 2:
        '''
        self._set_component('cell_type', None, value)
    #--- End: def

#--- End: class
