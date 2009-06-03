#! /usr/bin/python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Name:     Pin.py
# Purpose:  
# Author:   Fabien Marteau <fabien.marteau@armadeus.com>
# Created:  05/05/2008
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
__versionTime__ = "05/05/2008"
__author__ = "Fabien Marteau <fabien.marteau@armadeus.com>"

from periphondemand.bin.utils.wrapperxml import WrapperXml
from periphondemand.bin.utils.error      import Error

class Pin(WrapperXml):
    """ Manage Pin
        attributes:
            
    """
    
    def __init__(self,parent,**keys):
        """ init Pin,
            __init__(self,parent,node)
            __init__(self,parent,num)
        """
        if "node" in keys:
            self.__initnode(keys["node"])
        elif "num" in keys:
            self.__initnum(keys["num"])
        else:
            raise Error("Keys unknown in Pin",0)
        self.parent = parent

    def __initnode(self,node):
        WrapperXml.__init__(self,node=node)
    def __initnum(self,num):
        WrapperXml.__init__(self,nodename="pin")
        self.setNum(num)

    def getNum(self):
        return self.getAttribute("num")

    def getConnections(self):
        """ return a list of pin connection 
            return ("instance_dest":string,"interface_dest":string,"port_dest":string,"pin_dest":string)
        """
        connectionslist =[]
        if(self.getNode("connect")!=None):
            for element in self.getNodeList("connect"):
                connectionslist.append({"instance_dest":str(element.getAttribute("instance_dest")),\
                             "interface_dest":str(element.getAttribute("interface_dest")),\
                             "port_dest":str(element.getAttribute("port_dest")),\
                             "pin_dest":str(element.getAttribute("pin_dest"))})
        return connectionslist

    def delConnection(self,instance_dest,interface_dest=None,
                           port_dest=None,pin_dest=None):
        """ Suppress a connection
        """
        if(self.getNode("connect")!=None):
            if interface_dest != None:
                self.delNode("connect",
                        {"instance_dest":instance_dest,
                         "interface_dest":interface_dest,
                         "port_dest":port_dest,
                         "pin_dest":str(pin_dest)})
            else:
                self.delNode("connect",
                        {"instance_dest":instance_dest})
        else:
             raise Error("No connection for "
                  +self.getParent().getParent().getParent().getInstanceName()\
                  +"."+self.getParent().getParent().getName()\
                  +"."+self.getParent().getName()\
                  +"."+self.getNum(),0)

    def getConnectedPinList(self):
        """ return list of pins connected to this pin
        """
        project = self.getParent().getParent().getParent().getParent()
        pinlist = []
        for connect in self.getConnections():
            pinlist.append(project.getInstance(
                connect["instance_dest"]).getInterface(
                    connect["interface_dest"]).getPort(
                        connect["port_dest"]).getPin(
                            connect["pin_dest"]))
        return pinlist

    def addConnection(self,instance_destname,interface_destname,
                           port_destname,pin_destnum=None):
        """ add pin connection and check direction compatibility                
        """
        if pin_destnum!=None:
            attributes = {"instance_dest":str(instance_destname),
                          "interface_dest":str(interface_destname),
                          "port_dest":str(port_destname),
                          "pin_dest":str(pin_destnum)}
        else:
            attributes = {"instance_dest":str(instance_destname),
                          "interface_dest":str(interface_destname),
                          "port_dest":str(port_destname)}
        self.addNode(nodename="connect",attributedict=attributes)

    def connectionExists(self,port_dest,pin_dest):
        """ check if this connection exists
        """
        for connect in self.getConnections():
            if connect =={
          "instance_dest":port_dest.getParent().getParent().getInstanceName(),
          "interface_dest":port_dest.getParent().getName(),
          "port_dest":port_dest.getName(),
          "pin_dest":str(pin_dest)}:
                return 1
        return 0

    def isEmpty(self):
        if len(self.getConnections()) == 0:
            return 1
        else:
            return 0

    def setNum(self,num):
        self.setAttribute("num",str(num))
    def getNum(self):
        return self.getAttribute("num")
    def isAll(self): # To Be Remove ?
        if self.getAttribute("all") == "true":
            return 1
        else:
            return 0
    def setAll(self):
        self.setAttribute("all","true")

    def connectPin(self,portdest,pindestnum=None):
        """ connect pin checking if connection exists and in multiple 
            connection can be done.
            attributes:
                portdest       -- port (Port)
                pindestnum     -- pin destination number (str)
        """

        # if the same connection exists -> error
        if pindestnum is None:
            pindestnum = 0

        if self.connectionExists(portdest,pindestnum) == 1:
            raise Error("Connection exists on "\
                +self.getParent().getParent().getParent().getInstanceName()\
                +"."+self.getParent().getParent().getName()\
                +"."+self.getParent().getName()\
                +"."+self.getNum(),0)

        if self.getParent().getDir() == "in" :
            if len(self.getConnections()) != 0:
               try:
                   pindest = portdest.getPin(pindestnum)
                   pindest.delConnection(self.getParent().getParent().getParent().getInstanceName(),
                                      self.getParent().getParent().getName(),
                                      self.getParent().getName(),
                                      self.getNum())
               except:
                   pass
               raise Error("Can't connect more than one pin on 'in' pin",0)
        self.addConnection(
                portdest.getParent().getParent().getInstanceName(),
                portdest.getParent().getName(),
                portdest.getName(),
                pindestnum)

    def autoconnectPin(self):
        """ connect all platform connection, if connection is not for this platform, delete it 
        """
        project = self.getParent().getParent().getParent().getParent()
        for connection in self.getConnections():
            if connection["instance_dest"] == project.getPlatformName():
                connectport = project.getInstance(
                        connection["instance_dest"]).getInterface(
                                connection["interface_dest"]).getPort(
                                        connection["port_dest"])
                connectport.connectPin(connection["pin_dest"],self.getParent(),self.getNum())
            else:
                self.delConnection(connection["instance_dest"])

    def isConnected(self):
        """ Return 1 if pin is connected to something, else return 0 """
        if len(self.getConnectedPinList()) > 0:
            return 1
        else:
            return 0


