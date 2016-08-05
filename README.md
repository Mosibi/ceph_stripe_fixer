# ceph_stripe_fixer

Remove striped objects from a ceph pool without using the striper library.

Use this for example when a file upload to Ceph was interupted and there is a mismatch between the real number of striped parts and what the object self thinks.

Richard Arends (richard@mosibi.nl)
