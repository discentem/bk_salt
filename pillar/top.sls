#!py

def run():
  top_file = {
    'base': {
        '*': [ 'default' ]
    }
  }

  role = __salt__['grains.get']("role", None)
  if role != None:
      top_file['base']['*'].append(role)

  return top_file
