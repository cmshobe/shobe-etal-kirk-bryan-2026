#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to create Figure 15 in the 2026 Kirk Bryan Field Trip guide (Shobe et al):
    plots changes to cross-section form on the South Platte River after 
    removal of the Lake George Diversion Dam

Created Spring 2026

@author: Charles Shobe, USFS Rocky Mountain Research Station
"""
import matplotlib

matplotlib.use('PS')
import numpy as np
import matplotlib.pyplot as plt



plt.rcParams['text.usetex'] = False

US3_x_common = np.load('cross_section_data/US3_x_common.npy') #1D array
US3_z_interp = np.load('cross_section_data/US3_z_interp.npy', allow_pickle = True) #dict containing arrays of all five surveys

DS1_x_common = np.load('cross_section_data/DS1_x_common.npy') #1D array
DS1_z_interp = np.load('cross_section_data/DS1_z_interp.npy', allow_pickle = True) #dict containing arrays of all five surveys

#note that the two x arrays are not the same

#2-panel plot: US3 on top, DS1 on bottom
fig, (ax1, ax2) = plt.subplots(2, 1, figsize = (8,6))

ibm_palette = ['#ffb000', '#fe6100', '#dc267f', '#785ef0', '#648fff']
colors = {'summer_2023': ibm_palette[0],
          'spring_2024': ibm_palette[1],
          'summer_2024': ibm_palette[2],
          'spring_2025': ibm_palette[3],
          'summer_2025': ibm_palette[4]}

colors = {'summer_2023': '0.0',
          'spring_2024': '0.2',
          'summer_2024': '0.4',
          'spring_2025': '0.6',
          'summer_2025': '0.8'}


#nb: to get at the arrays in the dictionary, unpack from the outer array structure with e.g. US3_z_interp[()]['key']
for label in colors:
    c = colors[label]
    ax1.plot(US3_x_common - min(US3_x_common), US3_z_interp[()][label] - 2417.7, color=c, lw=2, label=f"{label}")
    ax2.plot(DS1_x_common - min(DS1_x_common), DS1_z_interp[()][label] - 2417.8, color=c, lw=2, label=f"{label}")
    
handles, labels = ax1.get_legend_handles_labels()
new_labels = ['Summer 2023', 'Spring 2024', 
                     'Summer 2024', 'Spring 2025', 'Summer 2025']
ax1.legend(handles, new_labels, ncols = 1, 
           title_fontsize = 12, framealpha = 1,
           edgecolor = 'k', loc = 'lower right')

ax1.set_ylabel('Elevation above arbitrary\ncommon datum [m]', fontsize = 12)
ax1.set_ylim(0, 5.1)

ax2.set_xlabel('Distance from river-left benchmark [m]', fontsize = 12)
ax2.set_ylabel('Elevation above arbitrary\ncommon datum [m]', fontsize = 12)
ax2.set_ylim(0, 2)

ax1.text(0.005, 0.88, 'A: Upstream of the dam (former impoundment)', transform=ax1.transAxes, fontsize = 16, zorder = 10)
ax2.text(0.005, 0.88, 'B: Downstream of the dam', transform=ax2.transAxes, fontsize = 16, zorder = 10)

ax1.annotate('pre-removal impounded\nsediment surface', xy = (0.48, 0.8), xytext = (0.5, 0.55),
                   xycoords = 'axes fraction', fontsize = 12, ha = 'center',
                   va = 'center', 
                   bbox = dict(boxstyle='square', fc = 'none', color = 'none'),
                   arrowprops = dict(arrowstyle='->, widthB=2.5, lengthB=0.5', 
                                     lw = 2., color = 'k'))

ax2.annotate('', xy = (0.79, 0.38), xytext = (0.75, 0.8),
                   xycoords = 'axes fraction', fontsize = 12, ha = 'center',
                   va = 'center', 
                   bbox = dict(boxstyle='square', fc = 'none', color = 'none'),
                   arrowprops = dict(arrowstyle='->, widthB=2.5, lengthB=0.5', 
                                     lw = 2., color = 'k'))

ax2.annotate('bank reshaping (part of\npost-removal restoration)', xy = (0.87, 0.61), xytext = (0.75, 0.85),
                   xycoords = 'axes fraction', fontsize = 12, ha = 'center',
                   va = 'center', 
                   bbox = dict(boxstyle='square', fc = 'none', color = 'none'),
                   arrowprops = dict(arrowstyle='->, widthB=2.5, lengthB=0.5', 
                                     lw = 2., color = 'k'))

ax2.annotate('natural, post-removal\nbed incision', xy = (0.37, 0.3), xytext = (0.4, 0.55),
                   xycoords = 'axes fraction', fontsize = 12, ha = 'center',
                   va = 'center', 
                   bbox = dict(boxstyle='square', fc = 'none', color = 'none'),
                   arrowprops = dict(arrowstyle='->, widthB=2.5, lengthB=0.5', 
                                     lw = 2., color = 'k'))

fig.savefig('cross_section_examples.png', dpi=1000, bbox_inches = 'tight')
fig.savefig('cross_section_examples.eps', dpi=1000, bbox_inches = 'tight')