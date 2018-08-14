import salt.utils.platform
import logging

log = logging.getLogger(__name__)

__virtualname__ = "apm"

def __virtual__():
    if salt.utils.platform.is_windows():
        return __virtualname__

    return(False, "states.apm is currently only test on windows")

def install_packages(name):

    ret = { 'name': name
            'changes': {},
            'result': True,
            'comment': ''
    }

    current_packages = __salt__['apm.get_packages']()
