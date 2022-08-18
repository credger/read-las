#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 12:32:04 2022

@author: credger
"""

from readlas import readlas
fileName = '1046076476.las'
readlas(fileName)

print('wellname: ', readlas.wellname)
print('api: ', readlas.api)
print(readlas.data)