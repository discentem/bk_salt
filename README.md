### Basic Usage

- cd into `bk_salt`

- Run salt-call: 
    
    ```bash
    sudo /opt/salt/salt-call --local state.apply --file-root=$(pwd)/salt --pillar-root=$(pwd)/pillar -l debug saltenv=base
    ```
