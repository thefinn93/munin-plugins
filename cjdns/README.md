These plugins interact with [cjdns](https://github.com/cjdelisle/cjdns).
Currently the only one, cjdns_peers,
checks the number of active peers you have connected. It requires
[cjdcmd](https://github.com/inhies/cjdcmd). If cjdcmd isn't in the path,
set it in the config. Recent versions of cjdcmd do not require .cjdnsadmin.
Specifying cjdroute.conf is enough:

```
[cjdns_*]
env.PATH /path/to/cjdcmd/directory
env.file /path/to/my/cjdroute.conf
```

A sample output, from Dan's Seattle node:

![Seanode CJDNS peer, last day](https://hostedmunin.com/plot/meshwith.me-4948/cjdns_peers/day.png)
