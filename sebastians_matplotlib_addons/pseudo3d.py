import numpy as np


def transform(projection, v2):
    v = np.array([v2[0], v2[1], 1.0])
    tv = np.matmul(projection, v)
    return tv[0:2]


def transform_multi(projection, xs, ys):
    assert len(xs) == len(ys)
    tx = []
    ty = []
    for i in range(len(xs)):
        v2 = np.array([xs[i], ys[i]])
        tv2 = transform(projection=projection, v2=v2)
        tx.append(tv2[0])
        ty.append(tv2[1])
    return tx, ty


def ax_add_grid(
    ax,
    projection,
    x_bin_edges,
    y_bin_edges,
    alpha=0.66,
    linewidth=0.1,
    color="k",
    linestyle="-",
):
    xmin = np.min(x_bin_edges)
    xmax = np.max(x_bin_edges)
    ymin = np.min(y_bin_edges)
    ymax = np.max(y_bin_edges)
    for xv in x_bin_edges:
        txs, tys = transform_multi(projection, xs=[xv, xv], ys=[ymin, ymax])
        ax.plot(
            txs,
            tys,
            linestyle=linestyle,
            alpha=alpha,
            linewidth=linewidth,
            color=color,
        )
    for yv in y_bin_edges:
        txs, tys = transform_multi(projection, xs=[xmin, xmax], ys=[yv, yv])
        ax.plot(
            txs,
            tys,
            linestyle=linestyle,
            alpha=alpha,
            linewidth=linewidth,
            color=color,
        )


def ax_add_plot(
    ax,
    projection,
    x,
    y,
    **kwargs,
):
    tx = []
    ty = []
    for i in range(len(x)):
        tvec = transform(projection, [x[i], y[i]])
        tx.append(tvec[0])
        ty.append(tvec[1])
    ax.plot(tx, ty, **kwargs)


def ax_add_mesh(ax, projection, mesh, **kwargs):
    for e in mesh["edges"]:
        start = mesh["vertices"][e[0]]
        stop = mesh["vertices"][e[1]]
        ax_add_plot(
            ax=ax,
            projection=projection,
            y=[-start[0], -stop[0]],
            x=[start[1], stop[1]],
            **kwargs,
        )


def ax_add_circle(
    ax,
    projection,
    x,
    y,
    r,
    alpha=0.66,
    linewidth=0.1,
    color="k",
    linestyle="-",
    fn=360,
):
    phis = np.linspace(0, 2 * np.pi, fn)
    xpts = []
    ypts = []
    for phi in phis:
        vec = r * np.array([x + np.cos(phi), y + np.sin(phi)])
        tvec = transform(projection, vec)
        xpts.append(tvec[0])
        ypts.append(tvec[1])
    ax.plot(
        xpts,
        ypts,
        linestyle=linestyle,
        alpha=alpha,
        linewidth=linewidth,
        color=color,
    )


def ax_add_mesh_intensity_to_alpha(
    ax,
    projection,
    x_bin_edges,
    y_bin_edges,
    intensity_rgb,
    linewidth=0.0,
    threshold=0.0,
    grid_alpha=0.3,
    grid_linewidth=0.1,
    edgecolor="none",
    gamma=1.0,
):
    assert len(x_bin_edges) == intensity_rgb.shape[0] + 1
    assert len(y_bin_edges) == intensity_rgb.shape[1] + 1

    assert 1.0 > threshold >= 0.0

    assert projection.shape[0] == 3
    assert projection.shape[1] == 3

    assert 0.0 < gamma

    for ix in range(intensity_rgb.shape[0]):
        for iy in range(intensity_rgb.shape[1]):
            rgb = intensity_rgb[ix, iy, :]
            if np.min(rgb) < 0.0 or np.max(rgb) > 1.0:
                print(
                    "intensity_rgb[",
                    ix,
                    ", ",
                    iy,
                    "] = ",
                    rgb,
                    ", out of range [0,1].",
                )

            rgb_norm = np.max(rgb[0:3])
            if rgb_norm < threshold:
                continue

            rgb_flat = rgb[0:3] / rgb_norm
            alpha = rgb_norm**gamma

            x_start = x_bin_edges[ix]
            x_stop = x_bin_edges[ix + 1]

            y_start = y_bin_edges[iy]
            y_stop = y_bin_edges[iy + 1]

            xpoly = [x_start, x_start, x_stop, x_stop]
            ypoly = [y_start, y_stop, y_stop, y_start]

            txpoly, typoly = transform_multi(projection, xpoly, ypoly)

            ax.fill(
                txpoly,
                typoly,
                facecolor=(rgb_flat[0], rgb_flat[1], rgb_flat[2]),
                edgecolor=edgecolor,
                linewidth=linewidth,
                alpha=alpha,
            )
