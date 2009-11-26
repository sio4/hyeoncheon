#!/bin/sh -e

user=vios
project_name=hyeoncheon
var_dir=/var/opt/$project_name



# default layout:
echo "preparing external layout..."
rm -f var
sudo mkdir -p $var_dir
sudo chown -R $user.libvirtd $var_dir
ln -s $var_dir var

mkdir -p var/local-pool
mkdir -p var/shared-pool
mkdir -p var/isos


### storage pool for local vms
echo "preparing local storage pool..."
sed "s,@UUID@,`uuid`,;s,@VAR_DIR@,$var_dir," \
	data/local-pool.xml \
	| sudo tee /etc/libvirt/storage/local-pool.xml > /dev/null
sudo chmod 600 /etc/libvirt/storage/local-pool.xml
sudo rm -f /etc/libvirt/storage/autostart/local-pool.xml
sudo ln -s ../local-pool.xml /etc/libvirt/storage/autostart/

echo "please check libvirt configurations and restert libvirtd manually."

echo "done."
