#!/usr/bin/env python

# Remove striped objects from a ceph pool without using the striper library.
# Use this for example when a file upload to Ceph was interupted and there
# is a mismatch between the real number of striped parts and what the
# object self thinks.
#
# Richard Arends (richard@mosibi.nl)

import rados
import argparse


###
# Main
###
parser = argparse.ArgumentParser(description='Remove corrupt striped file from a ceph pool.')
parser.add_argument('--pool', help='ceph pool name', required=True)
parser.add_argument('--cephconf', default="/etc/ceph/ceph.conf",  help='ceph.conf file', required=False)
parser.add_argument('--keyring', default="/etc/ceph/ceph.client.admin.keyring", help='ceph keyring file', required=False)
parser.add_argument('--objectname', help='the name of the corrupt object', required=True)
args = parser.parse_args()

cephpool = str(args.pool)
cephconf = str(args.cephconf)
keyring = str(args.keyring)
objectname = str(args.objectname)

cluster = rados.Rados(conffile=cephconf, conf=dict(keyring=keyring))
cluster.connect()
ioctx = cluster.open_ioctx(cephpool)

object_size = int(ioctx.get_xattr('{0}.0000000000000000'.format(objectname), 'striper.size'))			# the total size of the object
stripe_size = int(ioctx.get_xattr('{0}.0000000000000000'.format(objectname), 'striper.layout.object_size'))	# nr of bytes for every object part
number_of_objects = (object_size/stripe_size)

print 'Number of objects: {0}'.format(number_of_objects)
object_nr = 0

while object_nr < number_of_objects:
	hex_id = '{0:x}'.format(int(object_nr))									# convert the object # to hex
	hex_id_long = '{0:0>16}'.format(hex_id)									# prefix with leading zeros

	stripe_object = '{0}.{1}'.format(objectname, hex_id_long)						# <name>.<hex_id_long>. this is the name of the object in the pool

	try:
		statobject = ioctx.stat(stripe_object)
		print 'Removing part {0}'.format(stripe_object)
		ioctx.remove_object(stripe_object)
	except:
		print 'Part {0} is not present'.format(stripe_object)

	object_nr += 1

ioctx.close()
cluster.shutdown()
