import salt.utils.platform
import salt.exceptions
import logging
import pprint

log = logging.getLogger(__name__)

__virtualname__ = "apm"

def __virtual__():
    if salt.utils.platform.is_windows():
        return __virtualname__

    return False

default_apm_cmd = "C:\Program Files\Atom Beta\\resources\cli\\apm.cmd"

def extract_package_info(string):
    package = string.split('\n')[0]
    package_name, package_version = package.split('@')
    return { 'name' : package_name, 'version' : package_version }

def list_packages(apm_cmd=default_apm_cmd,
                  with_categories=False):

    cmd = "{0} list".format(apm_cmd)
    cmd_output = __salt__['cmd.run'](cmd)
    cmd_output = cmd_output.split(' ')

    if with_categories == False:
        packages = {}
        for line in cmd_output:
            if '@' in line:
                package_info = extract_package_info(line)
                package_name = package_info['name']
                package_version = package_info['version']
                packages[package_name] = package_version

    elif with_categories:
        packages = { 'Built-in Atom Packages' : {},
                     'Community Packages' : {} }
        # we can assume all packages are built-ins until
        #  we hit "Packages" in the output
        appendTo = 'Built-in Atom Packages'
        for line in cmd_output:
            if line == "Packages":
                appendTo = 'Community Packages'
            elif '@' in line:
                package_info = extract_package_info(line)
                package_name = package_info['name']
                package_version = package_info['version']
                packages[appendTo][package_name] = package_version

    return packages

def install(package, apm_cmd=default_apm_cmd):
    cmd = "{0} install {1}".format(apm_cmd, package)
    cmd_output = __salt__['cmd.run'](cmd)

    success = "Installing {0}".format(package) and "done"
    if success in cmd_output:
        return True
    else:
        raise salt.exceptions.CommandExecutionError(
            cmd_output)

def uninstall(package, apm_cmd=default_apm_cmd):
    cmd = "{0} uninstall {1}".format(apm_cmd, package)
    cmd_output = __salt__['cmd.run'](cmd)

    success = "Uninstalling {0} done".format(package)
    if cmd_output == success:
        return True
    else:
        raise salt.exceptions.CommandExecutionError(
            cmd_output)
