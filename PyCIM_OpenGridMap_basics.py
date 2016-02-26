"""This .py (for python 2) creates and describes the way to write 
a cim-modeled (in version CIM14) power system based on 
PyCIM (http://pydoc.net/Python/PyCIM/15.13.4/CIM14/)

The PyCIM function cimwrite takes the instances of electrical
equipments saved in a dictionary and writes the 
cim text in a file pathed.

The power system modeled is radial and composed of:
1 source, 1 transmission line, 1 transformer, 1 distribution, 1 load
and the nodes between each equipment (the nodes represent substations)

The equipments are connected as follows:

# - Source (simplified model of a generator) -> (node_source)
# -> Transmission Line -> (node_HV)
# -> 2Winding Transformer -> (node_LV)
# -> Distribution Line -> (node_load)
# -> Load"""

#_________________________________________________________
#_____________________ Import Modules ____________________
#_________________________________________________________
#import all modules required (may be more than the required)

from PyCIM import *
from CIM14.IEC61970.Core import*
from CIM14.IEC61970.Wires import *
from CIM14.IEC61970.Topology import *
from CIM14.IEC61970.Equivalents import *
from CIM14.IEC61970.LoadModel import *
import uuid

#initialize the dictionary for cimwrite
dictionary= {}

#_________________________________________________________
#_____________________ nodes _____________________________
#_________________________________________________________
#Create all the connectivity nodes of the grid
#These connectivity nodes represent a simplified model of substation

#call the object for Connectivity nodes
node_source = ConnectivityNode(name='node_source')
#create a UUID for this instance
node_source.UUID = str(uuid.uuid1()) 
#save the instance in the dictionary with the UUID as 'key'
dictionary[node_source.UUID]= node_source

node_HV = ConnectivityNode(name='node_HV')
node_HV.UUID = str(uuid.uuid1())
dictionary[node_HV.UUID]= node_HV

node_LV = ConnectivityNode(name='node_LV')
node_LV.UUID = str(uuid.uuid1())
dictionary[node_LV.UUID]= node_LV

node_load = ConnectivityNode(name='node_load')
node_load.UUID = str(uuid.uuid1())
dictionary[node_load.UUID]= node_load

#_________________________________________________________
#_____________________ Base Voltage ______________________
#_________________________________________________________
#creates the neccessary base voltages
#In this case it's simulated a transmission line of 110 kV
#and a distribution line of 44 kV
#This objects (BaseVoltage) are used when the equipments has not nomVoltage attribute
#and it is required the voltage to simulate these equipment in Simulink
BaseV_110 = BaseVoltage(110000)
BaseV_110.UUID = str(uuid.uuid1())
dictionary[BaseV_110.UUID]= BaseV_110

BaseV_44 = BaseVoltage(44000)
BaseV_44.UUID = str(uuid.uuid1())
dictionary[BaseV_44.UUID]= BaseV_44


#_________________________________________________________
#_____________________ Source ____________________________
#_________________________________________________________
#create the source and its Terminal
#the terminal and connectivity node allow the connection between
#equipments. Each equipment has its own terminal to get a connection
#with the connectivity node.

#create the Energy Source instance which models a network equivalent
#the phases specified can also be ABC
source = EnergySource(phases='ABCN',name='source', x=0.01, r=0.01, 
	activePower=5000000, nominalVoltage=110000, voltageAngle=0.0)
source.UUID = str(uuid.uuid1())

#create terminal that connect the source to the node_source
#with the ConnectivityNode attribute refers to the node
#with the _ConductingEquipment attribute refers to the equipment
ter_source = Terminal(name= 'ter_source', ConnectivityNode= node_source, ConductingEquipment=source)
#create a UUID for the ter_source instance
ter_source.UUID = str(uuid.uuid1())

#save the instances in the dictionary with UUID as 'key'
dictionary[source.UUID] = source
dictionary[ter_source.UUID]= ter_source



#_________________________________________________________
#_____________________ Lines _____________________________
#_________________________________________________________
#create Transmission (tl), Distribution (dl) lines and its terminals
#each line require 2 terminals as it's connected in 2 sides

#______________________ Transmission _____________________

#create the terminals (with UUID, name and respective CN) related to the line
#in this case the relation between the terminal and the conducting equipment is
#is defined in the transmission line object, but can be the other way around also.
ter_source_tl = Terminal(name='ter_source_tl', ConnectivityNode=node_source)
ter_source_tl.UUID = str(uuid.uuid1())
ter_tl_HV = Terminal(name='ter_tl_HV', ConnectivityNode=node_HV)
ter_tl_HV.UUID = str(uuid.uuid1())

#create the line with its parameters and UUID
Transmission = ACLineSegment(name='Transmission', r=0.3257, x=0.3153, r0=0.5336, 
	x0=0.88025, length=100, phases='ABCN', Terminals=[ter_source_tl, ter_tl_HV])
Transmission.UUID = str(uuid.uuid1())

#put the instances in the dictionary
dictionary[Transmission.UUID]= Transmission
dictionary[ter_source_tl.UUID]= ter_source_tl
dictionary[ter_tl_HV.UUID]= ter_tl_HV

#_____________________ Distribution _______________________

#create the line with its parameters and UUID
Distribution = ACLineSegment(name='Distribution', r=0.3257, x=0.3153, r0=0.5336, 
	x0=0.88025, length=10, phases='ABCN')
Distribution.UUID = str(uuid.uuid1())

#in this case the relation between terminal and line is defined in the terminals
#to show that this it's also possible, but can be the other way around also.
#create the terminals (with UUID, name and respective CN) related to the line
ter_LV_dl = Terminal(name='ter_LV_dl', ConnectivityNode=node_LV, ConductingEquipment=Distribution)
ter_LV_dl.UUID = str(uuid.uuid1())
ter_dl_LV = Terminal(name='ter_dl_LV', ConnectivityNode=node_load, ConductingEquipment=Distribution)
ter_dl_LV.UUID = str(uuid.uuid1())

#put the instances in the dictionary
dictionary[Distribution.UUID]= Distribution
dictionary[ter_LV_dl.UUID]= ter_LV_dl
dictionary[ter_dl_LV.UUID]= ter_dl_LV


#_________________________________________________________
#_____________________ Transformer _______________________
#_________________________________________________________
#create a transformer with its windings and terminals
#The 2 transformer windings are contained in a 
#powertransformer instance

#creates HV winding
HV_winding = TransformerWinding(name='HV_winding', phases='ABCN', connectionType='Yn',
     windingType= 'primary', ratedU=110000, ratedS=5000000, x=1.0, r=1.0)
HV_winding.UUID = str(uuid.uuid1())
"""For a two winding transformer, the full reactance of the transformer 
should be entered on the primary (high voltage) winding."""

#creates LV winding
LV_winding = TransformerWinding(name='LV_winding', phases='ABCN', connectionType='Yn',
     windingType= 'secondaty', ratedU=44000, ratedS=5000000)
LV_winding.UUID = str(uuid.uuid1())

#creates the Power Transformer object, which contain the windings
Transformer = PowerTransformer(name='Transformer', TransformerWindings = [HV_winding,LV_winding])
Transformer.UUID = str(uuid.uuid1())

#create terminal related to the HV winding
ter_HV = Terminal(name= 'ter_HV', ConnectivityNode= node_HV, ConductingEquipment=HV_winding)
ter_HV.UUID = str(uuid.uuid1())
#create terminal related to the LV winding
ter_LV = Terminal(name= 'ter_LV', ConnectivityNode= node_LV, ConductingEquipment=LV_winding)
ter_LV.UUID = str(uuid.uuid1())

dictionary[ter_HV.UUID] = ter_HV
dictionary[ter_LV.UUID] = ter_LV
dictionary[HV_winding.UUID] = HV_winding
dictionary[LV_winding.UUID] = LV_winding
dictionary[Transformer.UUID] = Transformer

#_________________________________________________________
#_____________________ Load _____________________________
#_________________________________________________________

#create the load with its parameters and UUID
load = EnergyConsumer(name='load', phases='ABCN', pfixed=1000000, qfixed=200000)
load.UUID = str(uuid.uuid1())
#set the base voltage of the load
load._BaseVoltage = BaseV_44

ter_load = Terminal(name='ter_load', ConnectivityNode=node_load, ConductingEquipment=load)
ter_load.UUID = str(uuid.uuid1())

#put the objects in the dictionary for cimwrite
dictionary[ter_load.UUID]= ter_load
dictionary[load.UUID]= load


#_________________________________________________________
#_____________________ Sort Dictionary ___________________
#_________________________________________________________
#This sorting process isn't fundamental, but
#makes output more human readable.

import collections #package to sort the dictionary

d_vals=sorted(dictionary.values())
d_keys= sorted(dictionary, key=dictionary.get)
dictionary = collections.OrderedDict(zip(d_keys, d_vals))

#_________________________________________________________
#_____________________ Write CIM _________________________
#_________________________________________________________
#Final step is to write the instances in CIM text

from PyCIM import cimwrite #module to write the CIM text

path_out = 'PyCIM_OpenGridMap_basics.xml'
cimwrite(dictionary, path_out)

print '\nWhat is in path:\n'
from PyCIM.PrettyPrintXML import xmlpp #module to print and view output
print xmlpp(path_out)
