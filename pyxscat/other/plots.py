import matplotlib.pyplot as plt
import matplotlib.colors as colors

from .other_functions import np_log, np_roi, np_weak_lims
from .units import *

def plot_image(data, title='', log=False, weak_lims=True):
    fig = plt.figure(figsize=(7,7), dpi=100)
    data = np_log(data, log)
    plt.imshow(data)
    plt.colorbar()
    plt.clim(np_weak_lims(data, weak_lims))
    plt.title(title)
    plt.show()

def plot_images_overlap(edf1_data, edf2_data, title='', log=False, weak_lims=True):
    edf1_data = np_log(edf1_data, log)
    edf2_data = np_log(edf2_data, log)
    plt.figure(
        frameon=False, 
        figsize=(5,5), 
    )

    im1 = plt.imshow(
        edf1_data, 
        cmap=plt.cm.gray, 
        interpolation='nearest',
    )

    plt.clim(
        np_weak_lims(
        edf1_data, 
        weak_lims,
        )
    )

    im2 = plt.imshow(
        edf2_data, 
        cmap=plt.cm.viridis, 
        alpha=0.9, 
        interpolation='bilinear',
    )

    plt.clim(
        np_weak_lims(
            edf2_data, 
            weak_lims
        )
    )
    plt.title(title)
    plt.show()


def plot_mesh(
    mesh_horz, 
    mesh_vert, 
    data, 
    unit='q_nm^-1', 
    auto_lims=True, 
    title='', 
    log=True, 
    colorbar=False,
    color_lims=[], 
    show=True,
    scatter_mode=False,
    **kwargs):
    """
    Plots the 2D Scattering map using pcolormesh method from matplotlib

    Parameters:
    mesh_horz(np.array) : 
    """
    DICT_PLOT = DICT_UNIT_PLOTS.get(unit, DICT_PLOT_DEFAULT)

    fig, ax = plt.subplots(figsize=(7,7), dpi=100, constrained_layout=True)
    ax.set_aspect('equal')

    try:
        if color_lims:
            if log:
                norm = colors.LogNorm(
                    vmax=color_lims[1],
                    vmin=color_lims[0],
                )
            else:
                norm = colors.Normalize(
                    vmax=color_lims[1],
                    vmin=color_lims[0],
                )
        else:
            norm = None
    except:
        norm = None



    if scatter_mode:
        try:
            plt.scatter(mesh_horz,mesh_vert,c=data,s=0.6, norm=norm, edgecolors="None", marker=",")
        except:
            return "Map could not be generated"

    else:
        try:
            plt.pcolormesh(
                mesh_horz,
                mesh_vert,
                data, 
                shading='nearest', 
                cmap='viridis',
                norm=norm,
            )
        except:
            return "Map could not be generated"

    if colorbar:
        plt.colorbar()

    plt.xlabel(kwargs.get('xlabel', DICT_PLOT['X_LABEL']), fontsize=20)
    plt.ylabel(kwargs.get('ylabel', DICT_PLOT['Y_LABEL']), fontsize=20)

    if not auto_lims:
        x_lims = kwargs.get('xlim', DICT_PLOT['X_LIMS'])
        if x_lims == '':
            x_lims = DICT_PLOT['X_LIMS']

        y_lims = kwargs.get('ylim', DICT_PLOT['Y_LIMS'])
        if y_lims == '':
            y_lims = DICT_PLOT['Y_LIMS']

        x_ticks = kwargs.get('xticks', DICT_PLOT['X_TICKS'])
        if x_ticks == '':
            x_ticks = DICT_PLOT['X_TICKS']

        y_ticks = kwargs.get('yticks', DICT_PLOT['Y_TICKS'])
        if y_ticks == '':
            y_ticks = DICT_PLOT['Y_TICKS']

        plt.xlim(x_lims)
        plt.ylim(y_lims)
        plt.xticks(x_ticks, fontsize=15)
        plt.yticks(y_ticks, fontsize=15)

    else:
        plt.xticks(ax.get_xticks(), fontsize=15)
        plt.yticks(ax.get_yticks(), fontsize=15)

    ax.tick_params(direction='out', length=6, width=2)
    plt.title(title)

    if show:
        plt.show()

