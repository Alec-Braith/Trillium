"""
Utilities used by example notebooks
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

def plot_image(image, factor=1.0, clip_range = None, **kwargs):
    """
    Utility function for plotting RGB images.
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))
    if clip_range is not None:
        ax.imshow(np.clip(image * factor, *clip_range), **kwargs)
    else:
        ax.imshow(image * factor, **kwargs)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()


def plot_animation(images, factor=1.0, clip_range = None, **kwargs):
    """
    Utility function for plotting RGB images in an animation/gif.
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))
    ax.set_xticks([])
    ax.set_yticks([])

    def animation_frame(i):
        ax.imshow(np.clip(images[i] * factor, *clip_range))
        ax.imshow(images[i] * factor)
        return images[i]

    animation = FuncAnimation(fig, func = animation_frame)
    plt.show()