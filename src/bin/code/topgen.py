#! /usr/bin/python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Name:     TopGen.py
# Purpose:  
# Author:   Fabien Marteau <fabien.marteau@armadeus.com>
# Created:  15/05/2008
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
__versionTime__ = "15/05/2008"
__author__ = "Fabien Marteau <fabien.marteau@armadeus.com>"

import periphondemand.bin.define
from   periphondemand.bin.define import *
from   periphondemand.bin.utils import Settings
from   periphondemand.bin.utils.error import Error

settings = Settings()

class TopGen:
    """ Generate Top component from a project
    """

    def __init__(self,project):
        self.project = project

    def generate(self):
        """ generate code for top component
        """
        ## checking if all intercons are done
        for masterinterface in self.project.getInterfaceMaster():
            try:
                self.project.getInstance(\
                        masterinterface.getParent().getInstanceName()\
                        +"_"\
                        +masterinterface.getName()\
                        +"_intercon")
            except Error,e:
                raise Error("Intercon missing:\n"+str(e),0)
        
        ########################
        # header
        out = self.header()
        ########################
        # entity
        entityname = "top_"+self.project.getName()
        portlist =  self.project.getPlatform().getConnectPortsList()
        out = out + self.entity(entityname,portlist)
        ########################
        # architecture head
        out = out + self.architectureHead(entityname)
        ########################
        # declare components
        out = out + self.declareComponents()
        ########################
        # declare signals
        incompleteportslist = self.project.getPlatform().getIncompleteExternalPortsList()        
        out = out + self.declareSignals(self.project.getInstancesList(),
                                                incompleteportslist)
        ########################
        # begin
        out = out + self.architectureBegin()
        ########################
        # declare Instance
        out =out+ self.declareInstance()
        #######################
        # instance connection
        out =out+ self.connectInstance(incompleteportslist)
        ########################
        # architecture foot
        out = out + self.architectureFoot(entityname)

        #######################
        # save file
        try:
            file = open(settings.projectpath+SYNTHESISPATH+\
                    "/top_"+ self.project.getName()+VHDLEXT,"w")
        except IOError, e:
            raise e
        file.write(out)
        file.close()
        return out
