### 1.Create A Workspace
https://www.eksworkshop.com/020_prerequisites/workspace/
### 2.Pick the right Region，ap-southeast-1
https://www.eksworkshop.com/020_prerequisites/workspaceiam/
### 3.Setup EKS cluster (over 20 minutes)
https://www.eksworkshop.com/030_eksctl/launcheks/
### 4.CICD With Codepipeline
https://www.eksworkshop.com/intermediate/220_codepipeline/
### 5.Download zip file and upload to Cloud9
https://github.com/hlmiao/I-Day/blob/master/Devops/CICDforEKSv2/source/eks-workshop-sample-api-service-go-master.zip
### 6.Create CodeCommit Repository
```
TeamRole:~ $ cd /tmp
TeamRole:/tmp $ git clone https://git-codecommit.ap-southeast-1.amazonaws.com/v1/repos/eks-workshop
TeamRole:~/environment $ unzip -n eks-workshop-sample-api-service-go-master.zip -d /tmp/eks-workshop/
```
```
git status
git add .
git commit -am "1 Added all files"
git push
git status
```
### 7.Create CodePipeline
https://www.eksworkshop.com/intermediate/220_codepipeline/codepipeline/
