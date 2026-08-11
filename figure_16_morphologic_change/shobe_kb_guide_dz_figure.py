#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to create Figure 16 in the 2026 Kirk Bryan Field Trip guide (Shobe et al):
    plots average morphologic change at nine river cross-sections on the South 
    Platte River after removal of the Lake George Diversion Dam

Created Spring 2026

@author: Charles Shobe, USFS Rocky Mountain Research Station
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_parquet('dz_data/fieldguide_dz_data.parquet')
data['category'] = data['reach'].str[:-2]

ibm_palette = ['#ffb000', '#fe6100', '#dc267f', '#785ef0']


##############trying a plot over time; may be more intuitive to understand

fig, (ax1, ax2) = plt.subplots(2, 1, figsize = (8,6))
fig.subplots_adjust(hspace = 0.1)
iter = 0
ibm_palette_3by3 = ['#ffb000', '#fe6100', '#785ef0'] * 3
ibm_palette_3by3 = ['0.0', '0.4', '0.8'] * 3
for r in sorted(data["reach"].unique()):
    sub = data[data["reach"] == r].copy()
    ys = sub['ΔC_mean_Δz_m'].to_numpy().astype(float)
    if sub.iloc[0]['category'] == 'control':
        linestyle = ':'
        marker = '+'
    elif sub.iloc[0]['category'] == 'upstream':
        linestyle = '-'
        marker = 'o'
    elif sub.iloc[0]['category'] == 'downstream':
        linestyle = '--'
        marker = 's'
    
    color = ibm_palette_3by3[iter]
    iter += 1
    ax1.plot(np.arange(4), ys, marker=marker, lw=2, label=r, linestyle = linestyle,
            color = color)
    ax2.plot(np.arange(4), ys, marker=marker, lw=2, label=r, linestyle = linestyle,
            color = color)

ax1.set_ylim(-2.1, 0.2)
ax2.set_ylim(-0.2, 0.1)

ax1.set_xticks(np.arange(4))
ax1.set_xticklabels([])
ax1.set_ylabel(r'Average elevation change $\overline{\Delta z}$ [m]', fontsize = 12)
ax1.yaxis.set_label_coords(-0.08, 0)

ax2.set_xlabel('Time interval', fontsize = 12)
ax2.set_xticks(np.arange(4))
ax2.set_xticklabels(['Summer 2023 -\nSpring 2024\n(removal + low flow)', 'Spring 2024 -\nSummer 2024\n(high spring flow)', 
                     'Summer 2024 -\nSpring 2025\n(low flow)', 'Spring 2025 -\nSummer 2025\n(low spring flow)'])

ax2.axhline(y = 0, linewidth = 2, color = 'darkgray', zorder = 0)

handles, labels = ax1.get_legend_handles_labels()
handles_reorder = handles[:]
handles_reorder[3:6] = handles[6:]
handles_reorder[6:] = handles[3:6]
new_labels = ['Control U', 'Control M', 'Control D',
              'Upstream U', 'Upstream M', 'Upstream D',
              'Downstream U', 'Downstream M', 'Downstream D']
ax1.legend(handles_reorder, new_labels, ncols = 3, title = 'Cross-section', 
           title_fontsize = 12, framealpha = 1,
           edgecolor = 'k', loc = 'lower right')

ax1.text(0.005, 0.88, 'A', transform=ax1.transAxes, fontsize = 20, zorder = 10)
ax2.text(0.005, 0.88, 'B', transform=ax2.transAxes, fontsize = 20, zorder = 10)


fig.savefig('average_elevation_change_over_time.png', dpi=1000, bbox_inches = 'tight')
fig.savefig('average_elevation_change_over_time.eps', dpi=1000, bbox_inches = 'tight')