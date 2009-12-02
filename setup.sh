#!/bin/sh -e

user=vios
project_name=hyeoncheon
var_dir=/var/opt/$project_name



echo "### setup project environment..."
# default layout:
echo "# preparing external layout..."
rm -f var
sudo mkdir -p $var_dir
sudo chown -R $user.libvirtd $var_dir
ln -s $var_dir var

mkdir -p var/local-pool
mkdir -p var/shared-pool
mkdir -p var/isos


### storage pool for local vms
echo "# preparing local storage pool..."
sed "s,@UUID@,`uuid`,;s,@VAR_DIR@,$var_dir," \
	data/local-pool.xml \
	| sudo tee /etc/libvirt/storage/local-pool.xml > /dev/null
sudo chmod 600 /etc/libvirt/storage/local-pool.xml
sudo rm -f /etc/libvirt/storage/autostart/local-pool.xml
sudo ln -s ../local-pool.xml /etc/libvirt/storage/autostart/

echo "please check libvirt configurations and restert libvirtd manually."

echo "done."



echo "### setup external resource..."
echo "# install and setup apache webserver..."
sudo apt-get install apache2 libapache2-mod-fastcgi python-flup
sudo rm -f /etc/apache2/mods-enabled/rewrite.load
sudo ln -s ../mods-available/rewrite.load /etc/apache2/mods-enabled/
echo "FIXME patch default site configuration... (not automated yet!)"
sudo cp hyeoncheon.init /etc/init.d/hyeoncheon
echo "FIXME setup runlevel... (not yet automated.)"

sudo /etc/init.d/hyeoncheon restart
sudo /etc/init.d/apache2 restart


