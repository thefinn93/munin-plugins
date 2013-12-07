# CJDNS
These plugins interact with [cjdns](https://github.com/cjdelisle/cjdns). They
all need access to the cjdns admin interface, which can be granted in two ways:

### 1. Specify info in munin config
The preferred way to connect it to the cjdns admin interface is to place the
connection infomation in munin's node configuration, like so:

```
[cjdns_*]
env.cjdns_addr 127.0.0.1
env.cjdns_port 11234
env.cjdns_password super_duper_secure_password
```

The `cjdns_address` and `cjdns_port` are optional, and the values shown above
are used if not otherwise specified. `cjdns_password` is not optional.

### 2. Run the plugins as a user with a `.cjdnsadmin` file

The other, legacy method of connection involves running these plugins as a
specific user who has a `~/.cjdnsadmin` file. For this option, the config should
look something like this:

```
[cjdns_*]
user finn
env.HOME /home/finn
```

Note that it may not be necessary to specify `HOME`, but in my tests it was.

## cjdns_bandwidth
Show's each peer's bandwidth usage thanks to [this](https://github.com/cjdelisle/cjdns/pull/284).
Labels each peer based on the "user" field, if available (only available on
incoming peers), otherwise just public key. If the enviromenal variable NAMES is
set to a non empty string, it will use those names as well (names in this file
override "user" from cjdns):

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

## cjdns_nodes
Graphs the number of unique nodes in your routing table. This is a somewhat good
way to get an idea of the total size of the network.

## cjdns_peers.py
checks the number of active peers you have connected, using cjdns's
`InterfaceController_peerStats()` function.

## cjdns_peers.sh
checks the number of active peers you have connected using [cjdcmd](https://github.com/inhies/cjdcmd).
if cjdcmd is not in the path of the munin plugin, you may specify it's location
in the config:

```
[cjdns_peers]
env.CJDCMD /home/user/go/bin/cjdcmd
```

### cjdns_versions
Pings all known hosts, records their reported version numbers, and graphs the
the popularity of each version over time. Note that at this time I have been
unable to get this plugin to complete in a timely manner, and do not recommend
actually using it.
