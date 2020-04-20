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
    args = {'c': 'copy'}
    args.update(stream2file.options)

    return cnv_options_to_args(args) + [stream2file.output_]


def _get_dash_stream(key, rep):
    args = {
        'map':              '0',
        'b:v:' + str(key):   rep.bitrate.normalize_video(),
        'b:a:' + str(key):   rep.bitrate.audio,
        's:v:' + str(key):   rep.size.normalize
    }
    return cnv_options_to_args(args)


def _dash(dash):
    dirname, name = get_path_info(dash.output_)
    init_args = {
        'c:v':              dash.format.video,
        'c:a':              dash.format.audio,
        'bf':              '1',
        'keyint_min':      '120',
        'g':               '120',
        'sc_threshold':    '0',
        'b_strategy':      '0',
        'use_timeline':    '1',
        'use_template':    '1',
        'init_seg_name':   name + '_init_$RepresentationID$.$ext$',
        "media_seg_name":  name + '_chunk_$RepresentationID$_$Number%05d$.$ext$',
        'f':               'dash'
    }
    init_args.update(dash.options)
    args = cnv_options_to_args(init_args)

    for key, rep in enumerate(dash.reps):
        args += _get_dash_stream(key, rep)

    return args + ['-strict', '-2', dirname + '/' + name + '.mpd']


def _hls_seg_ext(hls):
    return 'm4s' if hls.options.get('hls_segment_type', '') == 'fmp4' else 'ts'


def _get_hls_stream(hls, rep, dirname, name):
    args = {
        'c:v':                      hls.format.video,
        'c:a':                      hls.format.audio,
        's:v':                      rep.size.normalize,
        'crf':                      '20',
        'sc_threshold':             '0',
        'g':                        '48',
        'keyint_min':               '48',
        'hls_list_size':            '0',
        'hls_time':                 '10',
        'hls_allow_cache':          '1',
        'b:v':                      rep.bitrate.normalize_video(),
        'b:a':                      rep.bitrate.audio,
        'maxrate':                  rep.bitrate.max_rate,
        'hls_segment_filename':     dirname + "/" + name + "_" + str(rep.size.height) + "p_%04d." + _hls_seg_ext(hls),
        'hls_fmp4_init_filename':   name + "_init.mp4",
        'strict':                   '-2'
    }
    args.update(hls.options)

    return cnv_options_to_args(args) + [dirname + "/" + name + "_" + str(rep.size.height) + "p.m3u8"]


def _hls(hls):
    dirname, name = get_path_info(hls.output_)
    streams = []
    for rep in hls.reps:
        streams += _get_hls_stream(hls, rep, dirname, name)

    return streams


def stream_args(media):
    return getattr(sys.modules[__name__], "_%s" % type(media).__name__.lower())(media)


def command_builder(ffmpeg_bin: str, media):
    args = [ffmpeg_bin] + cnv_options_to_args(dict(media.media.input_opts)) + stream_args(media)
    return " ".join(clean_args(args))

