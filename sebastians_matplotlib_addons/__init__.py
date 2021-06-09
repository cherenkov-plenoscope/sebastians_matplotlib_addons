import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as plt_colors

FIGURE_16_9 = {"rows": 1080, "cols": 1920, "fontsize": 1}
FIGURE_4_3 = {"rows": 1080, "cols": 1440, "fontsize": 1}
FIGURE_1_1 = {"rows": 1080, "cols": 1080, "fontsize": 1}
FIGURE_2_1 = {"rows": 2*1080, "cols": 1080, "fontsize": 1}


def figure(style=FIGURE_16_9, dpi=240):
    scale = style["fontsize"]
    width_inch = style["cols"] / dpi
    height_inch = style["rows"] / dpi
    return plt.figure(
        figsize=(width_inch / scale, height_inch / scale), dpi=dpi * scale
    )


def close_figure(fig):
    plt.close(fig)


AXES_BLANK = {"spines": [], "axes": [], "grid": False}
AXES_MINIMAL = {"spines": ["left", "bottom"], "axes": ["x", "y"], "grid": True}
AXES_MATPLOTLIB = {"spines": ["left", "bottom", "right", "top"], "grid": False}


def add_axes(fig, span, style=AXES_MINIMAL):
    ax = fig.add_axes(span)

    for pos in ["left", "bottom", "right", "top"]:
        if pos in style["spines"]:
            ax.spines[pos].set_visible(True)
        else:
            ax.spines[pos].set_visible(False)

    if "x" in style["axes"]:
        ax.axes.get_xaxis().set_visible(True)
    else:
        ax.axes.get_xaxis().set_visible(False)

    if "y" in style["axes"]:
        ax.axes.get_yaxis().set_visible(True)
    else:
        ax.axes.get_yaxis().set_visible(False)

    if style["grid"]:
        ax_add_grid(ax)
    return ax


def ax_add_grid(ax):
    ax.grid(color="k", linestyle="-", linewidth=0.66, alpha=0.1)


def ax_add_circle(
    ax,
    x,
    y,
    r,
    linewidth=1.0,
    linestyle="-",
    color="k",
    alpha=1,
    num_steps=1000,
):
    phi = np.linspace(0, 2 * np.pi, num_steps)
    xs = x + r * np.cos(phi)
    ys = y + r * np.sin(phi)
    ax.plot(
        xs,
        ys,
        linewidth=linewidth,
        linestyle=linestyle,
        alpha=alpha,
        color=color,
    )


def ax_add_hatches(ax, ix, iy, x_bin_edges, y_bin_edges, alpha=0.1):
    x0 = x_bin_edges[ix]
    x1 = x_bin_edges[ix + 1]
    y0 = y_bin_edges[iy]
    y1 = y_bin_edges[iy + 1]
    ax.plot([x0, x1], [y0, y1], "-k", alpha=alpha)


def ax_add_histogram(
    ax,
    bin_edges,
    bincounts,
    linestyle="-",
    linecolor="k",
    linealpha=1.0,
    bincounts_upper=None,
    bincounts_lower=None,
    face_color=None,
    face_alpha=None,
):
    assert bin_edges.shape[0] == bincounts.shape[0] + 1
    for i, bincount in enumerate(bincounts):
        ax.plot(
            [bin_edges[i], bin_edges[i + 1]],
            [bincount, bincount],
            linestyle=linestyle,
            color=linecolor,
            alpha=linealpha,
        )
        if bincounts_upper is not None and bincounts_lower is not None:
            both_nan = np.isnan(bincounts_upper[i]) and np.isnan(
                bincounts_lower[i]
            )
            if not both_nan:
                ax.fill_between(
                    x=[bin_edges[i], bin_edges[i + 1]],
                    y1=[bincounts_lower[i], bincounts_lower[i]],
                    y2=[bincounts_upper[i], bincounts_upper[i]],
                    color=face_color,
                    alpha=face_alpha,
                    edgecolor="none",
                )
