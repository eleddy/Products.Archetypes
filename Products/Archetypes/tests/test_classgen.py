import unittest

import Zope # Sigh, make product initialization happen

try:
    Zope.startup()
except: # Zope > 2.6
    pass

from Products.Archetypes.public import *
from Products.Archetypes.config import PKG_NAME
from Products.Archetypes import listTypes

from DateTime import DateTime
import unittest
from copy import deepcopy

schema = BaseSchema + Schema((
    TextField('atextfield',
              widget=RichWidget(description="Just a text field for the testing",
                                  label="A Text Field",
                                  )),

    FileField('afilefield',
              widget=RichWidget(description="Just a file field for the testing",
                                  label="A File Field",
                                  )),

    LinesField('alinesfield', widget=LinesWidget),

    DateTimeField('adatefield',
                  widget=CalendarWidget(description="A date field",
                                        label="A Date Field")),

    ObjectField('anobjectfield',
                widget=StringWidget(description="An object field",
                                    label="An Object Field"),
                validators=('isURL',),
                ),

    FixedPointField('afixedpointfield',
                    widget=DecimalWidget(description="A fixed point field",
                                         label="A Fixed Point Field"),
                    ),
    StringField('awriteonlyfield', mode="w"),
    
    StringField('areadonlyfield', mode="r"),
    ))


class Dummy(BaseContent):

    def __init__(self, oid, init_transforms=0, **kwargs):
        BaseContent.__init__(self, oid, **kwargs)

def gen_dummy():
    Dummy.schema = deepcopy(schema)
    registerType(Dummy)
    content_types, constructors, ftis = process_types(listTypes(), PKG_NAME)

class ClassGenTest( unittest.TestCase ):

    def setUp( self ):
        gen_dummy()
        self._dummy = Dummy(oid='dummy')
        self._dummy.initializeArchetype()

    def test_methods(self):
        obj = self._dummy
        #setters
        self.failUnless(hasattr(obj, 'setAtextfield'))
        self.failUnless(hasattr(obj, 'setAfilefield'))
        self.failUnless(hasattr(obj, 'setAlinesfield'))
        self.failUnless(hasattr(obj, 'setAdatefield'))
        self.failUnless(hasattr(obj, 'setAnobjectfield'))
        self.failUnless(hasattr(obj, 'setAfixedpointfield'))
        self.failUnless(hasattr(obj, 'setAwriteonlyfield'))
        self.failUnless(not hasattr(obj, 'setAreadonlyfield'))
        #getters
        self.failUnless(hasattr(obj, 'getAtextfield'))
        self.failUnless(hasattr(obj, 'getAfilefield'))
        self.failUnless(hasattr(obj, 'getAlinesfield'))
        self.failUnless(hasattr(obj, 'getAdatefield'))
        self.failUnless(hasattr(obj, 'getAnobjectfield'))
        self.failUnless(hasattr(obj, 'getAfixedpointfield'))
        self.failUnless(not hasattr(obj, 'getAwriteonlyfield'))
        self.failUnless(hasattr(obj, 'getAreadonlyfield'))
        #raw getters
        self.failUnless(hasattr(obj, 'getRawAtextfield'))
        self.failUnless(hasattr(obj, 'getRawAfilefield'))
        self.failUnless(hasattr(obj, 'getRawAlinesfield'))
        self.failUnless(hasattr(obj, 'getRawAdatefield'))
        self.failUnless(hasattr(obj, 'getRawAnobjectfield'))
        self.failUnless(hasattr(obj, 'getRawAfixedpointfield'))
        self.failUnless(hasattr(obj, 'getRawAwriteonlyfield'))
        self.failUnless(not hasattr(obj, 'getRawAreadonlyfield'))
        
    def test_textfield(self):
        obj = self._dummy
        obj.setAtextfield('Bla')
        self.failUnless(str(obj.getAtextfield()) == 'Bla')

    def test_filefield(self):
        obj = self._dummy
        obj.setAfilefield('Bla')
        self.failUnless(str(obj.getAfilefield()) == 'Bla')

    def test_linesfield(self):
        obj = self._dummy
        obj.setAlinesfield(['Bla', 'Ble', 'Bli'])
        self.failUnless(obj.getAlinesfield() == ['Bla', 'Ble', 'Bli'])

    def test_datefield(self):
        obj = self._dummy
        obj.setAdatefield('2002/01/01')
        self.failUnless(obj.getAdatefield() == DateTime('2002/01/01'))

    def test_objectfield(self):
        obj = self._dummy
        obj.setAnobjectfield('bla')
        self.failUnless(obj.getAnobjectfield() == 'bla')

    def test_fixedpointfield(self):
        obj = self._dummy
        obj.setAfixedpointfield('26.05')
        self.failUnless(obj.getAfixedpointfield() == '26.05')

    def test_writeonlyfield(self):
        obj = self._dummy
        obj.setAwriteonlyfield('bla')
        self.failUnless(obj.getRawAwriteonlyfield() == 'bla')
        
    def tearDown( self ):
        del self._dummy

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(ClassGenTest),
        ))

if __name__ == '__main__':
    unittest.main()
