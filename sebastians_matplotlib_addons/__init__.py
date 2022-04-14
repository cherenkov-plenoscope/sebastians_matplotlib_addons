import numpy as np
import matplotlib
import warnings


matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as plt_colors

from . import hemisphere

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


def close_figure(fig):
    msg = "Use close(fig) instead."
    warnings.warn(msg, DeprecationWarning)
    print(msg, "DeprecationWarning")
    plt.close(fig)


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


def ax_add_grid(ax):
    ax.grid(color="k", linestyle="-", linewidth=0.66, alpha=0.1)


def ax_add_grid_with_explicit_ticks(
    ax, xticks, yticks, color="k", linestyle="-", linewidth=0.66, alpha=0.33,
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
                )


def ax_add_box(ax, xlim, ylim, color="k", linewidth=None):
    """
    Draw a rectangular box in xlim, ylim to ax.
    """
    #  __
    # |  |
    ax.plot(
        [xlim[0], xlim[1]],
        [ylim[0], ylim[0]],
        color=color,
        linewidth=linewidth,
    )
    #  __
    # |__
    ax.plot(
        [xlim[1], xlim[1]],
        [ylim[0], ylim[1]],
        color=color,
        linewidth=linewidth,
    )
    #
    # |__|
    ax.plot(
        [xlim[0], xlim[1]],
        [ylim[1], ylim[1]],
        color=color,
        linewidth=linewidth,
    )
    #  __
    #  __|
    ax.plot(
        [xlim[0], xlim[0]],
        [ylim[0], ylim[1]],
        color=color,
        linewidth=linewidth,
    )


def write_video_from_image_slices(
    image_sequence_wildcard_path, output_path, frames_per_second=30, threads=1,
):
    """
    Writes an h264 video.mov from an image-sequence

    Parameters
    ----------
    image_sequence_wildcard_path : str, path
            Path to the imaege-sequence using a six-digit wildcard '%06d'.
    output_path : str, path
            Path to write the final movie to.
    frames_per_second : int
            Number of frames per second in video.
    threads : int
            The number of compute-threads to be used.
    """
    outpath = os.path.splitext(output_path)[0]
    o_path = outpath + ".stdour"
    e_path = outpath + ".stderr"
    v_path = outpath + ".mov"

    with open(o_path, "w") as stdout, open(e_path, "w") as stderr:
        rc = subprocess.call(
            [
                "ffmpeg",
                "-y",  # force overwriting of existing output file
                "-framerate",
                str(int(frames_per_second)),
                "-f",
                "image2",
                "-i",
                image_sequence_wildcard_path,
                "-c:v",
                "h264",
                # '-s', '1920x1080', # sample images down to FullHD 1080p
                "-crf",
                "23",  # high quality 0 (best) to 53 (worst)
                "-crf_max",
                "25",  # worst quality allowed
                "-threads",
                str(threads),
                v_path,
            ],
            stdout=stdout,
            stderr=stderr,
        )

    return rc


def transform_homo(homo, v2):
    v = np.array([v2[0], v2[1], 1.0])
    tv = np.matmul(homo, v)
    return tv[0:2]


def transform_homo_multi(homo, xs, ys):
    assert len(xs) == len(ys)
    tx = []
    ty = []
    for i in range(len(xs)):
        v2 = np.array([xs[i], ys[i], 1.0])
        tv2 = transform_homo(homo=homo, v2=v2)
        tx.append(tv2[0])
        ty.append(tv2[1])
    return tx, ty


def ax_pcolormesh_fill(
    ax,
    x_bin_edges,
    y_bin_edges,
    intensity_rgba,
    transform,
    edgecolor='none',
    linewidth=0.0,
    threshold=0.0,
    circle_radius=None,
    grid_alpha=0.3,
    grid_linewidth=0.1,
):
    assert len(x_bin_edges) == intensity_rgba.shape[0] + 1
    assert len(y_bin_edges) == intensity_rgba.shape[1] + 1

    assert threshold >= 0.0

    assert transform.shape[0] == 3
    assert transform.shape[1] == 3

    for ix in range(intensity_rgba.shape[0]):
        for iy in range(intensity_rgba.shape[1]):

            rgba = intensity_rgba[ix, iy, :]
            if np.min(rgba) < 0.0 or np.max(rgba) > 1.0:
                print("intensity_rgba[", ix, ", ", iy, "] = ", rgba, ", out of range [0,1].")

            rgb_norm = np.max(rgba[0:3])
            rgb_flat = rgba[0:3] / rgb_norm

            if rgb_norm < threshold:
                continue

            x_start = x_bin_edges[ix]
            x_stop = x_bin_edges[ix + 1]

            y_start = y_bin_edges[iy]
            y_stop = y_bin_edges[iy + 1]

            xpoly = [x_start, x_start, x_stop, x_stop]
            ypoly = [y_start, y_stop, y_stop, y_start]

            txpoly, typoly = transform_homo_multi(transform, xpoly, ypoly)

            ax.fill(
                txpoly,
                typoly,
                facecolor=(rgb_flat[0], rgb_flat[1], rgb_flat[2]),
                edgecolor=edgecolor,
                linewidth=linewidth,
                alpha=rgb_norm,
            )

    if circle_radius:
        phis = np.linspace(0, 2 * np.pi, 360)
        xpts = []
        ypts = []
        for phi in phis:
            vec = circle_radius * np.array([np.cos(phi), np.sin(phi)])
            tvec = transform_homo(transform, vec)
            xpts.append(tvec[0])
            ypts.append(tvec[1])
        ax.plot(xpts, ypts, "k-", linewidth=2*grid_linewidth)

    GRID = True
    if GRID:
        xmin = np.min(x_bin_edges)
        xmax = np.max(x_bin_edges)
        ymin = np.min(y_bin_edges)
        ymax = np.max(y_bin_edges)

        for xv in x_bin_edges:
            txs, tys = transform_homo_multi(transform, xs=[xv, xv], ys=[ymin, ymax])
            ax.plot(txs, tys, "k-", alpha=grid_alpha, linewidth=grid_linewidth)

        for yv in y_bin_edges:
            txs, tys = transform_homo_multi(transform, xs=[xmin, xmax], ys=[yv, yv])
            ax.plot(txs, tys, "k-", alpha=grid_alpha, linewidth=grid_linewidth)

