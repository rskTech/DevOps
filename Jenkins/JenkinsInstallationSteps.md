# Installing Jenkins on Ubuntu

## Install Java
````bash
apt-get install openjdk-17-jdk
````

## Install Jenkins
On AWS instances, the jenkins repos are already added. Hence, the below command shall work
````
apt install jenkins
````
If the above does not work, follow the below steps

````bash
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > \
    /etc/apt/sources.list.d/jenkins.list'
sudo apt-get update
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys  5BA31D57EF5975CA   => replace this ID with the error you ar egetting when doing apt update
sudo apt-get install jenkins
````

## Finish installation
1. Browse to <ip_address>:8080
2. Follow onscreen instructions
