These plugins interact with CJDNS. Currently the only one, cjdns_peers,
checks the number of active peers you have connected. It requires
[cjdcmd](https://github.com/inhies/cjdcmd). If cjdcmd isn't in the path,
set it in the config. Additionally, if the host, port or password need
to be specified (ie because the user that munin runs as doesn't have a 
`.cjdnsadmin` file), specify those as well:

```
[cjdns_peers]
env.CJDCMD /home/user/projects/go/bin/cjdcmd
env.host 127.0.0.1
env.port 11234
env.pass super_duper_secure
```

A sample output, from Dan's Seattle node:

![Seanode CJDNS peer, last day](https://hostedmunin.com/plot/meshwith.me-4948/cjdns_peers/day.png)
