from .version import __version__
import numpy as np
import matplotlib
import warnings


matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as plt_colors
import matplotlib.patches as plt_patches


from . import hemisphere
from . import pseudo3d
from . import video

FIGURE_16_9 = {"rows": 1080, "cols": 1920, "fontsize": 1}
FIGURE_4_3 = {"rows": 1080, "cols": 1440, "fontsize": 1}
FIGURE_1_1 = {"rows": 1080, "cols": 1080, "fontsize": 1}
FIGURE_2_1 = {"rows": 2 * 1080, "cols": 1080, "fontsize": 1}


def figure(style=FIGURE_16_9, dpi=240):
    scale = style["fontsize"]
    width_inch = style["cols"] / dpi
    height_inch = style["rows"] / dpi
    return plt.figure(
        figsize=(width_inch / scale, height_inch / scale), dpi=dpi * scale
    )


def close(fig):
    plt.close(fig)


AXES_BLANK = {"spines": [], "axes": [], "grid": False}
AXES_MINIMAL = {"spines": ["left", "bottom"], "axes": ["x", "y"], "grid": True}
AXES_MATPLOTLIB = {
    "spines": ["left", "bottom", "right", "top"],
    "axes": ["x", "y"],
    "grid": False,
}


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


def ax_add_grid(ax, add_minor=False):
    which = "both" if add_minor else "major"
    ax.grid(color="grey", linestyle="-", linewidth=0.33, which=which)


def ax_add_grid_with_explicit_ticks(
    ax,
    xticks,
    yticks,
    color="grey",
    linestyle="-",
    linewidth=0.33,
    alpha=1,
):
    for ytick in yticks:
        ax.axhline(
            y=ytick,
            xmin=0,
            xmax=1,
            color=color,
            linestyle=linestyle,
            linewidth=linewidth,
            alpha=alpha,
        )
    for xtick in xticks:
        ax.axvline(
            x=xtick,
            ymin=0,
            ymax=1,
            color=color,
            linestyle=linestyle,
            linewidth=linewidth,
            alpha=alpha,
        )


def ax_add_circle(
    ax,
    x,
    y,
    r,
    num_steps=1000,
    **kwargs,
):
    phi = np.linspace(0, 2 * np.pi, num_steps)
    xs = x + r * np.cos(phi)
    ys = y + r * np.sin(phi)
    ax.plot(
        xs,
        ys,
        **kwargs,
    )


def ax_add_pie_slice(
    ax,
    x=0,
    y=0,
    phi_start_rad=0,
    phi_stop_rad=0.5 * np.pi,
    radius=1,
    num_steps=100,
    **kwargs,
):
    points = [(0, 0)]
    for phi_rad in np.linspace(phi_start_rad, phi_stop_rad, num_steps):
        point = (x + radius * np.cos(phi_rad), y + radius * np.sin(phi_rad))
        points.append(point)
    points = np.asarray(points)
    p = plt_patches.Polygon(points, **kwargs)
    ax.add_patch(p)


def ax_add_hexagon(ax, x, y, r_outer, orientation_deg=0.0, **kwargs):
    xx = np.zeros(7)
    yy = np.zeros(7)
    ori = np.deg2rad(orientation_deg)
    for i, phi in enumerate(np.linspace(0.0, 2.0 * np.pi, 7)):
        _x = x + np.cos(phi + ori) * r_outer
        _y = y + np.sin(phi + ori) * r_outer
        xx[i] = _x
        yy[i] = _y
    ax.plot(xx, yy, **kwargs)


def ax_add_hatches(
    ax,
    ix,
    iy,
    x_bin_edges,
    y_bin_edges,
    linestyle="-",
    color="black",
    alpha=0.1,
    **kwargs,
):
    x0 = x_bin_edges[ix]
    x1 = x_bin_edges[ix + 1]
    y0 = y_bin_edges[iy]
    y1 = y_bin_edges[iy + 1]
    ax.plot(
        [x0, x1],
        [y0, y1],
        color=color,
        linestyle=linestyle,
        alpha=alpha,
        **kwargs,
    )


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
    label=None,
    draw_bin_walls=False,
):
    assert bin_edges.shape[0] == bincounts.shape[0] + 1
    for i, bincount in enumerate(bincounts):
        ax.plot(
            [bin_edges[i], bin_edges[i + 1]],
            [bincount, bincount],
            linestyle=linestyle,
            color=linecolor,
            alpha=linealpha,
            label=label if i == 0 else None,
        )
        if draw_bin_walls and i + 1 < bincounts.shape[0]:
            ax.plot(
                [bin_edges[i + 1], bin_edges[i + 1]],
                [bincounts[i], bincounts[i + 1]],
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
                    linewidth=0.0,
                )


def ax_add_box(ax, xlim, ylim, **kwargs):
    """
    Draw a rectangular box in xlim, ylim to ax.
    """
    #  __
    # |  |
    ax.plot([xlim[0], xlim[1]], [ylim[0], ylim[0]], **kwargs)
    #  __
    # |__
    ax.plot([xlim[1], xlim[1]], [ylim[0], ylim[1]], **kwargs)
    #
    # |__|
    ax.plot([xlim[0], xlim[1]], [ylim[1], ylim[1]], **kwargs)
    #  __
    #  __|
    ax.plot([xlim[0], xlim[0]], [ylim[0], ylim[1]], **kwargs)


def add_axes_zenith_range_indicator(
    fig,
    zenith_bin_edges_rad,
    zenith_bin,
    span=(0.9, 0.84, 0.09, 0.16),
    fontsize=5,
):
    ax = add_axes(
        fig=fig,
        span=span,
        style={"spines": ["left", "bottom"], "axes": [], "grid": True},
    )
    _eps = 1e-2
    ax.set_aspect("equal")
    ax.set_xlim([-_eps, 1 + _eps])
    ax.set_ylim([-_eps, 1 + _eps])
    ax_add_circle(
        ax=ax, x=0, y=0, r=1, color="black", alpha=0.2, linewidth=0.5
    )
    num_bins = len(zenith_bin_edges_rad) - 1
    for zzz in range(num_bins):
        ax_add_pie_slice(
            ax=ax,
            phi_start_rad=np.pi / 2 - zenith_bin_edges_rad[zzz],
            phi_stop_rad=np.pi / 2 - zenith_bin_edges_rad[zzz + 1],
            facecolor="black",
            alpha=0.5 if zzz == zenith_bin else 0.2,
        )
    ax.text(
        s=make_angle_range_str(
            start_rad=zenith_bin_edges_rad[zenith_bin],
            stop_rad=zenith_bin_edges_rad[zenith_bin + 1],
        ),
        x=0.0,
        y=-0.2,
        fontsize=fontsize,
        transform=ax.transAxes,
    )
    return ax


def make_angle_range_str(start_rad, stop_rad):
    circ_str = r"$^\circ{}$"
    zenith_range_str = (
        f"[{np.rad2deg(start_rad):0.1f}"
        + circ_str
        + ", "
        + f"{np.rad2deg(stop_rad):0.1f}"
        + circ_str
        + ")"
    )
    return zenith_range_str
