import webbrowser
import platform


def get_version():
    version = platform.python_version()
    if len(version) != 3:  # This is to exclude minor versions.
        version = version[0:3]
    return version


def open_doc(url):
    webbrowser.open(url)


def open_library():
    version = get_version()
    url = "http://docs.python.org/{}/library/re.html".format(version)
    open_doc(url)


def open_guide():
    version = get_version()
    url = "http://docs.python.org/{}/howto/regex.html".format(version)
    open_doc(url)
