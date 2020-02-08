"""
ffmpeg_streaming.export_hls_playlist
~~~~~~~~~~~~

Export HLS playlist(HLS manifest)


:copyright: (c) 2019 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""


def _get_contents(reps, manifest):
    content = ['#EXTM3U', '#EXT-X-VERSION:3']
    for rep in reps:
        content += ['#EXT-X-STREAM-INF:BANDWIDTH=' + str(round(rep.kilo_bitrate * 1024)) + ',RESOLUTION=' + rep.size]
        content += [manifest + '_' + str(rep.height) + 'p.m3u8']
    return '\n'.join(content)


def export_hls_playlist(playlist_path, manifest, reps):
    with open(playlist_path, 'w', encoding='utf-8') as f_out:
        f_out.write(_get_contents(reps, manifest))
