import re


def convert_to_sec(time):
    h, m, s = time.split(":")
    return (int(h) * 3600) + (int(m) * 60) + int(s)


def progress(line, total_sec):
    time = re.search('(?<=time=)\w+:\w+:\w+', line)
    if time:
        sec = convert_to_sec(time.group(0))
        return round(100 * sec/total_sec)


def get_duration_sec(line):
    time = re.search('(?<=Duration: )\w+:\w+:\w+', line)
    if time:
        return convert_to_sec(time.group(0))
