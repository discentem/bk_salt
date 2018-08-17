#!py

def run():
    config = {}

    apm_packages = __salt__['pillar.get']("apm_packages", None)

    if apm_packages != None:
        config["install apm packages"] = {
            'apm.installed': [
                { 'packages': apm_packages }
            ]
        }

    return config
