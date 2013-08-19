These plugins interact with [cjdns](https://github.com/cjdelisle/cjdns)

cjdns_peers
-----------
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


cjdns_bandwidth
----------
Show's each peer's bandwidth usage thanks to [this](https://github.com/cjdelisle/cjdns/pull/284).
Must be run as a user with a `.cjdnsadmin` file in their home directory. On my server,
manually specifying HOME was required:

```
[cjdns_*]
user finn
env.HOME /home/finn
```

You'll need to make sure that the `cjdnsadmin` library is in your python path. cjdnsadmin is in
the `contrib/python/` folder of the cjdns git, and you can find your python path(s) by running:

```
$ python
>>> import sys
>>> sys.path
```

That will print out a list of directories, just ensure that it's in one of them


Additionally, if the enviromenal variable NAMES is set to a non empty string, it will attempt to
import that string and replace the labels on the graph with those names. This is handy because
no one remembers public keys:

```
env.NAMES /home/finn/cjdnsnames.json
```

and a sample file:

```json
{
        "l3f9rd1qrdjxbz0cjbjfxprxcnwt1zptdz1cctxcdgbkr510xcb0.k": "mal",
        "xltnfur6xh2n36g79y1qpht910c13sq7lb049662x7trfx3gf190.k": "florida",
        "8hgr62ylugxjyyhxkz254qtz60p781kbswmhhywtbb5rpzc5lxj0.k": "seanode"
}
```
