"""
ffmpeg_streaming.build_args
~~~~~~~~~~~~

Build a command for the FFmpeg


:copyright: (c) 2020 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""
import sys

from ._utiles import cnv_options_to_args, get_path_info, clean_args


def _stream2file(stream2file):
    """
    @TODO: add documentation
    """
    args = stream2file.format.all
    args.update({'c': 'copy'})
    args.update(stream2file.options)

    return cnv_options_to_args(args) + [stream2file.output_]


def _get_audio_bitrate(rep, index: int = None):
    """
    @TODO: add documentation
    """
    if rep.bitrate.audio_ is not None and rep.bitrate.audio_ != 0:
        opt = 'b:a' if index is None else 'b:a:' + str(index)
        return {opt: rep.bitrate.audio}

    return {}


def _get_dash_stream(key, rep):
    """
    @TODO: add documentation
    """
    args = {
        'map':              0,
        's:v:' + str(key):   rep.size.normalize,
        'b:v:' + str(key):   rep.bitrate.normalize_video()
    }
    args.update(_get_audio_bitrate(rep, key))
    return cnv_options_to_args(args)


def _dash(dash):
    """
    @TODO: add documentation
    """
    dirname, name = get_path_info(dash.output_)
    _args = dash.format.all
    _args.update({
        'use_timeline':    1,
        'use_template':    1,
        'init_seg_name':   name + '_init_$RepresentationID$.$ext$',
        "media_seg_name":  name + '_chunk_$RepresentationID$_$Number%05d$.$ext$',
        'f':               'dash'
    })
    _args.update(dash.options)
    args = cnv_options_to_args(_args)

    for key, rep in enumerate(dash.reps):
        args += _get_dash_stream(key, rep)

    return args + ['-strict', '-2', dirname + '/' + name + '.mpd']


def _hls_seg_ext(hls):
    """
    @TODO: add documentation
    """
    return 'm4s' if hls.options.get('hls_segment_type', '') == 'fmp4' else 'ts'


def _get_hls_stream(hls, rep, dirname, name):
    """
    @TODO: add documentation
    """
    args = hls.format.all
    args.update({
        'hls_list_size':            0,
        'hls_time':                 10,
        'hls_allow_cache':          1,
        'hls_segment_filename':     dirname + "/" + name + "_" + str(rep.size.height) + "p_%04d." + _hls_seg_ext(hls),
        'hls_fmp4_init_filename':   name + "_" + str(rep.size.height) + "p_init.mp4",
        's:v':                      rep.size.normalize,
        'b:v':                      rep.bitrate.normalize_video()
    })
    args.update(_get_audio_bitrate(rep))
    args.update({'strict': '-2'})
    args.update(hls.options)

    return cnv_options_to_args(args) + [dirname + "/" + name + "_" + str(rep.size.height) + "p.m3u8"]


def _hls(hls):
    """
    @TODO: add documentation
    """
    dirname, name = get_path_info(hls.output_)
    streams = []
    for rep in hls.reps:
        streams += _get_hls_stream(hls, rep, dirname, name)

    return streams


def stream_args(media):
    """
    @TODO: add documentation
    """
    return getattr(sys.modules[__name__], "_%s" % type(media).__name__.lower())(media)


def command_builder(ffmpeg_bin: str, media):
    """
    @TODO: add documentation
    """
    args = [ffmpeg_bin] + cnv_options_to_args(dict(media.media.input_opts)) + stream_args(media)
    return " ".join(clean_args(args))

