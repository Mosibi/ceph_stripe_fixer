# ceph_stripe_fixer

Remove striped objects from a ceph pool without using the striper library.

Use this for example when a file upload to Ceph was interupted and there is a mismatch between the real number of striped parts and what the object self thinks.

## Usage
./ceph_stripe_fixer.py [-h] --pool POOL [--cephconf CEPHCONF] [--keyring KEYRING] --objectname OBJECTNAME

## Example

Create a 100 megabyte file

```
dd if=/dev/zero of=file100mb.dd count=100 bs=1MB
```

Upload it to a Ceph pool and interrupt the upload

```
rados --striper -p testpool -n client.admin put file100mb.dd file100mb.dd 
```

Now the file is on Ceph, but not all striped objects are present and while a 'rados stat' is possible, removing the object using the striper function is not possibile anymore

```
rados --striper -p testpool -n client.admin rm file100mb.dd 

error removing testpool>file100mb.dd: (16) Device or resource busy
```

And this is why ceph_stripe_fixer.py is a handy tool :)

```
rados --striper -p testpool -n client.admin stat file100mb.dd 

Number of objects: 17
Removing part file100mb.dd.0000000000000000
Removing part file100mb.dd.0000000000000001
Removing part file100mb.dd.0000000000000002
Removing part file100mb.dd.0000000000000003
Removing part file100mb.dd.0000000000000004
Removing part file100mb.dd.0000000000000005
Removing part file100mb.dd.0000000000000006
Removing part file100mb.dd.0000000000000007
Removing part file100mb.dd.0000000000000008
Removing part file100mb.dd.0000000000000009
Removing part file100mb.dd.000000000000000a
Removing part file100mb.dd.000000000000000b
Removing part file100mb.dd.000000000000000c
Removing part file100mb.dd.000000000000000d
Removing part file100mb.dd.000000000000000e
Removing part file100mb.dd.000000000000000f
Removing part file100mb.dd.0000000000000010
```

Richard Arends (richard@mosibi.nl)
