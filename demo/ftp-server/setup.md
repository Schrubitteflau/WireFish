https://phoenixnap.com/kb/install-ftp-server-on-ubuntu-vsftpd

```bash
sudo apt update
sudo apt install vsftpd
sudo systemctl start vsftpd
sudo systemctl enable vsftpd
sudo useradd -m ftpuser
sudo passwd ftpuser
# mdp : passw0rd
```

Puis décommenter `#write_enable=YES` dans `/etc/vsftpd.conf`
