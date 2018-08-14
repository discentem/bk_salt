import salt.utils.platform
import logging
import pprint

log = logging.getLogger(__name__)

__virtualname__ = "apm"

def __virtual__():
    if salt.utils.platform.is_windows():
        return __virtualname__

    return False

def get_packages(apm_cmd="C:\Program Files\Atom Beta\\resources\cli\\apm.cmd"):
    cmd = "{0} list".format(apm_cmd)
    stdout = __salt__['cmd.run'](cmd)
    stdout = stdout.split(' ')

    packages = { 'Built-in' : {},
                 'Packages' : {} }
    for line in stdout:
        if 'Built-in' in line:
            appendTo = 'Built-in'
        elif line == "Packages":
            appendTo = 'Packages'
        elif '@' in line:
            package = line.split('\n')[0]

            split = package.split('@')
            package_name = split[0]
            package_version = split[1]
            packages[appendTo][package_name] = package_version

    return packages
