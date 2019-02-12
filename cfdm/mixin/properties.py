from __future__ import print_function
from builtins import super

import textwrap

import numpy
import sys

from . import Container


class Properties(Container):
    '''Mixin class for descriptive properties.

.. versionadded:: 1.7.0

    '''
    def _dump_properties(self, _prefix='', _level=0,
                         _omit_properties=None):
        '''TODO

.. versionadded:: 1.7.0

:Parameters:

    omit: sequence of `str`, optional
        Omit the given CF properties from the description.

    _level: `int`, optional

:Returns:

    `str`

**Examples:**

'''
        indent0 = '    ' * _level
        string = []

        properties = self.properties()
        
        if _omit_properties:
            for prop in _omit_properties:
                 properties.pop(prop, None)
        #--- End: if
 
        for prop, value in sorted(properties.items()):
            name   = '{0}{1}{2} = '.format(indent0, _prefix, prop)
            value  = repr(value)
            subsequent_indent = ' ' * len(name)
            if value.startswith("'") or value.startswith('"'):
                subsequent_indent = '{0} '.format(subsequent_indent)
                
            string.append(
                textwrap.fill(name+value, 79,
                              subsequent_indent=subsequent_indent))
        
        return '\n'.join(string)
    #--- End: def

    def equals(self, other, rtol=None, atol=None, verbose=False,
               ignore_data_type=False, ignore_fill_value=False,
               ignore_properties=(), ignore_type=False):
        '''Whether two instances are the same.

Equality is strict by default. This means that:

* the same descriptive properties must be present, with the same
  values and data types, and vector-valued properties must also have
  same the size and be element-wise equal (see the *ignore_properties*
  and *ignore_data_type* parameters).

Two real numbers ``x`` and ``y`` are considered equal if
``|x-y|<=atol+rtol|y|``, where ``atol`` (the tolerance on absolute
differences) and ``rtol`` (the tolerance on relative differences) are
positive, typically very small numbers. See the *atol* and *rtol*
parameters.

Any type of object may be tested but, in general, equality is only
possible with another object of the same type, or a subclass of
one. See the *ignore_type* parameter.

.. versionadded:: 1.7.0

:Parameters:

    other: 
        The object to compare for equality.

    atol: float, optional
        The tolerance on absolute differences between real
        numbers. The default value is set by the `cfdm.ATOL` function.
        
    rtol: float, optional
        The tolerance on relative differences between real
        numbers. The default value is set by the `cfdm.RTOL` function.

    ignore_fill_value: `bool`, optional
        If True then the "_FillValue" and "missing_value" properties
        are omitted from the comparison.

    verbose: `bool`, optional
        If True then print information about differences that lead to
        inequality.

    ignore_properties: sequence of `str`, optional
        The names of properties to omit from the comparison.

    ignore_data_type: `bool`, optional
        If True then ignore the data types in all numerical
        comparisons. By default different numerical data types imply
        inequality, regardless of whether the elements are within the
        tolerance for equality.

    ignore_type: `bool`, optional
        Any type of object may be tested but, in general, equality is
        only possible with another object of the same type, or a
        subclass of one. If *ignore_type* is True then equality is
        possible for any object with a compatible API.

:Returns: 
  
    `bool`
        Whether the two instances are equal.

**Examples:**

>>> p.equals(p)
True
>>> p.equals(p.copy())
True
>>> p.equals('not a colection of properties')
False

>>> q = p.copy()
>>> q.set_property('foo', 'bar')
>>> p.equals(q)
False
>>> p.equals(q, verbose=True)
Field: Non-common property name: foo
Field: Different properties
False

        '''
        pp = super()._equals_preprocess(other, verbose=verbose,
                                        ignore_type=ignore_type)
        if pp in (True, False):
            return pp
        
        other = pp
        
        # ------------------------------------------------------------
        # Check the properties
        # ------------------------------------------------------------
        if ignore_fill_value:
            ignore_properties += ('_FillValue', 'missing_value')

        self_properties  = self.properties()
        other_properties = other.properties()

        if ignore_properties:
            for prop in ignore_properties:
                self_properties.pop(prop, None)
                other_properties.pop(prop, None)
        #--- End: if
                
        if set(self_properties) != set(other_properties):
            if verbose:
                _ =  set(self_properties).symmetric_difference(other_properties)
                for prop in set(self_properties).symmetric_difference(other_properties):                    
                    print("{0}: Non-common property name: {1}".format( 
                        self.__class__.__name__, prop))
            return False

        for prop, x in self_properties.items():
            y = other_properties[prop]

            if not self._equals(x, y,
                                rtol=rtol, atol=atol,
                                ignore_fill_value=ignore_fill_value,
                                ignore_data_type=True, #ignore_data_type,
                                verbose=verbose):
                if verbose:
                    print("{0}: Different {1}: {2!r}, {3!r}".format(
                        self.__class__.__name__, prop, x, y))
                return False
        #--- End: for

        return True
    #--- End: def

    def names(self, extra=None):
        '''Return a name.

By default the name is the first found of the following:

1. The "standard_name" property.
2. The "cf_role" property, preceeded by ``'cf_role='``.
3. The "long_name" property, preceeded by ``'long_name='``.
4. The netCDF variable name, preceeded by ``'ncvar%'``.
5. The value of the *default* parameter.

.. versionadded:: 1.7.0

:Parameters:

    default: optional
        If no other name can be found then return the value of the
        *default* parameter. By default `None` is returned in this
        case.

    ncvar: `bool`, optional
        If False then do not consider the netCDF variable name.

    all_names: `bool`, optional
        If True then return a list of all possible names.

    custom: sequence of `str`, optional
        Replace the ordered list of properties from which to seatch
        for a name. The default list is ``['standard_name', 'cf_role',
        'long_name']``.

        *Parameter example:*
          ``custom=['project']``

        *Parameter example:*
          ``custom=['project', 'long_name']``

:Returns:

        The name. If the *all_names* parameter is True then a list of
        all possible names.

**Examples:**

>>> f.properties()
{'foo': 'bar',
 'long_name': 'Air Temperature',
 'standard_name': 'air_temperature'}
>>> f.nc_get_variable()
'tas'
>>> f.name()
'air_temperature'
>>> f.name(all_names=True)
['air_temperature', 'long_name=Air Temperature', 'ncvar%tas']
>>> x = f.del_property('standard_name')
>>> f.name()
'long_name=Air Temperature'
>>> x = f.del_property('long_name')
>>> f.name()
'ncvar%tas'
>>> f.name(custom=['foo'])
'foo=bar'
>>> f.name(default='no name', custom=['foo'])
['foo=bar', 'no name']

        '''
        properties = self.properties()
        properties.pop('cf_role', None)
        properties.pop('long_name', None)
        
        out = ['{0}={1}'.format(prop, value)
               for prop, value in sorted(properties.items())]

        if extra:
            out = list(extra) + out
            
        n = self.nc_get_variable(None)
        if n is not None:
            out.insert(0, 'ncvar%{0}'.format(n))

        n = self.get_property('long_name', None)
        if n is not None:
            out.insert(0, 'long_name={}'.format(n))
            
        n = self.get_property('cf_role', None)
        if n is not None:
            out.insert(0, 'cf_role={}'.format(n))
            
        n = self.get_property('standard_name', None)
        if n is not None:
            out.insert(0, n)
            
        return out
    #--- End: def

#--- End: class
