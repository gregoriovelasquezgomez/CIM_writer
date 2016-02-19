
'''This .py writes the IEEE 13 nodes test feeder in cim/xml text
using the PyCIM module
'''
#import all neccessary modules
#READY

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
#_____________________ Base Voltage ______________________
#_________________________________________________________
#creates the neccessary base voltages
#READY (verify base if it is 440)
BaseV_4160 = BaseVoltage(4160)
BaseV_4160.UUID = str(uuid.uuid1())
dictionary[BaseV_4160.UUID]= BaseV_4160

BaseV_480 = BaseVoltage(480)
BaseV_480.UUID = str(uuid.uuid1())
dictionary[BaseV_480.UUID]= BaseV_480


#_________________________________________________________
#_____________________ Nodes _____________________________
#_________________________________________________________
#Create all the connectivity nodes of the grid, that will be Bus objects in Power Factory
#READY

Node_650 = ConnectivityNode(name='Node_650')
Node_650.UUID = str(uuid.uuid1())
dictionary[Node_650.UUID]= Node_650

Node_646 = ConnectivityNode(name='Node_646')
Node_646.UUID = str(uuid.uuid1())
dictionary[Node_646.UUID]= Node_646

Node_645 = ConnectivityNode(name='Node_645')
Node_645.UUID = str(uuid.uuid1())
dictionary[Node_645.UUID]= Node_645

Node_632 = ConnectivityNode(name='Node_632')
Node_632.UUID = str(uuid.uuid1())
dictionary[Node_632.UUID]= Node_632

Node_633 = ConnectivityNode(name='Node_633')
Node_633.UUID = str(uuid.uuid1())
dictionary[Node_633.UUID]= Node_633

Node_634 = ConnectivityNode(name='Node_634')
Node_634.UUID = str(uuid.uuid1())
dictionary[Node_634.UUID]= Node_634

Node_611 = ConnectivityNode(name='Node_611')
Node_611.UUID = str(uuid.uuid1())
dictionary[Node_611.UUID]= Node_611

Node_684 = ConnectivityNode(name='Node_684')
Node_684.UUID = str(uuid.uuid1())
dictionary[Node_684.UUID]= Node_684

Node_652 = ConnectivityNode(name='Node_652')
Node_652.UUID = str(uuid.uuid1())
dictionary[Node_652.UUID]= Node_652

#special node for the line_632_671
Node_632_671 = ConnectivityNode(name='Node_632_671')
Node_632_671.UUID = str(uuid.uuid1())
dictionary[Node_632_671.UUID]= Node_632_671

Node_671 = ConnectivityNode(name='Node_671')
Node_671.UUID = str(uuid.uuid1())
dictionary[Node_671.UUID]= Node_671

Node_680 = ConnectivityNode(name='Node_680')
Node_680.UUID = str(uuid.uuid1())
dictionary[Node_680.UUID]= Node_680

Node_692 = ConnectivityNode(name='Node_692')
Node_692.UUID = str(uuid.uuid1())
dictionary[Node_692.UUID]= Node_692

Node_675 = ConnectivityNode(name='Node_675')
Node_675.UUID = str(uuid.uuid1())
dictionary[Node_675.UUID]= Node_675



#_________________________________________________________
#_____________________ Source ____________________________
#_________________________________________________________
#create the source and its connections to node 632 assuming that the source is the node 650 itself
#READY
#create terminal related to the source
ter_source = Terminal(name= 'ter_source', ConnectivityNode= Node_650)
ter_source.UUID = str(uuid.uuid1())

#create the Energy Source instance which represent the full equivalent network
source_EE = EnergySource(phases='ABCN',name='energy_source', x=0.0, r=0.0, activePower=5000, nominalVoltage=4160, voltageAngle=0.0)
source_EE.UUID = str(uuid.uuid1())

dictionary[source_EE.UUID] = source_EE
dictionary[ter_source.UUID]= ter_source


#_________________________________________________________
#_____________________ Transformer _______________________
#_________________________________________________________
#create a transformer with its windings and terminals

#create terminal related to the HV winding
ter_HV = Terminal(name= 'ter_HV', ConnectivityNode= Node_633)
ter_HV.UUID = str(uuid.uuid1())
#create terminal related to the LV winding
ter_LV = Terminal(name= 'ter_LV', ConnectivityNode= Node_634)
ter_LV.UUID = str(uuid.uuid1())


#creates HV winding
HV_winding = TransformerWinding(name='HV_winding', phases='ABC', connectionType='Yn',
     windingType= 'primary', ratedU=4160, ratedS=500, x=1.0, r=1.0)
HV_winding.UUID = str(uuid.uuid1())
"""For a two winding transformer, the full reactance of the transformer 
should be entered on the primary (high voltage) winding."""

#creates LV winding
LV_winding = TransformerWinding(name='LV_winding', phases='ABC', connectionType='Yn',
     windingType= 'secondaty', ratedU=480, ratedS=500)
LV_winding.UUID = str(uuid.uuid1())
#creates the Power Transformer object, which contain the windings
XFM_1 = PowerTransformer(name='XFM-1', TransformerWindings = [HV_winding,LV_winding])
XFM_1.UUID = str(uuid.uuid1())

dictionary[HV_winding.UUID] = HV_winding
dictionary[LV_winding.UUID] = LV_winding
dictionary[XFM_1.UUID] = XFM_1


#_________________________________________________________
#_____________________ Lines _____________________________
#_________________________________________________________
#creates line_650_632 and its terminals
#READY (change parameters to real ones)

#initially create the terminals (with UUID, name and respective CN) related to the line
ter650_l632 = Terminal(name='ter650_l632', ConnectivityNode=Node_650)
ter650_l632.UUID = str(uuid.uuid1())
ter632_l650 = Terminal(name='ter632_l650', ConnectivityNode=Node_632)
ter632_l650.UUID = str(uuid.uuid1())

#create the line with its parameters and UUID
Line_650_632 = ACLineSegment(name='Line_650_632', r=0.3257, x=0.3153, r0=0.5336, x0=0.88025, length=0.6096, phases='ABCN', Terminals=[ter650_l632, ter632_l650])
Line_650_632.UUID = str(uuid.uuid1())
Line_650_632._BaseVoltage = BaseV_4160

#put the objects in the dictionary for cimwrite
dictionary[Line_650_632.UUID]= Line_650_632
dictionary[ter650_l632.UUID]= ter650_l632
dictionary[ter632_l650.UUID]= ter632_l650
#_________________________________________________________

#creates line_632_633 and its terminals
#READY (change parameters to real ones)

#initially create the terminals (with UUID, name and respective CN) related to the line
ter632_l633 = Terminal(name='ter632_l633', ConnectivityNode=Node_632)
ter632_l633.UUID = str(uuid.uuid1())
ter633_l632 = Terminal(name='ter633_l632', ConnectivityNode=Node_633)
ter633_l632.UUID = str(uuid.uuid1())

#create the line with its parameters and UUID
Line_632_633 = ACLineSegment(name='Line_632_633', r=0.0814, x=0.0788, r0=0.1334, x0=0.220, length=0.1524, phases='ABCN', Terminals=[ter632_l633, ter633_l632])
Line_632_633.UUID = str(uuid.uuid1())
Line_632_633._BaseVoltage = BaseV_4160

#put the objects in the dictionary for cimwrite
dictionary[Line_632_633.UUID]= Line_632_633
dictionary[ter632_l633.UUID]= ter632_l633
dictionary[ter633_l632.UUID]= ter633_l632
#_________________________________________________________

#creates line_632_645 and its terminals
#READY (change parameters to real ones)

#first of all create the terminals (with UUID, name and respective CN) related to the line
ter632_l645 = Terminal(name='ter632_l645', ConnectivityNode=Node_632)
ter632_l645.UUID = str(uuid.uuid1())
ter645_l632 = Terminal(name='ter645_l632', ConnectivityNode=Node_645)
ter645_l632.UUID = str(uuid.uuid1())

#create the line with its parameters and UUID
line_632_645 = ACLineSegment(name='line_632_645', r=0.081427, x=0.08446, r0=0.1170, x0=0.16579, length=0.1524, phases='CBN', Terminals=[ter632_l645, ter645_l632])
line_632_645.UUID = str(uuid.uuid1())
line_632_645._BaseVoltage = BaseV_4160

#put the objects in the dictionary for cimwrite
dictionary[line_632_645.UUID]= line_632_645
dictionary[ter632_l645.UUID]= ter632_l645
dictionary[ter645_l632.UUID]= ter645_l632

#_________________________________________________________

#creates line_645_646 and its terminals
#READY (change parameters to real ones)

#first of all create the terminals (with UUID, name and respective CN) related to the line
ter645_l646 = Terminal(name='ter645_l646', ConnectivityNode=Node_645)
ter645_l646.UUID = str(uuid.uuid1())
ter646_l645 = Terminal(name='ter646_l645', ConnectivityNode=Node_646)
ter646_l645.UUID = str(uuid.uuid1())

#create the line with its parameters and UUID
line_645_646 = ACLineSegment(name='line_645_646', r=0.04885, x=0.050678, r0=0.070224, x0=0.099476, length=0.09144, phases='CBN', Terminals=[ter645_l646, ter646_l645])
line_645_646.UUID = str(uuid.uuid1())
line_645_646._BaseVoltage = BaseV_4160

#put the objects in the dictionary for cimwrite
dictionary[line_645_646.UUID]= line_645_646
dictionary[ter645_l646.UUID]= ter645_l646
dictionary[ter646_l645.UUID]= ter646_l645

#_________________________________________________________

#creates line_632_671_1 and its terminals
#READY (change parameters to real ones)

#first of all create the terminals (with UUID, name and respective CN) related to the line
ter632_l671_1 = Terminal(name='ter632_l671_1', ConnectivityNode=Node_632)
ter632_l671_1.UUID = str(uuid.uuid1())
ter671_1_l632 = Terminal(name='ter671_1_l632', ConnectivityNode=Node_632_671)
ter671_1_l632.UUID = str(uuid.uuid1())

#create the line with its parameters and UUID
line_632_671_1 = ACLineSegment(name='line_632_671_1', r=0.16285, x=0.15765, r0=0.2668, x0=0.4401294, length=0.3048, phases='ABCN', Terminals=[ter632_l671_1, ter671_1_l632])
line_632_671_1.UUID = str(uuid.uuid1())
line_632_671_1._BaseVoltage = BaseV_4160

#put the objects in the dictionary for cimwrite
dictionary[line_632_671_1.UUID]= line_632_671_1
dictionary[ter632_l671_1.UUID]= ter632_l671_1
dictionary[ter671_1_l632.UUID]= ter671_1_l632

#_________________________________________________________

#creates line_632_671_2 and its terminals
#READY (change parameters to real ones)

#first of all create the terminals (with UUID, name and respective CN) related to the line
ter632_l671_2 = Terminal(name='ter632_l671_2', ConnectivityNode=Node_632_671)
ter632_l671_2.UUID = str(uuid.uuid1())
ter671_2_l632 = Terminal(name='ter671_2_l632', ConnectivityNode=Node_671)
ter671_2_l632.UUID = str(uuid.uuid1())

#create the line with its parameters and UUID
line_632_671_2 = ACLineSegment(name='line_632_671_2', r=0.16285, x=0.15765, r0=0.2668, x0=0.4401294, length=0.3048, phases='ABCN', Terminals=[ter632_l671_2, ter671_2_l632])
line_632_671_2.UUID = str(uuid.uuid1())
line_632_671_2._BaseVoltage = BaseV_4160

#put the objects in the dictionary for cimwrite
dictionary[line_632_671_2.UUID]= line_632_671_2
dictionary[ter632_l671_2.UUID]= ter632_l671_2
dictionary[ter671_2_l632.UUID]= ter671_2_l632

#_________________________________________________________

#creates line_671_680 and its terminals
#READY (change parameters to real ones)

#first of all create the terminals (with UUID, name and respective CN) related to the line
ter671_l680 = Terminal(name='ter671_l680', ConnectivityNode=Node_671)
ter671_l680.UUID = str(uuid.uuid1())
ter680_l671 = Terminal(name='ter680_l671', ConnectivityNode=Node_680)
ter680_l671.UUID = str(uuid.uuid1())

#create the line with its parameters and UUID
line_671_680 = ACLineSegment(name='line_671_680', r=0.16285, x=0.15765, r0=0.2668, x0=0.4401294, length=0.3048, phases='ABCN', Terminals=[ter671_l680, ter680_l671])
line_671_680.UUID = str(uuid.uuid1())
line_671_680._BaseVoltage = BaseV_4160

#put the objects in the dictionary for cimwrite
dictionary[line_671_680.UUID]= line_671_680
dictionary[ter671_l680.UUID]= ter671_l680
dictionary[ter680_l671.UUID]= ter680_l671

#_________________________________________________________

#creates line_671_684 and its terminals
#READY (change parameters to real ones)

#first of all create the terminals (with UUID, name and respective CN) related to the line
ter671_l684 = Terminal(name='ter671_l684', ConnectivityNode=Node_671)
ter671_l684.UUID = str(uuid.uuid1())
ter684_l671 = Terminal(name='ter684_l671', ConnectivityNode=Node_684)
ter684_l671.UUID = str(uuid.uuid1())

#create the line with its parameters and UUID
line_671_684 = ACLineSegment(name='line_671_684', r=0.0488564, x=0.050678, r0=0.07024, x0=0.099476, length=0.09144, phases='ABN', Terminals=[ter671_l684, ter684_l671])
line_671_684.UUID = str(uuid.uuid1())
line_671_684._BaseVoltage = BaseV_4160

#put the objects in the dictionary for cimwrite
dictionary[line_671_684.UUID]= line_671_684
dictionary[ter671_l684.UUID]= ter671_l684
dictionary[ter684_l671.UUID]= ter684_l671

#_________________________________________________________

#creates line_684_652 and its terminals
#READY (change parameters to real ones)

#first of all create the terminals (with UUID, name and respective CN) related to the line
ter684_l652 = Terminal(name='ter684_l652', ConnectivityNode=Node_684)
ter684_l652.UUID = str(uuid.uuid1())
ter652_l684 = Terminal(name='ter652_l684', ConnectivityNode=Node_652)
ter652_l684.UUID = str(uuid.uuid1())

#create the line with its parameters and UUID
line_684_652 = ACLineSegment(name='line_684_652', r=0.12192, x=0.195072, r0=0.0, x0=0.0, length=0.24384, phases='AN', Terminals=[ter684_l652, ter652_l684])
line_684_652.UUID = str(uuid.uuid1())
line_684_652._BaseVoltage = BaseV_4160

#put the objects in the dictionary for cimwrite
dictionary[line_684_652.UUID]= line_684_652
dictionary[ter684_l652.UUID]= ter684_l652
dictionary[ter652_l684.UUID]= ter652_l684

#_________________________________________________________

#creates line_684_611 and its terminals
#READY (change parameters to real ones)

#first of all create the terminals (with UUID, name and respective CN) related to the line
ter684_l611 = Terminal(name='ter684_l611', ConnectivityNode=Node_684)
ter684_l611.UUID = str(uuid.uuid1())
ter611_l684 = Terminal(name='ter611_l684', ConnectivityNode=Node_611)
ter611_l684.UUID = str(uuid.uuid1())

#create the line with its parameters and UUID
line_684_611 = ACLineSegment(name='line_684_611', r=0.05996, x=0.07476, r0=0.0, x0=0.0, length=0.09144, phases='BN', Terminals=[ter684_l611, ter611_l684])
line_684_611.UUID = str(uuid.uuid1())
line_684_611._BaseVoltage = BaseV_4160

#put the objects in the dictionary for cimwrite
dictionary[line_684_611.UUID]= line_684_611
dictionary[ter684_l611.UUID]= ter684_l611
dictionary[ter611_l684.UUID]= ter611_l684

#_________________________________________________________

#creates line_692_675 and its terminals
#READY (change parameters to real ones)

#first of all create the terminals (with UUID, name and respective CN) related to the line
ter692_l675 = Terminal(name='ter692_l675', ConnectivityNode=Node_692)
ter692_l675.UUID = str(uuid.uuid1())
ter675_l692 = Terminal(name='ter675_l692', ConnectivityNode=Node_675)
ter675_l692.UUID = str(uuid.uuid1())

#create the line with its parameters and UUID
line_692_675 = ACLineSegment(name='line_692_675', r=0.080772, x=0.12182, r0=0.080772, x0=0.12182, length=0.1524, phases='ABCN', Terminals=[ter692_l675, ter675_l692])
line_692_675.UUID = str(uuid.uuid1())
line_692_675._BaseVoltage = BaseV_4160

#put the objects in the dictionary for cimwrite
dictionary[line_692_675.UUID]= line_692_675
dictionary[ter692_l675.UUID]= ter692_l675
dictionary[ter675_l692.UUID]= ter675_l692

#_________________________________________________________
#_____________________ Breaker ___________________________
#_________________________________________________________
#creates breaker between node_671 and node_692

#first of all create the terminals (with UUID, name and respective CN) related to the switch
ter671_b692 = Terminal(name='ter671_b692', ConnectivityNode=Node_671)
ter671_b692.UUID = str(uuid.uuid1())
ter692_b671 = Terminal(name='ter692_b671', ConnectivityNode=Node_692)
ter692_b671.UUID = str(uuid.uuid1())

#create the breaker with its parameters and UUID
breaker_671_692 = Switch(name='breaker_671_692', phases='ABCN', Terminals=[ter671_b692, ter692_b671])
breaker_671_692.UUID = str(uuid.uuid1())
breaker_671_692._BaseVoltage = BaseV_4160

#put the objects in the dictionary for cimwrite
dictionary[breaker_671_692.UUID]= breaker_671_692
dictionary[ter671_b692.UUID]= ter671_b692
dictionary[ter692_b671.UUID]= ter692_b671

#_________________________________________________________
#_____________________ Loads _____________________________
#_________________________________________________________

#first of all create the terminals (with UUID, name and respective CN) related to the Load
ter645_load = Terminal(name='ter645_load', ConnectivityNode=Node_645)
ter645_load.UUID = str(uuid.uuid1())

#create the load with its parameters and UUID
load_node645 = EnergyConsumer(name='load_node645', phases='CB', Terminals=[ter645_load], pfixed=0.17, qfixed=0.125)
load_node645.UUID = str(uuid.uuid1())
load_node645._BaseVoltage = BaseV_4160

#put the objects in the dictionary for cimwrite
dictionary[load_node645.UUID]= load_node645
dictionary[ter645_load.UUID]= ter645_load

#_________________________________________________________

#first of all create the terminals (with UUID, name and respective CN) related to the Load
ter646_load = Terminal(name='ter646_load', ConnectivityNode=Node_646)
ter646_load.UUID = str(uuid.uuid1())

#create the load with its parameters and UUID
load_node646 = EnergyConsumer(name='load_node646', phases='CB', Terminals=[ter646_load], pfixed=0.23, qfixed=0.132)
load_node646.UUID = str(uuid.uuid1())
load_node646._BaseVoltage = BaseV_4160

#put the objects in the dictionary for cimwrite
dictionary[load_node646.UUID]= load_node646
dictionary[ter646_load.UUID]= ter646_load

#_________________________________________________________

#first of all create the terminals (with UUID, name and respective CN) related to the Load
ter634_load = Terminal(name='ter634_load', ConnectivityNode=Node_634)
ter634_load.UUID = str(uuid.uuid1())

#create the load with its parameters and UUID
load_node634 = EnergyConsumer(name='load_node634', phases='ABCN', Terminals=[ter634_load], pfixed=0.4, qfixed=0.29)
load_node634.UUID = str(uuid.uuid1())
load_node634._BaseVoltage = BaseV_4160

#put the objects in the dictionary for cimwrite
dictionary[load_node634.UUID]= load_node634
dictionary[ter634_load.UUID]= ter634_load

#_________________________________________________________

#first of all create the terminals (with UUID, name and respective CN) related to the Load
ter632_671_load = Terminal(name='ter632_671_load', ConnectivityNode=Node_632_671)
ter632_671_load.UUID = str(uuid.uuid1())

#create the load with its parameters and UUID
load_node632_671 = EnergyConsumer(name='load_node632_671', phases='ABCN', Terminals=[ter632_671_load], pfixed=0.2, qfixed=0.116)
load_node632_671.UUID = str(uuid.uuid1())
load_node632_671._BaseVoltage = BaseV_4160

#put the objects in the dictionary for cimwrite
dictionary[load_node632_671.UUID]= load_node632_671
dictionary[ter632_671_load.UUID]= ter632_671_load

#_________________________________________________________

#first of all create the terminals (with UUID, name and respective CN) related to the Load
ter671_load = Terminal(name='ter671_load', ConnectivityNode=Node_671)
ter671_load.UUID = str(uuid.uuid1())

#create the load with its parameters and UUID
load_node671 = EnergyConsumer(name='load_node671', phases='ABC', Terminals=[ter671_load], pfixed=1.155, qfixed=0.66)
load_node671.UUID = str(uuid.uuid1())
load_node671._BaseVoltage = BaseV_4160

#put the objects in the dictionary for cimwrite
dictionary[load_node671.UUID]= load_node671
dictionary[ter671_load.UUID]= ter671_load

#_________________________________________________________

#first of all create the terminals (with UUID, name and respective CN) related to the Load
ter692_load = Terminal(name='ter692_load', ConnectivityNode=Node_692)
ter692_load.UUID = str(uuid.uuid1())

#create the load with its parameters and UUID
load_node692 = EnergyConsumer(name='load_node692', phases='ABC', Terminals=[ter692_load], pfixed=0.17, qfixed=0.151)
load_node692.UUID = str(uuid.uuid1())
load_node692._BaseVoltage = BaseV_4160

#put the objects in the dictionary for cimwrite
dictionary[load_node692.UUID]= load_node692
dictionary[ter692_load.UUID]= ter692_load

#_________________________________________________________

#first of all create the terminals (with UUID, name and respective CN) related to the Load
ter675_load = Terminal(name='ter675_load', ConnectivityNode=Node_675)
ter675_load.UUID = str(uuid.uuid1())

#create the load with its parameters and UUID
load_node675 = EnergyConsumer(name='load_node675', phases='ABCN', Terminals=[ter675_load], pfixed=0.843, qfixed=0.462)
load_node675.UUID = str(uuid.uuid1())
load_node675._BaseVoltage = BaseV_4160

#put the objects in the dictionary for cimwrite
dictionary[load_node675.UUID]= load_node675
dictionary[ter675_load.UUID]= ter675_load

#_________________________________________________________

#first of all create the terminals (with UUID, name and respective CN) related to the Load
ter611_load = Terminal(name='ter611_load', ConnectivityNode=Node_611)
ter611_load.UUID = str(uuid.uuid1())

#create the load with its parameters and UUID
load_node611 = EnergyConsumer(name='load_node611', phases='AN', Terminals=[ter611_load], pfixed=0.17, qfixed=0.08)
load_node611.UUID = str(uuid.uuid1())
load_node611._BaseVoltage = BaseV_4160

#put the objects in the dictionary for cimwrite
dictionary[load_node611.UUID]= load_node611
dictionary[ter611_load.UUID]= ter611_load

#_________________________________________________________

#first of all create the terminals (with UUID, name and respective CN) related to the Load
ter652_load = Terminal(name='ter652_load', ConnectivityNode=Node_652)
ter652_load.UUID = str(uuid.uuid1())

#create the load with its parameters and UUID
load_node652 = EnergyConsumer(name='load_node652', phases='AN', Terminals=[ter652_load], pfixed=0.128, qfixed=0.086)
load_node652.UUID = str(uuid.uuid1())
load_node652._BaseVoltage = BaseV_4160

#put the objects in the dictionary for cimwrite
dictionary[load_node652.UUID]= load_node652
dictionary[ter652_load.UUID]= ter652_load
#_________________________________________________________
#_____________________ Capacitors ________________________
#_________________________________________________________
#create the instances of capacitors in the grid


#first of all create the terminals (with UUID, name and respective CN) related to the capacitor
ter675_capacitor = Terminal(name='ter675_capacitor', ConnectivityNode=Node_675)
ter675_capacitor.UUID = str(uuid.uuid1())

#create the capacitor with its parameters and UUID
capacitor_node675= ShuntCompensator(name='capacitor_node675', nomU=4160, nomQ=0.6, phases='ABC', Terminals=[ter675_capacitor])
capacitor_node675.UUID = str(uuid.uuid1())
capacitor_node675._BaseVoltage = BaseV_4160

#put the objects in the dictionary for cimwrite
dictionary[capacitor_node675.UUID]= capacitor_node675
dictionary[ter675_capacitor.UUID]= ter675_capacitor

#_________________________________________________________
#first of all create the terminals (with UUID, name and respective CN) related to the capacitor
ter611_capacitor = Terminal(name='ter611_capacitor', ConnectivityNode=Node_611)
ter611_capacitor.UUID = str(uuid.uuid1())

#create the capacitor with its parameters and UUID
capacitor_node611= ShuntCompensator(name='capacitor_node611', nomU=4160, nomQ=0.1, phases='AN', Terminals=[ter611_capacitor])
capacitor_node611.UUID = str(uuid.uuid1())
capacitor_node611._BaseVoltage = BaseV_4160

#put the objects in the dictionary for cimwrite
dictionary[capacitor_node611.UUID]= capacitor_node611
dictionary[ter611_capacitor.UUID]= ter611_capacitor


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
from PyCIM import cimwrite

path_out = 'IEEE_13ntf_cim.xml'
cimwrite(dictionary, path_out, 'us-ascii')

print '\nWhat is in path:\n'

from PyCIM.PrettyPrintXML import xmlpp
print xmlpp(path_out)
