from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Products.Archetypes.debug import log, log_exc
##XXX remove dep, report errors properly

class iwidget:
    def __call__(instance, context=None):
        """return a rendered fragment that can be included in a larger
        context when called by a renderer.

        instance - the instance this widget is called for
        context  - should implement dict behavior
        """

    def getContext(self, mode, instance):
        """returns any prepaired context or and empty {}"""

class widget:
    """
    Base class for widgets
    
    A dynamic widget with a reference to a macro that can be used to
    render it
    
    description -- tooltip
    label       -- textual label
    visible     -- 1[default] visible 0 hidden -1 skipped
    """

    __implements__ = (iwidget,)

    security  = ClassSecurityInfo()
    security.declareObjectPublic()
    security.setDefaultAccess("allow")

    _properties = {
        'description' : '',
        'label' : '',
        'visible' : 1, ##XXX Remove for modes
        'attributes' : ''
        }
    
    def __init__(self, **kwargs):
        self._processed  = 0
        self._process_args(**kwargs)
        
    def _process_args(self, **kwargs):
        self.__dict__.update(self._properties)
        self.__dict__.update(kwargs)

    def __call__(self, mode, instance, context=None):
        """Not implemented"""
        return ''

    def getContext(self, instance):
        return {}



from Products.PageTemplates.Expressions import PathExpr
import Products.CMFCore.Expression as ex
from TAL.TALInterpreter import TALInterpreter
from cStringIO import StringIO

engine  = ex.getEngine()
_macro_registry = {}

class macrowidget(widget):
    """macro is the file containing the macros, the mode/view is the
    name of the macro in that file
    """
    
    _properties = widget._properties.copy()
    _properties.update({
        'macro' : None,
        })

    def bootstrap(self, instance):
        # do initialization-like thingies that need the instance
        pass

    def __call__(self, mode, instance, context=None):
        self.bootstrap(instance)
        pt = instance.restrictedTraverse(self.macro)
        macros = pt.macros
        transformer = getattr(context, 'tr_engine', None)
        if transformer is None:
            # ZPT
            output = StringIO()
        
            ti = TALInterpreter(macros[mode], {}, context, output,
                            tal=1, metal=1, strictinsert=0)
            #ti.debug = 1
            ti()
        
            return output.getvalue()
        else:
            # OpenPT with paxtransform
            return transformer.transform(macros[mode], context).text
    
InitializeClass(widget)
