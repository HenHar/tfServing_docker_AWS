# Deploy Tensorflow model with TfServing in a docker container on AWS instance

## Train model and save in saved model format
tf.saved_model.save([model], [save_path]) or model.export(save_path)
This examples uses EfficientNet model with imagenet weights, created in jupyter notebook "create_model.ipynb"

### directory should look like this with the top folder name as the model name
model_name=eff_imagenet
![alt text](https://github.com/HenHar/tfServing-inference-flutter/blob/main/images/required_structure.png?raw=true)

## Deploy with TF Serving docker locally for testing
sudo docker build -t eff_imagenet -f Dockerfile .

### Run docker container locally:
sudo docker run -d -p 8501:8501 eff_imagenet

### Test availabilty in browser
http://localhost:8501/v1/models/eff_imagenet

### Test inference of the locally deployed model 
python3 test_inference.py

## Deploy on AWS
### Create new EC2 instance 
Save your "*.pem" file locally
Look for your instance's public ip address (my test instance: 3.120.130.54)

### Add inboud rule to security group: allowing inbound on port 8501
![alt text](https://github.com/HenHar/tfServing-inference-flutter/blob/main/images/security_group.png?raw=true)

### Connect to to AWS instance:
ssh -i "*.pem" ec2-user@ec2-3-120-130-54.eu-central-1.compute.amazonaws.com

### Install docker:
sudo yum install docker

### Start docker service
sudo service docker start

### Copy data to AWS: open new terminal to copy data via scp
mkdir data
scp -i "*.pem" "files to upload" ec2-user@ec2-3-120-130-54.eu-central-1.compute.amazonaws.com:/home/ec2-user/data

### build the docker container on EC2 instance:
sudo docker build -t eff_imagenet -f Dockerfile .

### run docker container
sudo docker run -d -p 8501:8501 eff_imagenet

### check for model avalibilty with public ipin browser
http://3.120.130.54:8501/v1/models/eff_imagenet

### run inference with test_inference.py script with following url
http://3.120.130.54:8501/v1/models/eff_imagenet:predict



