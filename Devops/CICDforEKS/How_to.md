如果看不到图片请编辑 hosts 文件
Windows, C:\Windows\System32\drivers\etc\hosts
MBP, /private/etc/hosts
```
# GitHub Start 
192.30.253.112    Build software better, together 
192.30.253.119    gist.github.com
151.101.184.133    assets-cdn.github.com
151.101.184.133    raw.githubusercontent.com
151.101.184.133    gist.githubusercontent.com
151.101.184.133    cloud.githubusercontent.com
151.101.184.133    camo.githubusercontent.com
151.101.184.133    avatars0.githubusercontent.com
151.101.184.133    avatars1.githubusercontent.com
151.101.184.133    avatars2.githubusercontent.com
151.101.184.133    avatars3.githubusercontent.com
151.101.184.133    avatars4.githubusercontent.com
151.101.184.133    avatars5.githubusercontent.com
151.101.184.133    avatars6.githubusercontent.com
151.101.184.133    avatars7.githubusercontent.com
151.101.184.133    avatars8.githubusercontent.com
# GitHub End
```
-----
Reference:
https://www.eksworkshop.com/

## 环境准备
### 1. 安装下载kubectl及eksctl
#### 1.1	Kubectl
```CLI
# sudo curl --silent --location -o /usr/local/bin/kubectl \
https://amazon-eks.s3.us-west-2.amazonaws.com/1.17.7/2020-07-08/bin/linux/amd64/kubectl

sudo chmod +x /usr/local/bin/kubectl
```
#### 1.2 Eksctl
```CLI
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
cd /tmp
./eksctl completion bash >> ~/.bash_completion
./etc/profile.d/bash_completion.sh
. ~/.bash_completion
```
### 2. Create Key for EKS and Upload to KMS
```
ssh-keygen. ##默认设置，一路回车
```
```
aws ec2 import-key-pair --key-name "eksworkshop" --public-key-material file://~/.ssh/id_rsa.pub
```
```
如果遇到下面的错误，执行aws configure，做初始化配置
#### [ec2-user@ip-172-31-89-175 .ssh]$ aws ec2 import-key-pair --key-name "eksworkshop" --public-key-material file://~/.ssh/id_rsa.pub
You must specify a region. You can also configure your region by running "aws configure"
#### [ec2-user@ip-172-31-89-175 .ssh]$ aws ec2 import-key-pair --key-name "eksworkshop" --public-key-material file://~/.ssh/id_rsa.pub
Unable to locate credentials. You can configure credentials by running "aws configure".
```
### 3. Setting customer master key (CMK) for EKS
```
aws kms create-alias --alias-name alias/eksworkshop --target-key-id $(aws kms create-key --query KeyMetadata.Arn --output text)

export MASTER_ARN=$(aws kms describe-key --key-id alias/eksworkshop --query KeyMetadata.Arn --output text)

echo "export MASTER_ARN=${MASTER_ARN}" | tee -a ~/.bash_profile
```
## 资源创建
### 1. Create EKS Cluster (30min)
[ec2-user@ip-172-31-89-175 .ssh]$ echo "export MASTER_ARN=${MASTER_ARN}" | tee -a ~/.bash_profile
export MASTER_ARN=arn:aws:kms:us-east-1:348026336041:key/e978dc48-4299-4bf7-999c-46101f671ac9
```
Download yaml file and change it with yourname
https://github.com/hlmiao/I-Day/raw/master/Devops/CICDforEKS/scripts/eksworkshop-yourname.yaml
```
编辑`eksworkshop-youname.yaml`，复制上述`MASTER_ARN`的连接到yaml文件的`keyARN`处
```
eksctl create cluster -f eksworkshop-youname.yaml
```
如果创建EKS中报kubectl版本错误，可以忽略
![image](https://github.com/hlmiao/I-Day/blob/master/Devops/CICDforEKS/pic/001.png)

### 2. Launch Code Commit & CodeBuild
CloudFormation 执行 ops-deployment-cicd.yaml
https://github.com/hlmiao/I-Day/raw/master/Devops/CICDforEKS/scripts/ops-deployment-cicd-1020.yaml
#### 2.1 Going to CloudFormation
![image](https://github.com/hlmiao/I-Day/blob/master/Devops/CICDforEKS/pic/002.png)
#### 2.2 Create Stack
![image](https://github.com/hlmiao/I-Day/blob/master/Devops/CICDforEKS/pic/003.png)
#### 2.3 Design Stack
![image](https://github.com/hlmiao/I-Day/blob/master/Devops/CICDforEKS/pic/004.png)
#### 2.4 Copy yml to template (clean default firstly)
![image](https://github.com/hlmiao/I-Day/blob/master/Devops/CICDforEKS/pic/005.png)
#### 2.5 Validate the template
![image](https://github.com/hlmiao/I-Day/blob/master/Devops/CICDforEKS/pic/006.png)
#### 2.6 Go to Next
![image](https://github.com/hlmiao/I-Day/blob/master/Devops/CICDforEKS/pic/007.png)
#### 2.7 Naming Stack
![image](https://github.com/hlmiao/I-Day/blob/master/Devops/CICDforEKS/pic/008.png)
#### 2.8 Config stack
![image](https://github.com/hlmiao/I-Day/blob/master/Devops/CICDforEKS/pic/009.png)
#### 2.9 Running stack
![image](https://github.com/hlmiao/I-Day/blob/master/Devops/CICDforEKS/pic/010.png)
#### 2.10 Waiting for Stack Finished
![image](https://github.com/hlmiao/I-Day/blob/master/Devops/CICDforEKS/pic/011.png)
#### 2.11 Validate Resource being Created
![image](https://github.com/hlmiao/I-Day/blob/master/Devops/CICDforEKS/pic/012.png)
### 3. Modified auth K8S with Kubectl Role
Reference: https://www.eksworkshop.com/intermediate/220_codepipeline/configmap/
#### 3.1 Change Account ID to yours if you do not config in your env
```
ROLE="    - rolearn: arn:aws:iam::$ACCOUNT_ID:role/EksWorkshopCodeBuildKubectlRole\n      username: build\n      groups:\n        - system:masters"
```
#### 3.2 如果遇到类似的报错，执行`sudo yum update`
![image](https://github.com/hlmiao/I-Day/blob/master/Devops/CICDforEKS/pic/013.png)
#### 3.3 手动修改aws-auth ConfigMap，注意图片中的mapRoles是否有AccoundID
```
kubectl get -n kube-system configmap/aws-auth -o yaml | awk "/mapRoles: \|/{print;print \"$ROLE\";next}1" > /tmp/aws-auth-patch.yml
kubectl patch configmap/aws-auth -n kube-system --patch "$(cat /tmp/aws-auth-patch.yml)"
kubectl edit -n kube-system configmaps/aws-auth
```
![image](https://github.com/hlmiao/I-Day/blob/master/Devops/CICDforEKS/pic/014.png)
### 4. Config CodeCommit
#### 4.1 Going to CodeCommit that has been created & following guide to finished configuration
![image](https://github.com/hlmiao/I-Day/blob/master/Devops/CICDforEKS/pic/015.png)
#### 4.2 连接步骤
![image](https://github.com/hlmiao/I-Day/blob/master/Devops/CICDforEKS/pic/016.png)
https://console.aws.amazon.com/codesuite/codecommit/repositories/eksworkshop-eksctl/connect?connectionType=connection-instructions-GitRemoteHttps&region=us-east-1
#### 4.3 EC2上的设置
```
sudo yum -y install python2-pip
git clone codecommit::us-east-1://eksworkshop-eksctl
Download link
https://github.com/hlmiao/I-Day/raw/master/Devops/CICDforEKS/scripts/WorkshopSampleCode.zip
```
#### 4.4 Following git command to upload code to CodeCommit
![image](https://github.com/hlmiao/I-Day/blob/master/Devops/CICDforEKS/pic/017.png)
#### 4.5 Checking Code Exist in CodeCommit
![image](https://github.com/hlmiao/I-Day/blob/master/Devops/CICDforEKS/pic/018.png)
## CI/CD执行
### 1. Running CodeBuild
#### 1.1 Go to CodeBuild Page and find the Build Project
![image](https://github.com/hlmiao/I-Day/blob/master/Devops/CICDforEKS/pic/019.png)
#### 1.2 Running the Project
![image](https://github.com/hlmiao/I-Day/blob/master/Devops/CICDforEKS/pic/020.png)
#### 1.3 Checking the build log
![image](https://github.com/hlmiao/I-Day/blob/master/Devops/CICDforEKS/pic/021.png)
#### 1.4 Waiting for build finished
![image](https://github.com/hlmiao/I-Day/blob/master/Devops/CICDforEKS/pic/022.png)
#### 1.5 Checking whether application has been deployed
![image](https://github.com/hlmiao/I-Day/blob/master/Devops/CICDforEKS/pic/023.png)
#### 1.6 Go to the Browser to check application
![image](https://github.com/hlmiao/I-Day/blob/master/Devops/CICDforEKS/pic/024.png)
#### 1.7 Updating the Code and push to code commit
```
[ec2-user@ip-172-31-89-175 templates]$ vim /tmp/eksworkshop-eksctl/templates/hello.html
```
#### 1.8 Checking the application has been updated
![image](https://github.com/hlmiao/I-Day/blob/master/Devops/CICDforEKS/pic/025.png)


