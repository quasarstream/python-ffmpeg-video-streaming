import os

from .export_hls_playlist import export_hls_playlist
from .rep import Representation


def get_path_info(path):
    dirnmae = os.path.dirname(path).replace("\\", "/")
    name = str(os.path.basename(path).split('.')[0])

    if not os.path.exists(dirnmae):
        os.mkdir(dirnmae)

    return dirnmae, name


def get_hls_parm(hls):

    dirnmae, name = get_path_info(hls.path)

    commands = []
    for rep in hls.reps:
            if isinstance(rep, Representation):
                if hls.filter is not None:
                    for filter in hls.filter:
                        commands += ['-' + filter, hls.filter[filter]]
                commands += ['-s:v', rep.size()]
                commands += ['-crf', '20']
                commands += ['-sc_threshold', '0']
                commands += ['-g', '48']
                commands += ['-keyint_min', '48']
                commands += ['-hls_list_size', '0']
                commands += ['-hls_time', str(hls.hls_time)]
                commands += ['-hls_allow_cache', str(hls.hls_allow_cache)]
                commands += ['-b:v', rep.bit_rate()]
                commands += ['-maxrate', str(round(rep.kilo_bitrate * 1.2)) + "k"]
                commands += ['-hls_segment_filename', dirnmae + "/" + name + "_" + str(rep.height) + "p_%04d.ts"]
                if hls.hls_key_info_file is not None:
                    commands += ['-hls_key_info_file', hls.hls_key_info_file]
                commands += ['-strict', hls.strict]
                commands += [dirnmae + "/" + name + "_" + str(rep.height) + "p.m3u8"]

    export_hls_playlist(dirnmae, name, hls.reps)

    return commands


def get_dash_parm(dash):
    dirnmae, name = get_path_info(dash.path)

    commands = [
        '-bf', '1',
        '-keyint_min', '120',
        '-g', '120',
        '-sc_threshold', '0',
        '-b_strategy', '0',
        '-use_timeline', '1',
        '-use_template', '1',
        '-f', 'dash'
    ]

    if dash.filter is not None:
        for filter in dash.filter:
            commands += ['-' + filter, dash.filter[filter]]

    count = 0
    for rep in reversed(dash.reps):
            if isinstance(rep, Representation):
                commands += ['-map', '0']
                commands += ['-b:v:' + str(count), rep.bit_rate()]
                commands += ['-s:v:' + str(count), rep.size()]
                count += 1

    if dash.adaption is not None:
        commands += ['-adaptation_sets', dash.adaption]
    commands += ['-strict', dash.strict]
    commands += ['"' + dirnmae + '/' + name + '.mpd"']

    return commands
