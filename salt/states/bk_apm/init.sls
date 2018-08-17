#!py

def run():
    config = {}

    role = __salt__['grains.get']('role', None)
    apm_packages = __salt__['pillar.get']("apm_packages:" + str(role), None)

    if apm_packages != None:
        config["install apm packages"] = {
            'apm.installed': [
                { 'packages': apm_packages }
            ]
        }

    return config
