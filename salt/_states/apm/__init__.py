import logging
import salt.exceptions
log = logging.getLogger(__name__)

__virtualname__ = "apm"

def __virtual__():
    return __virtualname__

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

def _ensure_packages_is_array(packages):
    if isinstance(packages, str):
        packages_string = packages
        packages = [packages_string]
    return packages

def installed(name, packages, apm_cmd=None, hard=False):

    if apm_cmd == None:
        apm_cmd = _get_apm_cmd()

    ret = { 'name': name,
            'changes': {},
            'result': True,
            'comment': ''
    }

    packages = _ensure_packages_is_array(packages)

    if hard:
        current_packages = __salt__['apm.list_packages'](apm_cmd=apm_cmd,
                                                         with_categories=True)
        current_packages = current_packages['Community Packages']
        for current_package in current_packages:
            if current_package not in packages:
                uninstall_success = __salt__['apm.uninstall'](current_package,
                                                              apm_cmd=apm_cmd)
                if uninstall_success == True:
                    ret['changes'].update({current_package: { 'old': current_package,
                                                      'new': ''}})
                    msg = "{0} uninstalled due to apm.installed(hard=True) in state"
                    ret['comment'] += msg.format(current_package) + '\n'
                else:
                    ret['result'] = False
                    ret['comment'] += "{0} {1}\n".format(current_package, uninstall_success)

    elif hard == False:
        current_packages = __salt__['apm.list_packages'](apm_cmd=apm_cmd,
                                                         with_categories=False)
    for package in packages:
        try:
            package_name, package_version = package.split('@')
        except:
            package_name = package
            package_version = None
        if package_name in current_packages:
            if package_version == None:
                ret['comment'] += "{0} already installed\n".format(package_name)
            elif package_version != None:
                if current_packages[package_name] == package_version:
                    ret['comment'] += "{0} already installed\n".format(package)
                else:
                    install_success = __salt__['apm.install'](package,
                                                              apm_cmd=apm_cmd)
                    if install_success == True:
                        old_package = package_name + package_version
                        ret['changes'].update({package: { 'old': old_package,
                                                          'new': package}})
                    else:
                        ret['result'] = False
                        ret['comment'].update({package: install_success})

        else:
            install_success = __salt__['apm.install'](package,
                                                      apm_cmd=apm_cmd)
            if install_success == True:
                ret['changes'].update({package: { 'old': '',
                                                  'new': package}})
            else:
                ret['result'] = False
                ret['comment'].update({package: install_success})

    return ret

def uninstalled(name, packages, apm_cmd=None):
    if apm_cmd == None:
        apm_cmd = _get_apm_cmd()

    ret = { 'name': name,
            'changes': {},
            'result': True,
            'comment': ''
    }

    packages = _ensure_packages_is_array(packages)
    current_packages = __salt__['apm.list_packages'](apm_cmd=apm_cmd,
                                                     with_categories=False)

    for package in packages:
        try:
            package_name, package_version = package.split('@')
        except:
            package_name = package
            package_version = None
        if package_name in current_packages:
            if package_version == None:
                uninstall_success = __salt__['apm.uninstall'](package,
                                                              apm_cmd=apm_cmd)
                if uninstall_success == True:
                    ret['changes'].update({package: { 'old': package,
                                                      'new': ''}})
                else:
                    ret['result'] = False
                    ret['comment'].update({package: install_success})
            elif package_version != None:
                if current_packages[package_name] == package_version:
                    uninstall_success = __salt__['apm.uninstall'](package,
                                                                  apm_cmd=apm_cmd)
                    if uninstall_success == True:
                        ret['changes'].update({package: { 'old': package,
                                                          'new': ''}})
                    else:
                        ret['changes'].update({package: { 'old': '',
                                                          'new': ''}})
                        ret['result'] = False
                        ret['comment'].update({package: install_success})
                else:
                    ret['comment'] += "{0} not installed\n".format(package_name)
        else:
            ret['comment'] += "{0} not installed\n".format(package)

    return ret
