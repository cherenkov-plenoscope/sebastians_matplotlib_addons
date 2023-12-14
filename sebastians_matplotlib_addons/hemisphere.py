import numpy as np
import matplotlib.patches as plt_patches
import matplotlib.colors as plt_colors
import spherical_coordinates


def ax_add_projected_points_with_colors(
    ax,
    azimuths_rad,
    zeniths_rad,
    half_angle_rad,
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
            azimuth_rad=azimuths_rad[i],
            zenith_rad=zeniths_rad[i],
            half_angle_rad=half_angle_rad,
            linewidth=0.0,
            fill=True,
            zorder=2,
            facecolor=_colors[i],
            alpha=_alphas[i],
        )


def ax_add_projected_circle(
    ax, azimuth_rad, zenith_rad, half_angle_rad, **kwargs
):
    point_diameter = 2.0 * half_angle_rad

    proj_radii = np.sin(zenith_rad)
    proj_x = np.cos(azimuth_rad) * proj_radii
    proj_y = np.sin(azimuth_rad) * proj_radii

    e1 = plt_patches.Ellipse(
        (proj_x, proj_y),
        width=point_diameter * np.cos(zenith_rad),
        height=point_diameter,
        angle=np.rad2deg(azimuth_rad),
        **kwargs,
    )
    ax.add_patch(e1)


def ax_add_magnet_flux_symbol(
    ax, azimuth_rad, zenith_rad, half_angle_rad, direction, **kwargs
):
    ax_add_projected_circle(
        ax=ax,
        azimuth_rad=azimuth_rad,
        zenith_rad=zenith_rad,
        half_angle_rad=half_angle_rad,
        linewidth=1,
        fill=False,
        **kwargs,
    )
    if direction == "inwards":
        ax_add_projected_circle(
            ax=ax,
            azimuth_rad=azimuth_rad,
            zenith_rad=zenith_rad,
            half_angle_rad=half_angle_rad * 0.25,
            linewidth=0.0,
            fill=True,
            **kwargs,
        )
    elif "outwards":
        x, y = _transform(azimuth_rad, zenith_rad)
        ax.plot(
            x,
            y,
            marker="x",
            markersize=6.5 * np.cos(zenith_rad),
            **kwargs,
        )


def _transform(az, zd):
    return spherical_coordinates.az_zd_to_cx_cy(azimuth_rad=az, zenith_rad=zd)


def ax_add_plot(ax, azimuths_rad, zeniths_rad, **kwargs):
    _x, _y = _transform(az=azimuths_rad, zd=zeniths_rad)
    ax.plot(_x, _y, **kwargs)


def ax_add_mesh(ax, azimuths_rad, zeniths_rad, faces, **kwargs):
    azs = azimuths_rad
    zds = zeniths_rad
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


def ax_add_grid_stellarium_style(ax, color="black", alpha=1.0, linewidth=0.05):
    TAU = 2.0 * np.pi
    ax_add_grid(
        ax=ax,
        azimuths_rad=np.linspace(0, TAU, 36, endpoint=False),
        zeniths_rad=np.deg2rad([0, 10, 20, 30, 40, 50, 60, 70, 80, 90]),
        linewidth=linewidth,
        color=color,
        alpha=alpha,
        draw_lower_horizontal_edge_rad=None,
        zenith_min_rad=np.deg2rad(5),
    )


def ax_add_grid(
    ax,
    azimuths_rad,
    zeniths_rad,
    linewidth,
    color,
    alpha,
    draw_lower_horizontal_edge_rad=None,
    zenith_min_rad=0.0,
):
    zeniths = zeniths_rad
    zenith_min = zenith_min_rad

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

    azimuths = azimuths_rad
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

    if draw_lower_horizontal_edge_rad is not None:
        zd_edge = draw_lower_horizontal_edge_rad
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


def ax_add_circle(ax, x, y, r, linewidth, color, alpha):
    phis = np.linspace(0, 2 * np.pi, 1001)
    xs = r * np.cos(phis)
    ys = r * np.sin(phis)
    ax.plot(xs, ys, linewidth=linewidth, color=color, alpha=alpha)


def ax_add_ticklabel_text(
    ax,
    radius=0.95,
    label_azimuths_rad=[0, 1 / 2 * np.pi, 2 / 2 * np.pi, 3 / 2 * np.pi],
    label_azimuths=["N", "E", "S", "W"],
    xshift=-0.05,
    yshift=-0.025,
    **kwargs,
):
    for i in range(len(label_azimuths_rad)):
        _az = label_azimuths_rad[i]
        xs = radius * (np.cos(_az) + xshift)
        ys = radius * (np.sin(_az) + yshift)
        ax.text(
            x=xs,
            y=ys,
            s=label_azimuths[i],
            rotation=90 + np.rad2deg(label_azimuths_rad[i]),
            **kwargs,
        )
