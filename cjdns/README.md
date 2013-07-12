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

It takes time for cjdcmd peers to output all results, so the plugin may
timeout periodically. It might make sense to increase timeout by
adding/editing the timeout line in `munin-node` from 20 seconds
(the default value) to something like 60:

timeout 60

A sample output, from Dan's Seattle node:

![Seanode CJDNS peer, last day](https://hostedmunin.com/plot/meshwith.me-4948/cjdns_peers/day.png)
