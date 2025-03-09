from typing import Any, Dict

def managed(name: str) -> Dict[str, Any]:
    enable = __salt__['pillar.get']('cpe_touchid:enabled', False)

    if not enable:
        return __states__['file.absent'](
            name='/etc/pam.d/sudo_local',
        )
    return __states__['file.managed'](
        name='/etc/pam.d/sudo_local',
        source='salt://_states/cpe_touchid/templates/touchid.sls',
        template='py'   
    )