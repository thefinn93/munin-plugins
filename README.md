Some munin plugins for a minecraft server.

Install
-------

1. Place these files in your munin plugins directory then
 symlink them to the active plugins directory, or whatever
 your distro does. On Ubuntu, place them in `/usr/share/munin/plugins/`
 then symlink them in `/etc/munin/plugins/`. 

2. Edit your munin-node file (on Ubuntu this is located in
 `/etc/munin/plugin-conf.d/munin-node`) and add the appropriate information.
 See the README's in each subdirectory for more specific infomation 

3. Restart munin-node and your server should start reporting
 stats. 
