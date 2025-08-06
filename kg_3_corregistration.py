# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 17:48:35 2015

@author: takeiyuichi
"""

import os
import sys

import mne


if __name__ == '__main__':
    from mne.commands.utils import get_optparser
    
    parser = get_optparser(__file__)
    options, args = parser.parse_args()
    
    os.environ['ETS_TOOLKIT'] = 'qt4'
    mne.gui.coregistration()
    sys.exit(0)
