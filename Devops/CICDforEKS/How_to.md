Reference:
https://www.eksworkshop.com/

# 环境准备
### 1. 安装下载kubectl及eksctl
1.1	Kubectl
```CLI
# sudo curl --silent --location -o /usr/local/bin/kubectl \
https://amazon-eks.s3.us-west-2.amazonaws.com/1.17.7/2020-07-08/bin/linux/amd64/kubectl

sudo chmod +x /usr/local/bin/kubectl
```
1.2 Eksctl
```CLI
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
cd /tmp
./eksctl completion bash >> ~/.bash_completion
. /etc/profile.d/bash_completion.sh
. ~/.bash_completion
```
### 2.Create Key for EKS and Upload to KMS

ssh-keygen. ##默认设置，一路回车

aws ec2 import-key-pair --key-name "eksworkshop" --public-key-material file://~/.ssh/id_rsa.pub

如果遇到下面的错误，执行aws configure，做初始化配置
#### [ec2-user@ip-172-31-89-175 .ssh]$ aws ec2 import-key-pair --key-name "eksworkshop" --public-key-material file://~/.ssh/id_rsa.pub
You must specify a region. You can also configure your region by running "aws configure"
#### [ec2-user@ip-172-31-89-175 .ssh]$ aws ec2 import-key-pair --key-name "eksworkshop" --public-key-material file://~/.ssh/id_rsa.pub
Unable to locate credentials. You can configure credentials by running "aws configure".

4.Setting customer master key (CMK) for EKS
-
aws kms create-alias --alias-name alias/eksworkshop --target-key-id $(aws kms create-key --query KeyMetadata.Arn --output text)

export MASTER_ARN=$(aws kms describe-key --key-id alias/eksworkshop --query KeyMetadata.Arn --output text)

echo "export MASTER_ARN=${MASTER_ARN}" | tee -a ~/.bash_profile

资源创建
-
1.Create EKS Cluster (30min)
Download yaml file

#一级标题  
##二级标题  
###三级标题  
####四级标题  
#####五级标题  
######六级标题  


