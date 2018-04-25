import abc

import mixin
import structure

from .cellextent import CellExtent

# ====================================================================
#
# DimensionCoordinate object
#
# ====================================================================

class DimensionCoordinate(mixin.Coordinate, structure.DimensionCoordinate):
    '''A dimension coordinate construct of the CF data model.

    '''
    __metaclass__ = abc.ABCMeta

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls, *args, **kwargs)
        obj._CellExtent = CellExtent
        return obj
    #--- End: def

    def dump(self, display=True, _omit_properties=None, field=None,
             key=None, _level=0, _title=None):
        '''Return a string containing a full description of the auxiliary
coordinate object.

:Parameters:

    display: `bool`, optional
        If False then return the description as a string. By default
        the description is printed, i.e. ``f.dump()`` is equivalent to
        ``print f.dump(display=False)``.

:Returns:

    out: `None` or `str`
        A string containing the description.

:Examples:

        '''
        if _title is None:
            if key is None:
                default = ''
            else:
                default = key
                
            _title = 'Dimension coordinate: ' + self.name(default=default)
                
        return super(DimensionCoordinate, self).dump(
            display=display, _omit_properties=_omit_properties,
            field=field, key=key,
             _level=_level, _title=_title)
    #--- End: def

#--- End: class
