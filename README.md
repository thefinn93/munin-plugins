Some munin plugins for a minecraft server.

Install
-------

1. Place these files in your munin plugins directory then
 symlink them to the active plugins directory, or whatever
 your distro does. On Ubuntu, place them in `/usr/share/munin/plugins/`
 then symlink them in `/etc/munin/plugins/`. 

2. Enable rcon on your minecraft server. Edit `server.properties` and
 set `enable-rcon=true`. Then add (or set) `rcon.password` with a secret
 of your choice. Since you'll never need to memorize it, it's suggested
 that you just fill it with random gibberish

3. Edit your munin-node file (on Ubuntu this is located in
 `/etc/munin/plugin-conf.d/munin-node`) and add this at the
 bottom:

```
[minecraft_*]
env.password=<password>
```

 Replacing <password> with the rcon password. If you have
 rcon running on a different server and/or a nonstandard
 port, add:

```
env.port=1234
env.host=300.403.22.1
```

4. Restart munin-node and your server should start reporting
 stats. You'll see `Rcon connection from: /127.0.0.1` at the
 server console a fair bit, that means that it's working.
