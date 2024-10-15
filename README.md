# Deploy Tensorflow model with TfServing in a docker container on AWS instance

## Train model and save in saved model format
* save with `tf.saved_model.save([model], [save_path])` or `model.export(save_path])`
* This examples uses EfficientNet model with imagenet weights, created in jupyter notebook "create_model.ipynb"

### Directory should look like this with the top folder name as the model name
model_name=eff_imagenet\
![alt text](https://github.com/HenHar/tfServing-inference-flutter/blob/main/images/required_structure.png?raw=true)

## Deploy with TF Serving docker locally for testing
```
sudo docker build -t eff_imagenet -f Dockerfile .
```

### Run docker container locally:
```
sudo docker run -d -p 8501:8501 eff_imagenet
```

### Test availabilty in browser
http://localhost:8501/v1/models/eff_imagenet

### Test inference of the locally deployed model 
```
python3 test_inference.py
```

## Deploy on AWS
### Create new EC2 instance with Ubuntu
* Save your "*.pem" file locally
* Look for your instance's public ip address (my test instance: 3.120.130.54)

### Add temporary inboud rule to security group: allowing inbound on port 8501
![alt text](https://github.com/HenHar/tfServing-inference-flutter/blob/main/images/security_group.png?raw=true)

### Connect to to AWS instance:
```
ssh -i "*.pem" ubuntu@3.120.130.54
```

### Install docker: (on Amazaon Linux instance install with sudo yum install docker and sudo service docker start)
```
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

 sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```



### Copy data to AWS: open new terminal to copy data via scp
```
mkdir data
scp -i "*.pem" "files to upload" ubuntu@3.120.130.54:/home/ubuntu/data
```

### build the docker container on EC2 instance:
```
sudo docker build -t eff_imagenet -f Dockerfile .
```

### run docker container
```
sudo docker run -d -p 8501:8501 eff_imagenet
```

### check for model avalibilty with public ip in browser
http://3.120.130.54:8501/v1/models/eff_imagenet

### run inference with test_inference.py script with following url
http://3.120.130.54:8501/v1/models/eff_imagenet:predict


# Add https support with caddy and nip.io
* caddy also provides a reverse_proxy so that only port :80 and :443 of the EC2 instance needs to be open to the internet
* you have to register a domain or you can use nip.io for https support
* adjust security group and delete inbound rule for port :8501

### install caddy
```
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https curl
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy
```
##
* uncomment the reverse_proxy line in the Caddyfile
`sudo nano /etc/caddy/Caddyfile`

```
<EC2 Public IP>.nip.io {
    reverse_proxy localhost:8501
}
```

start or restart caddy service
```
sudo systemctl start caddy
sudo systemctl restart caddy
```



