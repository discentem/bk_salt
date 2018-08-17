import salt.exceptions
import logging

__virtualname__ = "apm"

def __virtual__():
    supported_platforms = ['windows', 'darwin']
    for platform in supported_platforms:
        if __utils__['platform.is_{0}'.format(platform)]():
            return __virtualname__

    return False

def _get_apm_cmd():
    if 'apm_cmd' in __context__:
            return __context__['apm_cmd']
    __context__['apm_cmd'] = __salt__['grains.filter_by']({
        'default': '/usr/local/bin/apm',
        'Windows': 'C:\Program Files\Atom Beta\Atom\\resources\cli\\apm.cmd'
        },
        grain='os_family'
    )

    return __context__['apm_cmd']

def extract_package_info(string):
    package = string.split('\n')[0]
    package_name, package_version = package.split('@')
    return { 'name' : package_name, 'version' : package_version }

def list_packages(apm_cmd=None,
                  with_categories=False):

    if apm_cmd == None:
        apm_cmd = _get_apm_cmd()

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

def install(package, apm_cmd=None):
    if apm_cmd == None:
        apm_cmd = _get_apm_cmd()
    cmd = "{0} install {1}".format(apm_cmd, package)
    cmd_output = __salt__['cmd.run'](cmd)

    success = _success_message(package, action="install")
    if success in cmd_output:
        return True
    else:
        raise salt.exceptions.CommandExecutionError(
            cmd_output)

def uninstall(package, apm_cmd=None):
    if apm_cmd == None:
        apm_cmd = _get_apm_cmd()

    cmd = "{0} uninstall {1}".format(apm_cmd, package)
    cmd_output = __salt__['cmd.run'](cmd)

    success = _success_message(package, action="uninstall")
    if cmd_output == success:
        return True
    else:
        raise salt.exceptions.CommandExecutionError(
            cmd_output)
