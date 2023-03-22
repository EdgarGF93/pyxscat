import matplotlib.pyplot as plt
from other_functions import np_log, np_roi, np_weak_lims

def plot_image(Edf_data, title='', log=False, weak_lims=True):
    fig = plt.figure(figsize=(7,7), dpi=100)
    data = np_log(Edf_data, log)
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