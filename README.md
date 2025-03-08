### Basic Usage

- cd into `bk_salt`

- Run salt locally: 
    
    ```bash
    sudo /opt/salt/salt-call --local state.apply --file-root=$(pwd)/salt --pillar-root=$(pwd)/pillar --module-dir=$(pwd)/salt/_modules -l debug saltenv=base
    ```

# Repository Layout

[salt/top.sls](salt/top.sls) points to a single state, [salt/states/cpe_init](salt/states/cpe_init/) which dynamically includes other states via the `include` state.