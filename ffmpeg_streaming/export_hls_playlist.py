def _get_contents(reps, name):
    content = ['#EXTM3U', '#EXT-X-VERSION:3']
    for rep in reps:
        content += ['#EXT-X-STREAM-INF:BANDWIDTH=' + str(round(rep.kilo_bitrate * 1024)) + ',RESOLUTION=' + rep.size]
        content += [name + '_' + str(rep.height) + 'p.m3u8']
    return '\n'.join(content)


def export_hls_playlist(dirname, name, reps):
    with open(dirname + "/" + name + ".m3u8", 'w', encoding='utf-8') as f_out:
        f_out.write(_get_contents(reps, name))
