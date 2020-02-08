"""
ffmpeg_streaming.build_args
~~~~~~~~~~~~

Build a command for the FFmpeg


:copyright: (c) 2019 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""

from .utiles import get_path_info
from .rep import Representation


def _get_hls_args(hls):
    dirname, name = get_path_info(hls.output)

    args = []
    for key, rep in enumerate(hls.reps):
        if isinstance(rep, Representation):
            if hls.options is not None:
                for option in hls.options:
                    args += ['-' + option, str(hls.options[option])]
            if key > 0:
                args += ['-c:v', hls.video_format]
                if hls.audio_format is not None:
                    args += ['-c:a', hls.audio_format]
            args += ['-s:v', rep.size]
            args += ['-crf', '20']
            args += ['-sc_threshold', '0']
            args += ['-g', '48']
            args += ['-keyint_min', '48']
            args += ['-hls_list_size', str(hls.hls_list_size)]
            args += ['-hls_time', str(hls.hls_time)]
            args += ['-hls_allow_cache', str(hls.hls_allow_cache)]
            args += ['-b:v', rep.bit_rate]
            if rep.audio_bit_rate is not None:
                args += ['-b:a', rep.audio_bit_rate]
            args += ['-maxrate', str(round(rep.kilo_bitrate * 1.2)) + "k"]
            args += ['-hls_segment_filename', dirname + "/" + name + "_" + str(rep.height) + "p_%04d.ts"]
            if hls.hls_key_info_file is not None:
                args += ['-hls_key_info_file', hls.hls_key_info_file.replace("\\", "/")]
            args += ['-strict', hls.options.get('strict', "-2")]
            args += [dirname + "/" + name + "_" + str(rep.height) + "p.m3u8"]

    return args


def _get_dash_args(dash):
    dirname, name = get_path_info(dash.output)

    args = [
        '-bf', '1',
        '-keyint_min', '120',
        '-g', '120',
        '-sc_threshold', '0',
        '-b_strategy', '0',
        '-use_timeline', '1',
        '-use_template', '1',
        '-init_seg_name', (name + '_init_$RepresentationID$.$ext$') if dash.init_seg_name is None else dash.init_seg_name,
        "-media_seg_name", (name + '_chunk_$RepresentationID$_$Number%05d$.$ext$') if dash.media_seg_name is None else dash.media_seg_name,
        '-f', 'dash'
    ]

    if dash.options is not None:
        for option in dash.options:
            args += ['-' + option, str(dash.options[option])]

    for key, rep in enumerate(dash.reps):
        if isinstance(rep, Representation):
            args += ['-map', '0']
            args += ['-b:v:' + str(key), rep.bit_rate]
            if rep.audio_bit_rate is not None:
                args += ['-b:a:' + str(key), rep.audio_bit_rate]
            args += ['-s:v:' + str(key), rep.size]

    if dash.adaption is not None:
        args += ['-adaptation_sets', dash.adaption]
    args += ['-strict', dash.options.get('strict', "-2")]
    args += ['"' + dirname + '/' + name + '.mpd"']
    
    return args


def _get_stream2file_args(stream2file):
    args = ['-c', 'copy']

    if stream2file.options is not None:
        for option in stream2file.options:
            args += ['-' + option, str(stream2file.options[option])]
    args += ['"' + stream2file.output + '"']

    return args


def build_command(cmd, media_obj):
    if type(cmd) != list:
        cmd = [cmd]

    cmd += ['-y', '-i', '"' + media_obj.filename.replace("\\", "/") + '"']
    cmd += ['-c:v', media_obj.video_format]

    if media_obj.audio_format is not None:
        cmd += ['-c:a', media_obj.audio_format]

    media_name = type(media_obj).__name__

    if media_name == 'HLS':
        cmd += _get_hls_args(media_obj)
    elif media_name == 'DASH':
        cmd += _get_dash_args(media_obj)
    elif media_name == 'StreamToFile':
        cmd += _get_stream2file_args(media_obj)

    return " ".join(cmd)
