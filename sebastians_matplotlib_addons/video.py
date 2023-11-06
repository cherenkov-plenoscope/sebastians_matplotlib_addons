import os
import subprocess


def write_video_from_image_slices(
    image_sequence_wildcard_path,
    output_path,
    frames_per_second=30,
    threads=1,
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
