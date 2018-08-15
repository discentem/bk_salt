import salt.utils.platform
import logging

log = logging.getLogger(__name__)

__virtualname__ = "apm"

def __virtual__():
    if salt.utils.platform.is_windows():
        return __virtualname__

    return(False, "states.apm is currently only tested on windows")

def packages_installed(name, packages):

    ret = { 'name': name,
            'changes': {},
            'result': True,
            'comment': ''
    }

    current_packages = __salt__['apm.list_packages']()
    log.info("NAME:" + name)
    for package in packages:
        log.info(package)
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
                    install_attempt = __salt__['apm.install'](package)
                    if install_attempt == True:
                        old_package = package_name + package_version
                        ret['changes'].update({package: { 'old': old_package,
                                                          'new': package}})
                    else:
                        ret['result'] = False
                        ret['comment'].update({package: install_attempt})
                        break

        else:
            install_attempt = __salt__['apm.install'](package)
            if install_attempt == True:
                ret['changes'].update({package: { 'old': '',
                                                  'new': package}})
            else:
                ret['result'] = False
                ret['comment'].update({package: install_attempt})

    return ret
