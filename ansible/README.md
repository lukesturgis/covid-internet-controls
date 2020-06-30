# Ansible

For configuration management, Ansible is used in order to secure each host and deploy the latest software changes.

## Ansible Command & Control Server

The Ansible command and control server (C&C) is responsible for handling all requests to each given VPS.

Setup for this C&C server is as follows:


1. Install Ansible

  		sudo apt-add-repository ppa:ansible/ansible
		sudo apt install ansible

2. Create/modify `/etc/ansible/hosts`, which contains the IP addresses of managed hosts. Note that this file contains addresses with a prefix for easier understanding of which country a VPS resides in, rather than an IP address.

		Korea 			ansible_host=xx.xx.xx.xx
		...

3. Ensure that the following files are present in the `ansible` directory:

	1.  `.env`, which contains the ROOT_PASSWORD.
	2.  `authorized_keys`, which contains the SSH keys for the users that are authorized to SSH into each VPS.
	3.  `cert.pem`, the certificate file for HTTPS communication to each VPS.
	4.  `key.pem`, the key file for HTTPS communication to each VPS.
	5.  `.worker.env`, which contains the REQUEST_KEY for verifying POST requests to each VPS.


## Onboarding a New VPS

To configure a new host to be ready for Ansible management, you must perform the following:

1. Copy over the SSH key for connection:
	
		ssh-copy-id {server IP address}

## Ansible Deployment

To run an ansible playbook, you will need to perform the following:

 1. Switch to the root acccount
	
		sudo -s

2. Enter the `ansible` directory:

		cd ansible/

3. Run a given playbook:

		ansible-playbook deploy.yml


This will execute the playbook against all of the hosts that exist in `/etc/ansible/hosts`.