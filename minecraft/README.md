These plugins poll a bukkit server for information about it. It may require
the Essentials plugin. I have not tested it that much.

You will need to enable rcon on your minecraft server. Edit `server.properties` and
set `enable-rcon=true`. Then add (or set) `rcon.password` with a secret
of your choice. Since you'll never need to memorize it, it's suggested
that you just fill it with random gibberish. Then provide the password
to munin in the munin-node config file (as mentioned in the main README):
 
```
[minecraft_*]
env.password <password>
```

 Replacing <password> with the rcon password. If you have
 rcon running on a different server and/or a nonstandard
 port, add:

```
env.port 1234
env.host 300.403.22.1
```
You'll see `Rcon connection from: /127.0.0.1` at the
 server console a fair bit, that means that it's working.
