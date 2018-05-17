# -*- coding: utf-8 -*-

"""
saveparticledata module alpha version

Created on Thu May 3 2018

@author: K. Yoo, 
Intense Beam and Accelerator Laboratory(IBAL), 
Ulsan National Institute of Science and Technology(UNIST),
Republic of Korea
"""

# ========================================================================== #
#                      Module for Saving Particle Data                       #
# -------------------------------------------------------------------------- #
#                                                                            #
# 1. Particle data by ZCrossingParticles in WARP                             #
# 2. Particle data at specific time-step                                     #
# 3. Particle data at specific time-step with vtk format for ParaView        #
#                                                                            #
# ========================================================================== #

"""
First, to use this module, it may be convinient locating this file 
at the same directory with WARP scripts.
And, this module must be imported in the scripts.
< e.g. "import saveparticledata as spd" >
"""

import os
import numpy as np

from warp import *
from warp.particles.extpart import ZCrossingParticles
from pyevtk.hl import pointsToVTK

      
# -------------------------------------------------------------------------- #

def zcross_data(
        zPos=None, dirName="zposition_particle_data", 
        fileName="z_particle_data", delim="\t", ts=None):
    """
This function exports particle data 'ZCrossingParticles' in WARP.
Particle data includes position (x,y,z) and velocity (vx, vy, vz)
Arguments are following;
 - zPos: This is the list including all z-Positions to want to collect 
         particle data. 
         < e.g. zPos=[100.*mm, 200.*mm] >
 - dirName: Partilce data will be saved in the directory having this name 
            {Default="zposition_particle_data"}
 - fileName: Partilce data at each z-position will be saved in the file 
             having the name of 'fileName_z-position.txt'
             {Default="z_particle_data"}
             < e.g. z_particle_data_0.5m.txt, at z=0.5m >
 - delim: Each components of particle data will be separated with 
          this delimiter in .txt file
          {Default="\t"  (tab)}
 - ts: All particle data will be saved when the time-step is 'ts'
    """
    assert zPos is not None, ValueError(
            'z position is not defined for data')
    assert isinstance(zPos, list) is True, ValueError(
            'z position must be given by the list type')
    assert isinstance(dirName, str) is True, ValueError(
            'Directory name must be given by the string type')
    assert isinstance(fileName, str) is True, ValueError(
            'File name must be given by the string type')
    assert ts is not None, ValueError(
            'Time-step is not defined for data')
    nZPos = len(zPos)
    zPartData = []
    for i in range(nZPos):
        zPartData.append(ZCrossingParticles(zz=zPos[i], laccumulate=1))
    @callfromafterstep
    def savezposdata():
        if top.it == ts:
            zPartDir = './{dirName}/'.format(dirName=dirName)
            if not os.path.exists(zPartDir):
                os.mkdir(zPartDir)
            for i in range(nZPos):
                zWriteFile = open("./{dirName}/{fileName}_{zPos}m.txt".\
                                  format(dirName=dirName, fileName=fileName, 
                                         zPos=zPos[i]), "w")
                zHeaders = \
                "pid{de}x(m){de}y(m){de}t(s){de}vx(m/s){de}vy(m/s){de}vz(m/s)".\
                    format(de=delim)
                zWriteFile.write(zHeaders)
                znn = zPartData[i].getn()
                zid = zPartData[i].getpid()
                zxx = zPartData[i].getx()
                zyy = zPartData[i].gety()
                ztt = zPartData[i].gett()
                zvx = zPartData[i].getvx()
                zvy = zPartData[i].getvy()
                zvz = zPartData[i].getvz()
                for j in range(znn):
                    zWriteFile.write("\n")
                    zWriteFile.write("{pid}{de}".format(
                            pid=zid[j], de=delim))
                    zWriteFile.write("{xpos:.9f}{de}".format(
                            xpos=zxx[j], de=delim))
                    zWriteFile.write("{ypos:.9f}{de}".format(
                            ypos=zyy[j], de=delim))
                    zWriteFile.write("{tof}{de}".format(
                            tof=ztt[j], de=delim))
                    zWriteFile.write("{vx}{de}".format(
                            vx=zvx[j], de=delim))
                    zWriteFile.write("{vy}{de}".format(
                            vy=zvy[j], de=delim))
                    zWriteFile.write("{vz}".format(
                            vz=zvz[j]))
                zWriteFile.close()
                
# -------------------------------------------------------------------------- #


# -------------------------------------------------------------------------- #

def ts_data(
        part=None, ts=None, dirName="timestep_particle_data", 
        fileName="time_particle_data", delim="\t"):
    """
This function exports particle data at specific time-step.
Particle data includes position (x,y,z) and velocity (vx, vy, vz)
Arguments are following;
 - part: This is the particle species.
 - ts: This is the list including all time-step to want to collect 
         particle data. 
         < e.g. ts=[100, 200] >
 - dirName: Partilce data will be saved in the directory having this name 
            {Default="timestep_particle_data"}
 - fileName: Partilce data at each time-step will be saved in the file 
             having the name of 'fileName_time-step.txt'
             {Default="time_particle_data"}
             < e.g. time_particle_data_100_ts.txt, at time-step=100 >
 - delim: Each components of particle data will be separated with 
          this delimiter in .txt file
          {Default="\t"  (tab)}
    """
    assert part is not None, ValueError(
            'Particle species is not defined for data')
    assert ts is not None, ValueError(
            'Time-step is not defined for data')
    assert isinstance(ts, list) is True, ValueError(
            'Time-step must be given by list type')
    assert isinstance(dirName, str) is True, ValueError(
            'Directory name must be given by string type')
    assert isinstance(fileName, str) is True, ValueError(
            'File name must be given by string type')
    nTs = len(ts)
    @callfromafterstep
    def savetsdata():
        for i in range(nTs):
            if top.it == ts[i]:
                tsPartDir = './{dirName}/'.format(dirName=dirName)
                if not os.path.exists(tsPartDir):
                    os.mkdir(tsPartDir)
                tsWriteFile = open("./{dirName}/{fileName}_{ts}_ts.txt".
                         format(dirName=dirName, fileName=fileName, 
                                ts=ts[i]), "w")
                tsHeaders = \
                "x(m){de}y(m){de}z(m){de}vx(m/s){de}vy(m/s){de}vz(m/s)".\
                    format(de=delim)
                tsWriteFile.write(tsHeaders)
                tsn = part.getn()
                tsx = part.getx()
                tsy = part.gety()
                tsz = part.getz()
                tsvx = part.getvx()
                tsvy = part.getvy()
                tsvz = part.getvz()
                for j in range(tsn):
                    tsWriteFile.write("\n")
                    tsWriteFile.write("{xpos:.9f}{de}".format(
                            xpos=tsx[j], de=delim))
                    tsWriteFile.write("{ypos:.9f}{de}".format(
                            ypos=tsy[j], de=delim))
                    tsWriteFile.write("{zpos:.9f}{de}".format(
                            zpos=tsz[j], de=delim))
                    tsWriteFile.write("{vx}{de}".format(
                            vx=tsvx[j], de=delim))
                    tsWriteFile.write("{vy}{de}".format(
                            vy=tsvy[j], de=delim))
                    tsWriteFile.write("{vz}".format(
                            vz=tsvz[j]))
                tsWriteFile.close()
                
# -------------------------------------------------------------------------- #


# -------------------------------------------------------------------------- #

def vtk_data(part=None, tsstart=None, tsend=None, tsint=1, 
                  dirName="vtk_particle_data", 
                  fileName="vtk_particle_data"):
    """
This function exports particle data at specific time-step with vtk format 
for ParaView.
Particle data includes position (x,y,z)
Arguments are following;
 - part: This is the particle species.
 - tsstart: This is time-step to want to start collecting particle data. 
 - tsend: This is time-step to want to end collecting particle data. 
 - tsint: This is the interval of time-step to collect particle data. 
          {Default=1}
 - dirName: Partilce data will be saved in the directory having this name 
            {Default="vtk_particle_data"}
 - fileName: Partilce data at each time-step will be saved in the file 
             having the name of 'fileName_time-step.vtu'
             {Default="vtk_particle_data"}
             < e.g. vtk_particle_data_100.vtu, at time-step=100 >
    """
    assert part is not None, ValueError(
            'Particle species is not defined for data')
    assert tsstart is not None, ValueError(
            'Time-step for start is not defined for data')
    assert tsend is not None, ValueError(
            'Time-step for end is not defined for data')
    assert isinstance(dirName, str) is True, ValueError(
            'Directory name must be given by string type')
    assert isinstance(fileName, str) is True, ValueError(
            'File name must be given by string type')
    @callfromafterstep
    def vtkdata():
        if tsstart <= top.it <= tsend:
            if top.it % tsint == 0:
                vtkPartDir = './{dirName}/'.format(dirName=dirName)
                if not os.path.exists(vtkPartDir):
                    os.mkdir(vtkPartDir)
                nnn = part.getn()
                xxx = part.getx()
                yyy = part.gety()
                zzz = part.getz()
                val = [1 for i in range(nnn)]
                npval = np.array(val)
                pointsToVTK("./{dirName}/{fileName}_{ts}_ts".\
                            format(dirName=dirName, fileName=fileName, 
                                   ts=top.it), 
                            xxx, yyy, zzz,data={"particle" : npval})
                            
# -------------------------------------------------------------------------- #
