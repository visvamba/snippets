# AWS EC2 

## Connect via Session Manager (SSM)

1. Add this configuration to ~/.ssh/config

```
# SSH over Session Manager
host i-* mi-*
    ProxyCommand sh -c "aws --region <region> ssm start-session --target %h --document-name AWS-StartSSHSession --parameters 'portNumber=%p'"
```

## Mount via SSHFS

Example:

1. First, check if can start SSM session
   ```bash
   aws ssm start-session --target i-03b3b6093fbd249a9 --document-name AWS-StartSSHSession
   ```

2. Then mount via SSHFS.

    ```bash
    sshfs ec2-user@i-03b3b6093fbd249a9:/home/ec2-user/ /Users/visvamba/mnt -o "IdentityFile=/Users/visvamba/ssh_keys/speech2text.pem"
    ```

## Connect via SSH

```bash
ssh -i <keyfile> <user>@<instance ID>
```

