#!py

def run():

  role = __salt__['grains.get']('role', None)
  key = __salt__['pillar.get']("windows_license:" + str(role) + ":key", None)

  config = {}
  if role and key:
    config[key] = 'license.activate'

  else:
    config['Nothing for license.activate to do'] = {
      'test.show_notification': [
        { 'text': 'No windows key found for role: \'{0}\''.format(role) }
      ]
    }

  return config
