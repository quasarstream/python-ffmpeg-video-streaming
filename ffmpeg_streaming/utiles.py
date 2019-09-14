import os
import tempfile


def round_to_even(num):
    num = int(num) if ((int(num) % 2) == 0) else int(num) + 1
    return num


def clear_tmp_file(filename):
    if filename is not None and filename.startswith(tempfile.gettempdir()) and filename.endswith('_py_ff_vi_st.tmp'):
        os.remove(filename)


def get_path_info(path):
    dirname = os.path.dirname(path).replace("\\", "/")
    name = str(os.path.basename(path).split('.')[0])

    if not os.path.exists(dirname):
        os.mkdir(dirname)

    return dirname, name
