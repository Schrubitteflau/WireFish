https://phoenixnap.com/kb/install-ftp-server-on-ubuntu-vsftpd

sudo apt update
sudo apt install vsftpd
sudo systemctl start vsftpd
sudo systemctl enable vsftpd
sudo useradd -m ftpuser
sudo passwd ftpuser
mdp : passw0rd

Décommenter #write_enable=YES dans /etc/vsftpd.conf
