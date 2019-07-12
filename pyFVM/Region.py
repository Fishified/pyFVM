
import pyFVM.IO as io
import pyFVM.FoamDictionaries as fd
import pyFVM.Polymesh as pm
import pyFVM.Equation as equation
import pyFVM.Field as field



class Region():

    """Sets up the simulation's 'Region'.

    An instance of the Region class is required for the case to run. 
    The instance is created at the beginning of each case and is used to hold
    other class instances, such as 'polyMesh', any number of 'fluid' instances
    and a number of other attributes required for the simulation to run.

    """

    def __init__(self,casePath):
        
        """Initiates the class instance with the caseDirectoryPath attribute 
        and adds the 'dictionaries' and 'fluid' dictionaries. Reminder - 
        __init__ functions are run automatically when a new class instance is 
        created. This docstring does not appear in Sphinx documentation.
    
        """
        
        io.cfdPrintMainHeader()
        
        self.caseDirectoryPath = casePath
        self.STEADY_STATE_RUN = True

        print('Working case directory is %s' % self.caseDirectoryPath)
        
        #empty dictionary to hold 'fluid' properties. I a better name is 'field'
        self.fluid={}
        
        
        
        #model is used to hold the various equations
        self.model={}



        #creates an instance of the FoamDictionaires class
        #most of FoamDictionaries methods are initiated in the __init__
        #function, but two are not: 'cfdReadTimeDirectory' and cfdReadTransportProperties()
        self.dictionaries=fd.FoamDictionaries(self)
        
        
        
        #creats and instance of Polymesh, which runs all the methods necessary
        #to get the mesh topology from the __init__ function of the class
        self.mesh=pm.Polymesh(self)
        
        print('\n')
        self.cfdGeometricLengthScale()



        #these two require the mesh and therefore are not included in the __init__
        #function of FoamDictionaries and are instead run after initializing 
        #self.mesh. 
        self.dictionaries.cfdReadTimeDirectory()
        
        
        
        #update boundary values for phi field 
        for i in self.fluid:
            if self.fluid[i].type == 'volScalarField':
                self.fluid[i].cfdUpdateScalarFieldForAllBoundaryPatches()
            
        self.dictionaries.cfdReadTransportProperties()
        
#        self.model['phi']=equation.Equation(self,'phi')
#        self.model['phi'].setTerms(['Transient', 'Convection'])
#        
#        self.fluid['mdot_f']=field.Field(self,'mdot_f','surfaceScalarField')
#        self.fluid['mdot_f'].dimensions=[0,0,0,0,0,0,0]
        
    def cfdGeometricLengthScale(self):
    
        """
        Calculates the geometric length scale of the mesh. 
        """
    
        self.totalVolume = sum(self.mesh.elementVolumes)
        self.lengthScale = self.totalVolume**(1/3)
    

