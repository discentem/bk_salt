import salt.loader

__opts__ = salt.config.minion_config('/etc/salt/minion')
__grains__ = salt.loader.grains(__opts__)
__opts__['grains'] = __grains__
__utils__ = salt.loader.utils(__opts__)
__salt__ = salt.loader.minion_mods(__opts__, utils=__utils__)

def __virtual__():
    return 'apm'

def get_cmd():

    apm_cmd = __salt__['grains.filter_by']({
        'default': '/usr/local/bin/apm',
        'Windows': 'C:\Program Files\Atom Beta\Atom\\resources\cli\\apm.cmd'
        },
        grain='os_family'
    )

    return apm_cmd
