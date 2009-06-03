#! /usr/bin/python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Name:     ProjectCli.py
# Purpose:  
# Author:   Fabien Marteau <fabien.marteau@armadeus.com>
# Created:  23/05/2008
#-----------------------------------------------------------------------------
#  Copyright (2008)  Armadeus Systems
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software 
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
#-----------------------------------------------------------------------------
# Revision list :
#
# Date       By        Changes
#
#-----------------------------------------------------------------------------

__doc__ = ""
__version__ = "1.0.0"
__versionTime__ = "23/05/2008"
__author__ = "Fabien Marteau <fabien.marteau@armadeus.com>"

import cmd,os
#import readline
import periphondemand.bin.define

from   periphondemand.bin.utils import wrapperxml,settings,error,basecli,wrappersystem
from   periphondemand.bin.utils import wrappersystem as sy
from   periphondemand.bin.utils.display  import Display

from   periphondemand.bin.code.vhdl.topvhdl      import TopVHDL

from   periphondemand.bin.commandline               import *
from   periphondemand.bin.commandline.synthesiscli  import SynthesisCli
from   periphondemand.bin.commandline.simulationcli import SimulationCli
from   periphondemand.bin.commandline.drivercli     import DriverCli

from   periphondemand.bin.utils.settings import Settings
from   periphondemand.bin.utils.basecli  import BaseCli
from   periphondemand.bin.utils.error    import Error

from   periphondemand.bin.core.project     import Project
from   periphondemand.bin.core.component   import Component
from   periphondemand.bin.core.platform    import Platform
from   periphondemand.bin.core.library     import Library

from   periphondemand.bin.code.intercon      import Intercon
from   periphondemand.bin.code.vhdl.topvhdl  import TopVHDL

from   periphondemand.bin.toolchain.synthesis   import Synthesis
from   periphondemand.bin.toolchain.simulation  import Simulation
from   periphondemand.bin.toolchain.driver      import Driver

settings = Settings()
display  = Display()

class ProjectCli(BaseCli):
    """ Project command line interface
    """
    def __init__(self,parent=None):
        BaseCli.__init__(self,parent)
        if settings.active_project is None:
            settings.active_project = Project("",void=1)
        if settings.active_library is None:
            settings.active_library = Library()
    
    def do_synthesis(self,arg):
        """\
Usage : synthesis
synthesis commands
        """
        try:
            self.isProjectOpen()
            self.isPlatformSelected()
        except Error,e:
            print e
            return

        cli = SynthesisCli(self)
        cli.setPrompt("synthesis")
        arg = str(arg)
        if len(arg) > 0:
            line = cli.precmd(arg)
            cli.onecmd(line)
            cli.postcmd(True, line)
        else:
            cli.cmdloop()
            self.stdout.write("\n")

    def do_simulation(self,line):
        """\
Usage : simulation
Simulation generation environment
        """
        try:
            self.isProjectOpen()
            self.isPlatformSelected()
        except Error,e:
            print e
            return
   
        # test if only one toolchain for simulation in library
        cli = SimulationCli(self)
        cli.setPrompt("simulation")
        line = str(line)
        if len(line) > 0:
            line = cli.precmd(line)
            cli.onecmd(line)
            cli.postcmd(True, line)
        else:
            cli.cmdloop()
            self.stdout.write("\n")

    def do_driver(self,line):
        """\
Usage : driver
Driver generation environment
        """
        try:
            self.isProjectOpen()
            self.isPlatformSelected()
        except Error,e:
            print e
            return
   
        # test if only one toolchain for simulation in library
        cli = DriverCli(self)
        cli.setPrompt("driver")
        line = str(line)
        if len(line) > 0:
            line = cli.precmd(line)
            cli.onecmd(line)
            cli.postcmd(True, line)
        else:
            cli.cmdloop()
            self.stdout.write("\n")

    def do_create(self,line):
        """\
Usage : create <projectname>
create new project
        """
        try:
            self.checkargs(line,"<projectname>")
        except Error,e:
            print e
            return
        try:
            sy.check_name(line)
        except Error,e:
            print e
            return 0
        dirname = os.path.abspath(line)
        if sy.dirExist(dirname):
            print "Project "+line+" already exists"
            return 0
        else:
            try:
                settings.active_project = Project(dirname,void=0)
            except Error,e:
                print e
                return

        self.setPrompt("project",settings.active_project.getName())
        print "Project "+settings.active_project.getName()+" created"

    def complete_load(self,text,line,begidx,endidx):
        """ complete load command with files under directory """
        path = line.split(" ")[1]
        if path.find("/") == -1: # sub
            path = ""
        elif text.split() == "": # sub/sub/
            path = "/".join(path)+"/"
        else: # sub/sub
            path = "/".join(path.split("/")[0:-1]) + "/"
        listdir = sy.listDirectory(path)
        listfile = sy.listFileType(path,"xml")
        listfile.extend(listdir)
        return self.completelist(line,text,listfile)

    def do_load(self,line):
        """\
Usage : projectload <projectfilename>.xml
Load a project
        """
        try:
            self.checkargs(line,"<projectfilename>.xml")
        except Error,e:
            print e
            return
        if sy.dirExist(line):
           head,projectname = os.path.split(line)
           line = os.path.join(head,projectname,projectname+".xml")
        if not sy.fileExist(line):
            print Error("File doesn't exists")
            return
        try:
                settings.active_project = Project(line)
        except Error,e:
            print e
            return
        except IOError,e:
            print e
            return
        self.setPrompt("project:"+settings.active_project.getName())
        print display

    def complete_addinstance(self,text,line,begidx,endidx):
        componentlist = []
        try:
            componentlist = self.completeargs(text,line,"<libraryname>.<componentname>.[componentversion] [newinstancename]")
        except Exception,e:
            print e
        return componentlist

    def do_addinstance(self,line):
        """\
Usage : addinstance <libraryname>.<componentname>.[componentversion] [newinstancename]
Add component in project
        """
        try:
            self.isProjectOpen()
            self.isPlatformSelected()
            self.checkargs(line,"<libraryname>.<componentname>.[componentversion] [newinstancename]")
        except Error,e:
            print display
            print e
            return 
        arg = line.split(' ')
        subarg = arg[0].split(".")
        try:
            instancename= arg[1]
        except IndexError:
            instancename=None
        try:
            componentversion=subarg[2]
        except IndexError:
            componentversion=None
        try:
            if instancename != None:
                sy.check_name(instancename)
            if instancename== None and componentversion==None:
                settings.active_project.addinstance(componentname=subarg[1],
                                                     libraryname=subarg[0])
            elif instancename != None and componentversion==None:
                settings.active_project.addinstance(componentname=subarg[1],
                                                     libraryname=subarg[0],
                                                     instancename=instancename)
            elif instancename == None and componentversion!=None:
                settings.active_project.addinstance(componentname=subarg[1],
                                                     libraryname=subarg[0],
                                                     componentversion=componentversion)
            else:
                settings.active_project.addinstance(componentname=subarg[1],
                                                     libraryname=subarg[0],
                                                     componentversion=componentversion,
                                                     instancename=instancename)
        except Error,e:
            print display
            print e
            return
        print display
    
    def complete_listcomponents(self,text,line,begidx,endidx):
        componentlist = []
        try:
            componentlist = self.completeargs(text,line,"[libraryname]")
        except Exception,e:
            pass
        return componentlist

    def do_listcomponents(self,line):
        """\
Usage : listcomponents [libraryname]
List components available in the library
        """
        if line.strip() == "":
            return self.columnize(settings.active_library.listLibraries())
        else:
            return self.columnize(
                    settings.active_library.listComponents(line))

    def listinstances(self):
        try:
            self.isProjectOpen()
            return [comp.getInstanceName()\
                    for comp in settings.active_project.getInstancesList()]
        except Error,e:
            print e
            return

    def do_listinstances(self,line=None):
        """\
Usage : listinstances
List all project instances
        """
        try:
            self.isProjectOpen()
        except Error,e:
            print e
            return 
        return self.columnize(self.listinstances())

    def complete_selectplatform(self,text,line,begidx,endidx):
        platformlist = []
        try:
            platformlist = self.completeargs(text,line,"<platformname>")
        except Exception,e:
            print e
        return platformlist

    def do_selectplatform(self,line):
        """\
Usage : selectplatform <platformname>
Select the platform to use
        """
        try:
            self.isProjectOpen()
            self.checkargs(line,"<platformname>")
        except Error,e:
            print e
            return
        try:
           settings.active_project.selectPlatform(line)
           settings.active_project.saveProject()
        except Error,e:
            print e
            return
        print display
        
    def do_listplatforms(self,line=None):
        """\
Usage : listplatforms
List platform available
        """
        try:
            self.isProjectOpen()
        except Error,e:
            print e
            return
        try:
            return self.columnize(settings.active_project.listAvailablePlatforms())
        except AttributeError,e:
            print e

    def complete_listinterfaces(self,text,line,begidx,endidx):
        pinlist = []
        try:
            pinlist = self.completeargs(text,line,"<instancename>")
        except Exception,e:
            print e
        return pinlist


    def do_listinterfaces(self,line=None):
        """\
Usage : listinterfaces
List instance interface
        """
        try:
            self.checkargs(line,"<instancename>")
            self.isProjectOpen()
            interfacelist= [interface.getName() for interface in settings.active_project.getInstance(line).getInterfacesList()]
        except Error,e:
            print display
            print e
            return
        print display
        return self.columnize(interfacelist)

    def do_saveproject(self,line=None):
        """\
Usage : saveproject
Save project in the curent directory
        """
        try:
            self.isProjectOpen()
        except Error,e:
            print display
            print e
            return
        print display
        settings.active_project.saveProject()

    def complete_connectpin(self,text,line,begidx,endidx):
        pinlist = []
        try:
            pinlist = self.completeargs(text,line,"<instancename>.<interfacename>.<portname>.<pinnum> <instancename>.<interfacename>.<portname>.<pinnum>")
        except Exception,e:
            print e
        return pinlist
    
    def do_connectpin(self,line):
        """\
Usage : connectpin <instancename>.<interfacename>.<portname>.[pinnum] <instancename>.<interfacename>.<portname>.[pinnum]
Connect pin between instances
        """
        try:
            self.isProjectOpen()
            self.checkargs(line,"<instancename>.<interfacename>.<portname>.[pinnum] <instancename>.<interfacename>.<portname>.[pinnum]")
        except Error,e:
            print display
            print e
            return
        arg = line.split(' ')
        source = arg[0].split('.')
        dest   = arg[-1].split('.')
        if len(source) == 3:
            source.append(None)
        if len(dest) == 3:
            dest.append(None)
        try:
            settings.active_project.connectPin(\
                    settings.active_project.getInstance(
                        source[0]).getInterface(
                            source[1]).getPort(
                                source[2]),\
                                 source[3],\
                    settings.active_project.getInstance(
                        dest[0]  ).getInterface(
                            dest [1]).getPort(dest[2]),\
                                    dest[3])
        except Error, e:
            print display
            print e
            return
        print display

    def complete_connectbus(self,text,line,begidx,endidx):
        buslist = []
        try:
            buslist = self.completeargs(text,line,"<masterinstancename>.<masterinterfacename> <slaveinstancename>.<slaveinterfacename>")
        except Exception,e:
            print e
        return buslist

    def do_connectbus(self,line):
        """\
Usage : connectbus <masterinstancename>.<masterinterfacename> <slaveinstancename>.<slaveinterfacename>
Connect slave to master bus
        """
        try:
            self.isProjectOpen()
            self.checkargs(line,"<masterinstancename>.<masterinterfacename> <slaveinstancename>.<slaveinterfacename>")
        except Exception,e:
            print display
            print e
            return
        arg=line.split(' ')
        source = arg[0].split('.')
        dest   = arg[-1].split('.')
        if len(source) != 2 or len(dest) != 2:
            print "Argument error"
            return
        try:
            settings.active_project.connectBus(source[0],source[1],dest[0],dest[1])
        except Error, e:
            print display
            print e
            return
        print display

    def do_autoconnectbus(self,line):
        """\
Usage : autoconnectbus
Autoconnect bus if only one master in project
        """
        try:
            self.isProjectOpen()
            settings.active_project.autoConnectBus()
        except Error,e:
            print display
            print e
            return
        print display

    def complete_addbusclock(self,text,line,begidx,endidx):
        clocklist = []
        try:
            clocklist = self.completeargs(text,line,"<instancesysconname>.<interfacename> <masterinstancename>.<masterinterfacename>")
        except Exception,e:
            print e
        return clocklist

    def do_addbusclock(self,line):
        """\
Usage : busaddclock <instancesysconname>.<interfacename> <masterinstancename>.<masterinterfacename>
Specify the bus clock
        """
        try:
            self.isProjectOpen()
            self.checkargs(line,"<instancesysconname>.<interfacename> <masterinstancename>.<masterinterfacename>")
        except Error,e:
            print display
            print e
            return
        arg=line.split(' ')
        source = arg[0].split('.')
        dest   = arg[-1].split('.')
        if len(source) != 2 or len(dest) != 2:
            print "Argument error"
            return
        try:
            settings.active_project.connectClkDomain(source[0],dest[0],source[1],dest[1])
        except Error, e:
            print display
            print e
            return
        print display

    def complete_delconnection(self,text,line,begidx,endidx):
        connectlist = []
        try:
            connectlist = self.completeargs(text,line,"<instancename>.<interfacename>.<portname>.<pinnum> <instancename>.<interfacename>.<portname>.<pinnum>")
        except Exception,e:
            print e
        return connectlist

    def do_delconnection(self,line):
        """\
Usage : delconnection <instancename>.<interfacename>.<portname>.[pinnum] [instancename].[interfacename].[portname].[pinnum]
Suppress a pin connection
        """
        try:
            self.isProjectOpen()
            self.checkargs(line,"<instancename>.<interfacename>.<portname>.[pinnum] [instancename].[interfacename].[portname].[pinnum]")
        except Error,e:
            print display
            print e
            return
        # get arguments
        arg     = line.split(' ')
        # make source and destination tabular
        source  = arg[0].split('.')
        dest    = arg[-1].split('.')
        # check if dest "instance.interface.port.pin" present,
        # if not set it to [None] tabular
        try:
            dest   = arg[1].split('.')
        except IndexError:
            dest = [None,None,None,None]
        # check if pin num present, if not set it None
        if len(source) == 3: # instead of 4
            source.append(None)
        if len(dest) == 3 :
            dest.append(None)
        try:
            settings.active_project.deletePin(source[0],source[1],source[2],source[3],
                                              dest[0],dest[1],dest[2],dest[3])
        except Error, e:
            print display
            print e
            return
        print display
        print "Connection deleted"

    def complete_delinstance(self,text,line,begidx,endidx):
        componentlist = []
        try:
            componentlist = self.completeargs(text,line,"<instancename>")
        except Exception,e:
            print e
        return componentlist

    def do_delinstance(self,line):
        """\
Usage : delinstance <instancename>
Suppress a component from project
        """
        try:
            self.isProjectOpen()
            self.checkargs(line,"<instancename>")
        except Error,e:
            print display
            print e
            return
        try:
            settings.active_project.delProjectComponent(line)
        except Error,e:
            print display
            print e
            return
        print display

    def do_check(self,line=None):
        """\
Usage : check
Check the project before code generation
        """
        try:
            self.isProjectOpen()
            settings.active_project.check()
        except Error,e:
            print display
            print e
        print display

    def complete_setaddr(self,text,line,begidx,endidx):
        addrlist = []
        try:
            addrlist = self.completeargs(text,line,"<slaveinstancename>.<slaveinterfacename> <addressinhexa>")
        except Exception,e:
            print e
        return addrlist

    def do_setaddr(self,line):
        """\
Usage : setaddr <slaveinstancename>.<slaveinterfacename> <addressinhexa>
Set the base address of slave interface
        """
        try:
            self.isProjectOpen()
            self.checkargs(line,"<slaveinstancename>.<slaveinterfacename> <addressinhexa>")
        except Error,e:
            print display
            print e
            return
        arg = line.split(' ')
        names = arg[0].split('.')
        if len(names) < 2:
            masterinterface = settings.active_project.getInstance(names[0]).getSlaveInterfaceList()
            if len(masterinterface) != 1:
                print display
                print "Error, need a slave interface name"
                return
            names.append(masterinterface[0].getName())
            
        try:
            interfaceslave = settings.active_project.getInstance(names[0]).getInterface(names[1])
            interfacemaster = interfaceslave.getMaster()
            interfacemaster.allocMem.setAddressSlave(interfaceslave,arg[1])
        except Error,e:
            print display
            print e
            return
        print display
        print "Base address "+arg[1]+" set"

    def do_listmasters(self,line=None):
        """\
Usage : listmaster
List master interface
        """
        try:
            self.isProjectOpen()
        except Error,e:
            print display
            print e
            return
        for master in settings.active_project.getInterfaceMaster():
            print master.parent.getInstanceName()+"."+master.getName()
        print display

    def complete_getmapping(self,text,line,begidx,endidx):
        mappinglist = []
        try:
            mappinglist = self.completeargs(text,line,"<masterinstancename>.<masterinterfacename>")
        except Exception,e:
            print e
        return mappinglist

    def do_getmapping(self,line=None):
        """\
Usage : getmapping <masterinstancename>.<masterinterfacename>
Return mapping for a master interface
        """
        try:
            self.isProjectOpen()
            self.checkargs(line,"<masterinstancename>.<masterinterfacename>")
        except Error,e:
            print display
            print e
            return
        arg = line.split(' ')
        names = arg[0].split('.')
        try:
            masterinterface = settings.active_project.getInstance(names[0]).getInterface(names[1])
            print masterinterface.allocMem
        except Error,e:
            print display
            print e
        print display

    def complete_printxml(self,text,line,begidx,endidx):
        printlist = []
        try:
            printlist = self.completeargs(text,line,"<instancename>")
        except Exception,e:
            print e
        return printlist

    def do_printxml(self,line=None):
        """\
Usage : printxml <instancename>
Print instance in XML format
        """
        try:
            self.isProjectOpen()
            self.checkargs(line,"<instancename>")
        except Error,e:
            print display
            print e
            return
        print settings.active_project.getInstance(line)
        print display

    def complete_info(self,text,line,begidx,endidx):
        infolist = []
        try:
            infolist = self.completeargs(text,line,"<instancename>")
        except Exception,e:
            print e
        return infolist

    def do_info(self,line=None):
        """\
Usage : info <instancename>
Print instance information
        """
        try:
            self.isProjectOpen()
            self.checkargs(line,"<instancename>")
            instance = settings.active_project.getInstance(line)
        except Error,e:
            print display
            print e
            return
        print "Instance name :"+instance.getInstanceName()
        print "Component  name :"+instance.getName()
        print "description : "+instance.getDescription().strip()
        print "->Generics"
        for generic in instance.getGenericsList():
            print "%15s : "%generic.getName() + generic.getValue()
        print "->Interfaces"
        for interface in instance.getInterfacesList():
            if interface.getBusName() != None:
                if interface.getClass() == "SLAVE":
                    print "%-15s "%interface.getName()+" Base address:"+hex(interface.getBaseInt())
                elif interface.getClass() == "MASTER":
                    print "%-15s :"%interface.getName()
                    for slave in interface.getSlavesList():
                        print " "*10 + "slave -> "+slave.getInstanceName()+"."+slave.getInterfaceName()
            else:
                print "%-15s :"%interface.getName()

            for port in interface.getPortsList():
                print " "*5+"%-15s"%port.getName()+" s"+port.getSize()
                for pin in port.getListOfPin():
                    print " "*8+"pin",
                    if pin.getNum()!= None:
                        print pin.getNum()+":",
                    elif pin.isAll():
                        print "all",
                    first = True
                    for connection in pin.getConnections():
                        if first is not True:
                            print " "*8+"|"+" "*5,
                        first = False
                        print "-> "+connection["instance_dest"]+"."+connection["interface_dest"]+"."+connection["port_dest"]+"."+connection["pin_dest"]

    def complete_setgeneric(self,text,line,begidx,endidx):
        genericlist = []
        try:
            genericlist = self.completeargs(text,line,"<instancename>.<genericname> <genericvalue>")
        except Exception,e:
            print e
        return genericlist

    def do_setgeneric(self,line=None):
        """\
Usage : setgeneric <instancename>.<genericname> <genericvalue>
Set generic parameter
        """
        try:
            self.isProjectOpen()
            self.checkargs(line,"<instancename>.<genericname> <genericvalue>")
        except Error,e:
            print display
            print e
            return
        args = line.split(" ")
        names = args[0].split(".")
        try:
            instance = settings.active_project.getInstance(names[0])
            generic = instance.getGeneric(names[1])
            if generic.isPublic()=="true":
                generic.setValue(args[1])
            else:
                raise Error("this generic can't be modified by user",0)
        except Error,e:
            print display
            print e
            return
        print display
        print "Done"

    def do_description(self,line):
        """\
Usage : description <some word for description>
set the project description
        """
        settings.active_project.setDescription(line)
        print display
        print "Description set : "+line
        return 

    def do_closeproject(self,line):
        """\
Usage : closeproject
Close the project
        """
        try:
            self.isProjectOpen()
        except Error,e:
            print display
            print e
            return
        settings.active_project = None
        print display
        print "Project closed"

    # Generate CODE
    
    def complete_intercon(self,text,line,begidx,endidx):
        interconlist = []
        try:
            interconlist = self.completeargs(text,line,"<masterinstancename>.<masterinterfacename>")
        except Exception,e:
            print e
        return interconlist


    ############# FIXME: Move it in synthesiscli ? ######################-
    def do_intercon(self,line=None):
        """\
Usage : intercon <masterinstancename>.<masterinterfacename>
Generate intercon for master given in argument
        """
        try:
            self.isProjectOpen()
            self.checkargs(line,"<instancename>.<masterinterfacename>")
        except Error,e:
            print e
            return
        arg = line.split(' ')
        names = arg[0].split('.')
        if len(names) != 2:
            print "Arguments error"
            return
        try:
            settings.active_project.generateIntercon(names[0],names[1])
        except Error,e:
            print e
            return
        print display

    def do_top(self,line):
        """\
Usage : top
Generate top component
        """
        try:
            self.isProjectOpen()
            top = TopVHDL(settings.active_project)
            top.generate()
        except Error,e:
            print e
            return
        print display
        print "Top generated with name : top_"+settings.active_project.getName()+".vhd"

    #####################################################################

    def do_report(self,line):
        """\
Usage : report
Generate a report of the project
        """
        try:
            self.isProjectOpen()
            text = settings.active_project.generateReport()
        except Error,e:
            print display
            print e
            return
        print display
        print "report : "
        print text

    def isProjectOpen(self):
        """ check if project is open, raise error if not
        """
        if settings.active_project.isVoid() :
            raise Error("No project open",0)

