#!py

def run():
    pillar = {
        'cpe_touchid': {
            'enabled': True,
        },
        'cpe_hosts': {
            'extra_entries': {
                'default': ['thing2']
            }
        }
    }

    is_friday = __salt__['dates.today_is']('Friday')
    cpe_machine = __salt__['grains.get']('tags:cpe_machine', False)

    if is_friday or cpe_machine:
        pillar['cpe_hosts']['extra_entries'] = {
            'default' : ['thing1']
        }
    if __grains__['os_family'] == 'Windows':
        pillar['cpe_touchid']['enabled'] = False

    return pillar