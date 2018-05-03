#!py

def run():

    role = __salt__['grains.get']('role', None)
    apps = __salt__['pillar.get']("apps:" + str(role), None)
    config = {}

    if role and apps and apps != []:
        for app in apps:
            config['install {0}'.format(app)] = {
                'chocolatey.installed': [
                    { 'name': app }
                ]
            }

    else:
        id = 'Nothing for chocolatey.install to do'
        config[id] = {
            'test.show_notification': [
              { 'text': 'No apps found for role: \'{0}\''.format(role) }
            ]
        }

        if apps == []:
            msg = "Apps list is empty for role: {0}".format(role)
            config[id]['test.show_notification'][0]['text'] = msg


    return config
