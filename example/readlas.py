#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 20:00:56 2022

@author: credger
"""

def readlas(fileName):
    import numpy as np
    import pandas as pd
    
    wellname, api, uwi, strt, stop, step, null, header, curves, units, data = (None,)*11  #Initialize outputs to None
       
    #Locate Sections of LAS file
    file = open(fileName,'r')
    section = []
    strtA, strtV, strtC, strtP, strtO = (None,)*5
    n = 0
    
    while(strtA == None):
        line = file.readline()
        if line.lstrip()[0:2] == '~V':  #lstrip removes leading whitepsace
            strtV = n
            section.append(['strtV', strtV])
        if line.lstrip()[0:2] == '~W':
            strtW = n
            section.append(['strtW', strtW])
        if line.lstrip()[0:2] == '~C':
            strtC = n
            section.append(['strtC', strtC])
        if line.lstrip()[0:2]== '~P':
            strtP = n
            section.append(['strtP', strtP])
        if line.lstrip()[0:2] == '~O':
            strtO = n
            section.append(['strtO', strtO])
        if line.lstrip()[0:2] == '~A':
            strtA = n
            section.append(['strtA', strtA])
        n = n+1
        
    positionV = [y[0] for y in section].index('strtV')
    endV = section[positionV+1][1]
    
    positionC = [y[0] for y in section].index('strtC')
    endC = section[positionC+1][1]
    
    positionW= [y[0] for y in section].index('strtW')
    endW = section[positionW+1][1]
    
    file.close()
    
    #Well Information
    file = open(fileName, 'r')
    lines = file.readlines()[strtW:endW]
    
    for line in lines:
        if 'STRT' in line.replace(" ", "")[0:5]:
            delimeter1 = line.find('.')
            delimeter2 = line[delimeter1:].find(' ')
            delimeter3 = line.find(':')
            strt = float(line[(delimeter1+delimeter2):delimeter3])
            
        if 'STOP' in line.replace(" ", "")[0:5]:
            delimeter1 = line.find('.')
            delimeter2 = line[delimeter1:].find(' ')
            delimeter3 = line.find(':')
            stop = float(line[(delimeter1+delimeter2):delimeter3])
            
        if 'STEP' in line.replace(" ", "")[0:5]:
            delimeter1 = line.find('.')
            delimeter2 = line[delimeter1:].find(' ')
            delimeter3 = line.find(':')
            step = float(line[(delimeter1+delimeter2):delimeter3])
            
        if 'NULL' in line.replace(" ", "")[0:5]:
            delimeter1 = line.find('.')
            delimeter2 = line[delimeter1:].find(' ')
            delimeter3 = line.find(':')
            null = float(line[(delimeter1+delimeter2):delimeter3])
        
        if 'API' in line.replace(" ", "")[0:5]:
            delimeter1 = line.find('.')
            delimeter2 = line[delimeter1:].find(' ')
            delimeter3 = line.find(':')
            api = line[delimeter1+delimeter2:delimeter3].replace(" ", "").replace("-", "")
            if api == 'APINUMBER':
                api = line[(delimeter3+1):].replace(" ", "").replace("-", "")
                
        if 'UWI' in line.replace(" ", "")[0:5]:
            delimeter1 = line.find('.')
            delimeter2 = line[delimeter1:].find(' ')
            delimeter3 = line.find(':')
            api = line[delimeter1+delimeter2:delimeter3].replace(" ", "").replace("-", "")
            if uwi == 'UNIQUEWELLID':
                uwi = line[(delimeter3+1):].replace(" ", "").replace("-", "")
                
        if 'WELL' in line.replace(" ", "")[0:5]:
            delimeter1 = line.find('.')
            delimeter2 = line[delimeter1:].find(' ')
            delimeter3 = line.find(':')
            wellname = line[(delimeter1+delimeter2):delimeter3].lstrip().rstrip()
            if wellname.replace(" ", "") == 'WELL':
                wellname = line[(delimeter3+1):].lstrip().rstrip()
    file.close()
    
    #Header
    file = open(fileName, 'r')
    header = file.readlines()[0:strtA]
    
    #Curve Names
    file = open(fileName, 'r')
    lines = file.readlines()[strtC:endC]
    curves = []
    for line in lines:
        if len(lines) == 0:
            continue
        if line[0] == '~':
            continue
        if line[0] == '#':
            continue
        else:
            delimeter1 = line.find('.')
            mnem = line[0:delimeter1].replace(" ", "")
            curves.append(mnem)
    file.close()
    
    #units
    file = open(fileName, 'r')
    lines = file.readlines()[strtC:endC]
    units = []
    for line in lines:
        if len(line) == 0:
            continue
        if line[0] == '~':
            continue
        if line[0] == '#':
            continue
        else:
            delimeter1 = line.find('.')
            delimeter2 = line[delimeter1:].find(' ')
            if delimeter2 == -1:  #for special case of no space after unit
                unit = line[(delimeter1+1):]
            else:
                unit = line[delimeter1:(delimeter1+delimeter2)].replace(".", "")
        units.append(unit)
    file.close()
    
    #Data
    file = open(fileName, 'r')
    lines = file.readlines()[(strtA+1):]
    ncurves = len(curves)
    cols = ncurves
    rows = len(lines)
    M = np.empty([rows,cols])
    r = 0
    c = 0
    
    for line in lines:
        for n in line.split():
            M[r,c] = float(n)
            c = c+1
            if c == ncurves:
                r = r+1
                c = 0
    file.close()
    
    data = pd.DataFrame(M)
    data.columns = curves
    
    readlas.wellname = wellname
    readlas.api = api
    readlas.uwi = uwi
    readlas.strt = strt
    readlas.stop = stop
    readlas.step = step
    readlas.null = null
    readlas.header = header
    readlas.curves = curves
    readlas.units = units
    readlas.data = data
    
    print('Use object attribute syntax to access outputs (e.g. readlas.wellname)')
    print()
    print('Available outputs: wellname, api, uwi, strt, stop, step, null, header, curves, units, data')
    print()
  
    return
