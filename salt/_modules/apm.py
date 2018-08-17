import salt.exceptions
import logging
import pprint
import salt.loader

log = logging.getLogger(__name__)
__opts__ = salt.config.minion_config('/etc/salt/minion')
__grains__ = salt.loader.grains(__opts__)
__opts__['grains'] = __grains__
__utils__ = salt.loader.utils(__opts__)
__salt__ = salt.loader.minion_mods(__opts__, utils=__utils__)

__virtualname__ = "apm"

def __virtual__():
    supported_platforms = ['windows', 'darwin']
    for platform in supported_platforms:
        if __utils__['platform.is_{0}'.format(platform)]():
            return __virtualname__

    return False

def extract_package_info(string):
    package = string.split('\n')[0]
    package_name, package_version = package.split('@')
    return { 'name' : package_name, 'version' : package_version }

def list_packages(apm_cmd,
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

def _success_message(package, action="install"):
    action = (action + 'ing').upper()
    if __utils__['platform.is_windows']:
        success = "{0} {0}".format(action, package) and "done"
    elif __utils__['platform.is_darwin']:
        success = "{0} {0}".format(action, package) and "✓"

    return success

def install(apm_cmd, package):
    cmd = "{0} install {1}".format(apm_cmd, package)
    cmd_output = __salt__['cmd.run'](cmd)

    success = _success_message(package, action="install")
    if success in cmd_output:
        return True
    else:
        raise salt.exceptions.CommandExecutionError(
            cmd_output)

def uninstall(apm_cmd, package):
    cmd = "{0} uninstall {1}".format(apm_cmd, package)
    cmd_output = __salt__['cmd.run'](cmd)

    success = _success_message(package, action="uninstall")
    if cmd_output == success:
        return True
    else:
        raise salt.exceptions.CommandExecutionError(
            cmd_output)
