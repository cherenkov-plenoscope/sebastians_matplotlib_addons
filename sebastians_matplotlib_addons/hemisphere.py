import numpy as np
import matplotlib.patches as plt_patches
import matplotlib.colors as plt_colors


def ax_add_projected_points_with_colors(
    ax,
    azimuths_deg,
    zeniths_deg,
    half_angle_deg,
    color=None,
    alpha=None,
    rgbas=None,
):
    if rgbas is not None:
        _colors = rgbas[:, 0:3]
        _alphas = rgbas[:, 3]
    else:
        assert color is not None
        assert alpha is not None
        _colors = [color for i in range(len(zeniths))]
        _alphas = [alpha for i in range(len(zeniths))]

    for i in range(len(_colors)):
        ax_add_projected_circle(
            ax=ax,
            azimuth_deg=azimuths_deg[i],
            zenith_deg=zeniths_deg[i],
            half_angle_deg=half_angle_deg,
            linewidth=0.0,
            fill=True,
            zorder=2,
            facecolor=_colors[i],
            alpha=_alphas[i],
        )


def ax_add_projected_circle(
    ax, azimuth_deg, zenith_deg, half_angle_deg, **kwargs
):
    point_diameter = 2.0 * np.deg2rad(half_angle_deg)
    zenith = np.deg2rad(zenith_deg)
    azimuth = np.deg2rad(azimuth_deg)

    proj_radii = np.sin(zenith)
    proj_x = np.cos(azimuth) * proj_radii
    proj_y = np.sin(azimuth) * proj_radii

    e1 = plt_patches.Ellipse(
        (proj_x, proj_y),
        width=point_diameter * np.cos(zenith),
        height=point_diameter,
        angle=azimuth_deg,
        **kwargs,
    )
    ax.add_patch(e1)


def ax_add_magnet_flux_symbol(
    ax, azimuth_deg, zenith_deg, half_angle_deg, direction, **kwargs
):
    ax_add_projected_circle(
        ax=ax,
        azimuth_deg=azimuth_deg,
        zenith_deg=zenith_deg,
        half_angle_deg=half_angle_deg,
        linewidth=1,
        fill=False,
        **kwargs,
    )
    if direction == "inwards":
        ax_add_projected_circle(
            ax=ax,
            azimuth_deg=azimuth_deg,
            zenith_deg=zenith_deg,
            half_angle_deg=half_angle_deg * 0.25,
            linewidth=0.0,
            fill=True,
            **kwargs,
        )
    elif "outwards":
        x, y = _transform(np.deg2rad(azimuth_deg), np.deg2rad(zenith_deg))
        ax.plot(
            x,
            y,
            marker="x",
            markersize=6.5 * np.cos(np.deg2rad(zenith_deg)),
            **kwargs,
        )
        nn = np.deg2rad(half_angle_deg)
        cx = np.sqrt(1.0 - nn**2 - nn**2)


def _transform(az, zd):
    r = np.sin(zd)
    x = np.cos(az) * r
    y = np.sin(az) * r
    return x, y


def ax_add_plot(ax, azimuths_deg, zeniths_deg, **kwargs):
    _x, _y = _transform(
        az=np.deg2rad(azimuths_deg), zd=np.deg2rad(zeniths_deg)
    )
    ax.plot(_x, _y, **kwargs)


def ax_add_mesh(ax, azimuths_deg, zeniths_deg, faces, **kwargs):
    azs = np.deg2rad(azimuths_deg)
    zds = np.deg2rad(zeniths_deg)
    for face in faces:
        a_az = azs[face[0]]
        a_zd = zds[face[0]]

        b_az = azs[face[1]]
        b_zd = zds[face[1]]

        c_az = azs[face[2]]
        c_zd = zds[face[2]]

        aa = _transform(az=a_az, zd=a_zd)
        bb = _transform(az=b_az, zd=b_zd)
        cc = _transform(az=c_az, zd=c_zd)

        ax.plot([aa[0], bb[0]], [aa[1], bb[1]], **kwargs)
        ax.plot([bb[0], cc[0]], [bb[1], cc[1]], **kwargs)
        ax.plot([cc[0], aa[0]], [cc[1], aa[1]], **kwargs)


def ax_add_grid(
    ax,
    azimuths_deg,
    zeniths_deg,
    linewidth,
    color,
    alpha,
    draw_lower_horizontal_edge_deg=None,
    zenith_min_deg=0.0,
):
    zeniths = np.deg2rad(zeniths_deg)
    zenith_min = np.deg2rad(zenith_min_deg)

    proj_radii = np.sin(zeniths)
    for i in range(len(zeniths)):
        ax_add_circle(
            ax=ax,
            x=0,
            y=0,
            r=proj_radii[i],
            linewidth=linewidth,  # * np.cos(zeniths[i]),
            color=color,
            alpha=alpha,
        )

    azimuths = np.deg2rad(azimuths_deg)
    for a in range(len(azimuths)):
        for z in range(len(zeniths)):
            if z == 0:
                continue
            zzstart = np.max([zenith_min, zeniths[z - 1]])
            r_start = np.sin(zzstart)
            zzstop = np.max([zenith_min, zeniths[z]])
            r_stop = np.sin(zzstop)
            start_x = r_start * np.cos(azimuths[a])
            start_y = r_start * np.sin(azimuths[a])
            stop_x = r_stop * np.cos(azimuths[a])
            stop_y = r_stop * np.sin(azimuths[a])
            ax.plot(
                [start_x, stop_x],
                [start_y, stop_y],
                color=color,
                linewidth=linewidth,  # * np.cos(zeniths[z - 1]),
                alpha=alpha,
            )

    if draw_lower_horizontal_edge_deg is not None:
        zd_edge = np.deg2rad(draw_lower_horizontal_edge_deg)
        r = np.sin(zd_edge)
        ax.plot(
            [-3 / 4 * r, 0],
            [-r, -r],
            color=color,
            linewidth=linewidth,
            alpha=alpha,
        )
        ax.plot(
            [-r, -r],
            [0, -3 / 4 * r],
            color=color,
            linewidth=linewidth,
            alpha=alpha,
        )
        ax_add_circle(
            ax=ax, x=0, y=0, r=r, linewidth=linewidth, color=color, alpha=alpha
        )


def ax_add_ticklabels(
    ax,
    azimuths_deg,
    rfov=1.0,
    fmt=r"{:1.0f}$^\circ$",
):
    xshift = -0.07 * rfov
    yshift = -0.025 * rfov

    azimuths = np.deg2rad(azimuths_deg)
    azimuth_deg_strs = [fmt.format(az) for az in azimuths_deg]
    xs = rfov * np.cos(azimuths) + xshift
    ys = rfov * np.sin(azimuths) + yshift
    for a in range(len(azimuths)):
        ax.text(x=xs[a], y=ys[a], s=azimuth_deg_strs[a])


def ax_add_circle(ax, x, y, r, linewidth, color, alpha):
    phis = np.linspace(0, 2 * np.pi, 1001)
    xs = r * np.cos(phis)
    ys = r * np.sin(phis)
    ax.plot(xs, ys, linewidth=linewidth, color=color, alpha=alpha)


def ax_add_ticklabel_text(
    ax,
    radius=0.95,
    label_azimuths_deg=[0, 90, 180, 270],
    label_azimuths=["N", "E", "S", "W"],
    xshift=-0.05,
    yshift=-0.025,
    **kwargs,
):
    for i in range(len(label_azimuths_deg)):
        _az = np.deg2rad(label_azimuths_deg[i])
        xs = radius * np.cos(_az) + xshift
        ys = radius * np.sin(_az) + yshift
        ax.text(
            x=xs,
            y=ys,
            s=label_azimuths[i],
            rotation=90 + label_azimuths_deg[i],
            **kwargs,
        )
