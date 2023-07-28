do the nsc commands after running nats in docker

then

nsc edit account --name eighty --js-mem-storage -1 --js-disk-storage -1 --js-streams -1 --js-consumer -1
nsc push -a eighty -u nats://127.0.0.1:4222

# test nats

```
nats --creds ~/.local/share/nats/nsc/keys/creds/eighty/eighty/eighty.creds account info
```

should show

```
Connection Information:

               Client ID: 11
               Client IP: 192.168.48.1
                     RTT: 1.761917ms
       Headers Supported: true
         Maximum Payload: 1.0 MiB
           Connected URL: nats://127.0.0.1:4222
       Connected Address: 127.0.0.1:4222
     Connected Server ID: NC45E6OKHDTQTR4AQDM57OFB5LUBWNSR5MGJEQN5FICU4ZUX2KBEKOAE
          TLS Connection: no

JetStream Account Information:
```

## notes

client user management

- each service should define and request for the perms they need, in nats user's syntax.

  - req user group
  - user block
  - user group config hardcoded , prob in clientconfig.json?

- have a wrapper function to make it easy on the service definition side, ride on nats
