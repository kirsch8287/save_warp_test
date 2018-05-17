# -*- coding: utf-8 -*-

"""
fielddata module test version

Created on Thu May 17 2018

@author: K. Yoo, 
Intense Beam and Accelerator Laboratory(IBAL), 
Ulsan National Institute of Science and Technology(UNIST),
Republic of Korea
"""

# ========================================================================== #
#                        Module for Saving Field Data                        #
# -------------------------------------------------------------------------- #
#                                                                            #
# 1. Electric Potnetial data from WARP [ 1D, 2D, 3D / xyz geometry ]         #
#                                                                            #
# ========================================================================== #

"""
First, to use this module, it may be convinient locating this file 
at the same directory with WARP scripts.
And, this module must be imported in the scripts.
< e.g. "import fielddata as fd" >
"""

import os
import numpy as np

from warp import *
from pyevtk.hl import gridToVTK


# -------------------------------------------------------------------------- #

def phi_1d_xyz(direction=None, ts=None, dirName="E_potential_1d_data", 
               fileName="E_potential_data", delim="\t",
               xx=0, yy=0, zz=0):
    """ 
This function exports electric potential data 1D of XYZ geomtrey.
Electric potential data includes position (x,y,z) and potential (phi)
Arguments are following;
 - direction: Exported electric potential will be along this direction.
              < "x", "y", "z" >
 - ts: All electric potential data will be saved when the time-step is 'ts'
         < e.g. ts=[100, 200] >
 - dirName: Potential data will be saved in the directory having this name.
            {Default="E_potential_data"}
 - fileName: Potential data at each z-position will be saved in the file 
             having the name of 'fileName_time-step.txt'.
             {Default="E_potential_data"}
             < e.g. E_potential_data_100.txt, at time-step=100 >
 - delim: Each components of data will be separated with 
          this delimiter in .txt file.
          {Default="\t"  (tab)}
 - xx: All electric potential data will be saved where the x-position is 'xx' 
       when the direction is not "x".
       This must be the grid number.
       {Default=0}
 - yy: All electric potential data will be saved where the y-position is 'yy' 
       when the direction is not "y".
       This must be the grid number.
       {Default=0}
 - zz: All electric potential data will be saved where the z-position is 'zz' 
       when the direction is not "z".
       This must be the grid number.
       {Default=0}
    """
    assert direction is not None, ValueError(
            'Dimension is not defined for data')
    assert ts is not None, ValueError(
            'Time-step is not defined for data')
    assert direction=="x" or direction=="y" or direction=="z", ValueError(
            'Direction must be one of "x", "y", and "z"')
    assert isinstance(ts, list) is True, ValueError(
            'Time-step must be given by the list type')
    assert isinstance(dirName, str) is True, ValueError(
            'Directory name must be given by the string type')
    assert isinstance(fileName, str) is True, ValueError(
            'File name must be given by the string type')
    @callfromafterstep
    def save_1d_data():
        for j in range(len(ts)):
            if top.it == ts[j]:
                phi_1d_dir = './{dirName}/'.format(dirName=dirName)
                if not os.path.exists(phi_1d_dir):
                    os.mkdir(phi_1d_dir)
                tsWriteFile = open("./{dirName}/{fileName}_{ts}_ts.txt".
                         format(dirName=dirName, fileName=fileName, 
                                ts=ts[j]), "w")
                if direction == "x":
                    tsWriteFile.write("x(m){de}phi(V)".format(de=delim))
                    for i in range(w3d.nx + 1):
                        xpos = i * w3d.dx + w3d.xmmin
                        pp = getphi(ix=i, iy=yy, iz=zz)
                        tsWriteFile.write("\n")
                        tsWriteFile.write("{xpos:.9f}{de}{phi:.9f}".format(
                                xpos=xpos, de=delim, phi=pp))
                    tsWriteFile.close()
                elif direction == "y":
                    tsWriteFile.write("y(m){de}phi(V)".format(de=delim))
                    for i in range(w3d.ny + 1):
                        ypos = i * w3d.dy + w3d.ymmin
                        pp = getphi(ix=xx, iy=i, iz=zz)
                        tsWriteFile.write("\n")
                        tsWriteFile.write("{ypos:.9f}{de}{phi:.9f}".format(
                                ypos=ypos, de=delim, phi=pp))
                    tsWriteFile.close()
                elif direction == "z":
                    tsWriteFile.write("z(m){de}phi(V)".format(de=delim))
                    for i in range(w3d.nz + 1):
                        zpos = i * w3d.dz + w3d.zmmin
                        pp = getphi(ix=xx, iy=yy, iz=i)
                        tsWriteFile.write("\n")
                        tsWriteFile.write("{zpos:.9f}{de}{phi:.9f}".format(
                                zpos=zpos, de=delim, phi=pp))
                    tsWriteFile.close()

# -------------------------------------------------------------------------- #


# -------------------------------------------------------------------------- #

def phi_2d_xyz(plane=None, ts=None, dirName="E_potential_2d_data", 
               fileName="E_potential_data", delim="\t",
               xx=0, yy=0, zz=0):
    """ 
This function exports electric potential data 2D of XYZ geomtrey.
Electric potential data includes position (x,y,z) and potential (phi)
Arguments are following;
 - plane: Exported electric potential will be on this plane.
          < "xy", "yz", "zx" >
 - ts: All electric potential data will be saved when the time-step is 'ts'
         < e.g. ts=[100, 200] >
 - dirName: Potential data will be saved in the directory having this name.
            {Default="E_potential_data"}
 - fileName: Potential data at each z-position will be saved in the file 
             having the name of 'fileName_time-step.txt'.
             {Default="E_potential_data"}
             < e.g. E_potential_data_100.txt, at time-step=100 >
 - delim: Each components of data will be separated with 
          this delimiter in .txt file.
          {Default="\t"  (tab)}
 - xx: All electric potential data will be saved where the x-position is 'xx' 
       when the plane is "yz".
       This must be the grid number.
       {Default=0}
 - yy: All electric potential data will be saved where the y-position is 'yy' 
       when the plane is "zx".
       This must be the grid number.
       {Default=0}
 - zz: All electric potential data will be saved where the z-position is 'zz' 
       when the plane is "xy".
       This must be the grid number.
       {Default=0}
    """
    assert plane is not None, ValueError(
            'Plane is not defined for data')
    assert ts is not None, ValueError(
            'Time-step is not defined for data')
    assert plane=="xy" or plane=="yz" or plane=="zx", ValueError(
            'Plane must be one of "xy", "yz", and "zx"')
    assert isinstance(ts, list) is True, ValueError(
            'Time-step must be given by the list type')
    assert isinstance(dirName, str) is True, ValueError(
            'Directory name must be given by the string type')
    assert isinstance(fileName, str) is True, ValueError(
            'File name must be given by the string type')
    @callfromafterstep
    def save_2d_data():
        for j in range(len(ts)):
            if top.it == ts[j]:
                phi_2d_dir = './{dirName}/'.format(dirName=dirName)
                if not os.path.exists(phi_2d_dir):
                    os.mkdir(phi_2d_dir)
                tsWriteFile = open("./{dirName}/{fileName}_{ts}_ts.txt".
                         format(dirName=dirName, fileName=fileName, 
                                ts=ts[j]), "w")
                if plane == "xy":
                    tsWriteFile.write(
                            "x(m){de}y(m){de}phi(V)".format(de=delim))
                    for i in range(w3d.nx + 1):
                        for k in range(w3d.ny + 1):
                            xpos = i * w3d.dx + w3d.xmmin
                            ypos = k * w3d.dy + w3d.ymmin
                            pp = getphi(ix=i, iy=k, iz=zz)
                            tsWriteFile.write("\n")
                            tsWriteFile.write(
                                    "{xpos:.9f}{de}{ypos:.9f}{de}{phi:.9f}".\
                                    format(xpos=xpos, ypos=ypos, 
                                           de=delim, phi=pp))
                    tsWriteFile.close()
                elif plane == "yz":
                    tsWriteFile.write(
                            "y(m){de}z(m){de}phi(V)".format(de=delim))
                    for i in range(w3d.ny + 1):
                        for k in range(w3d.nz + 1):
                            ypos = i * w3d.dy + w3d.ymmin
                            zpos = k * w3d.dz + w3d.zmmin
                            pp = getphi(ix=xx, iy=i, iz=k)
                            tsWriteFile.write("\n")
                            tsWriteFile.write(
                                    "{ypos:.9f}{de}{zpos:.9f}{de}{phi:.9f}".\
                                    format(ypos=ypos, zpos=zpos, 
                                           de=delim, phi=pp))
                    tsWriteFile.close()
                elif plane == "zx":
                    tsWriteFile.write(
                            "z(m){de}x(m){de}phi(V)".format(de=delim))
                    for i in range(w3d.nz + 1):
                        for k in range(w3d.nx + 1):
                            zpos = i * w3d.dz + w3d.zmmin
                            xpos = k * w3d.dx + w3d.xmmin
                            pp = getphi(ix=k, iy=yy, iz=i)
                            tsWriteFile.write("\n")
                            tsWriteFile.write(
                                    "{zpos:.9f}{de}{xpos:.9f}{de}{phi:.9f}".\
                                    format(zpos=zpos, xpos=xpos, 
                                           de=delim, phi=pp))
                    tsWriteFile.close()
                            
# -------------------------------------------------------------------------- #


# -------------------------------------------------------------------------- #

def phi_3d_xyz(ts=None, dirName="E_potential_3d_data", 
               fileName="E_potential_data", delim="\t"):
    """ 
This function exports electric potential data 3D of XYZ geomtrey.
Electric potential data includes position (x,y,z) and potential (phi)
Arguments are following;
 - ts: All electric potential data will be saved when the time-step is 'ts'
         < e.g. ts=[100, 200] >
 - dirName: Potential data will be saved in the directory having this name.
            {Default="E_potential_data"}
 - fileName: Potential data at each z-position will be saved in the file 
             having the name of 'fileName_time-step.txt'.
             {Default="E_potential_data"}
             < e.g. E_potential_data_100.txt, at time-step=100 >
 - delim: Each components of data will be separated with 
          this delimiter in .txt file.
          {Default="\t"  (tab)}
    """
    assert ts is not None, ValueError(
            'Time-step is not defined for data')
    assert isinstance(ts, list) is True, ValueError(
            'Time-step must be given by the list type')
    assert isinstance(dirName, str) is True, ValueError(
            'Directory name must be given by the string type')
    assert isinstance(fileName, str) is True, ValueError(
            'File name must be given by the string type')
    @callfromafterstep
    def save_3d_data():
        for j in range(len(ts)):
            if top.it == ts[j]:
                phi_3d_dir = './{dirName}/'.format(dirName=dirName)
                if not os.path.exists(phi_3d_dir):
                    os.mkdir(phi_3d_dir)
                tsWriteFile = open("./{dirName}/{fileName}_{ts}_ts.txt".
                         format(dirName=dirName, fileName=fileName, 
                                ts=ts[j]), "w")
                tsWriteFile.write(
                            "x(m){de}y(m){de}z(m){de}phi(V)".format(de=delim))
                for i in range(w3d.nx + 1):
                    for k in range(w3d.ny + 1):
                        for m in range(w3d.ny + 1):
                            xpos = i * w3d.dx + w3d.xmmin
                            ypos = k * w3d.dy + w3d.ymmin
                            zpos = m * w3d.dz + w3d.zmmin
                            pp = getphi(ix=i, iy=k, iz=m)
                            tsWriteFile.write("\n")
                            tsWriteFile.write("{xpos:.9f}{de}{ypos:.9f}{de}".\
                                              format(xpos=xpos, ypos=ypos, 
                                                     de=delim, phi=pp))
                            tsWriteFile.write("{zpos:.9f}{de}{phi:.9f}".\
                                              format(zpos=zpos, de=delim, 
                                                     phi=pp))
                                    
                tsWriteFile.close()

# -------------------------------------------------------------------------- #


# -------------------------------------------------------------------------- #

