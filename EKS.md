# EKS

## Create cluster

### Without nodegroup

```bash
eksctl --profile <profile> \
	create cluster \
 	--name <my-cluster> \
 	--version <1.21> \
 	--region <region>
 	--with-oidc \
 	--without-nodegroup
```



## Create kubeconfig for cluster (Connect to your cluster)

1. Update kubeconfig for cluster

   ```bash
   aws --profile <profile> eks --region <region-code> update-kubeconfig --name <cluster_name>
   ```

2. Test config

   ```bash
   kubectl get svc
   ```

## Delete cluster

```bash
eksctl --profile <profile> delete cluster --name <cluster_name> --region <region>
```

## Create managed node group

### Without a launch template

```bash
eksctl create nodegroup \
	--profile <profile>
  --cluster <my-cluster> \
  --region <us-west-2> \
  --name <my-mng> \
  --node-type <m5.large> \
  --nodes <3> \
  --nodes-min <2> \
  --nodes-max <4> \
  --ssh-access \
  --ssh-public-key <my-key> \
  --managed
```

## Autoscaling

If cluster nodegroup created with eksctl,

1. Save the following to a file named `cluster-autoscaler-policy.json`.

   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Action": [
                   "autoscaling:DescribeAutoScalingGroups",
                   "autoscaling:DescribeAutoScalingInstances",
                   "autoscaling:DescribeLaunchConfigurations",
                   "autoscaling:DescribeTags",
                   "autoscaling:SetDesiredCapacity",
                   "autoscaling:TerminateInstanceInAutoScalingGroup",
                   "ec2:DescribeLaunchTemplateVersions"
               ],
               "Resource": "*",
               "Effect": "Allow"
           }
       ]
   }
   ```

   

2. Create a policy

   ```bash
   aws --profile <profile> iam create-policy \
       --policy-name <AmazonEKSClusterAutoscalerPolicy> \
       --policy-document file://cluster-autoscaler-policy.json
   ```

3. Note the ARN that is returned

4. Create IAM role and attach policy to it

   ```bash
   eksctl --profile <profile> create iamserviceaccount \
     --cluster=<my-cluster> \
     --region=<region> \
     --namespace=kube-system \
     --name=cluster-autoscaler \
     --attach-policy-arn=arn:aws:iam::<AWS_ACCOUNT_ID>:policy/<AmazonEKSClusterAutoscalerPolicy> \
     --override-existing-serviceaccounts \
     --approve
   ```

5. Deploy the Cluster Autoscaler (for production, should optimise: https://docs.aws.amazon.com/eks/latest/userguide/cluster-autoscaler.html#ca-deployment-considerations)

   ```bash
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/autoscaler/master/cluster-autoscaler/cloudprovider/aws/examples/cluster-autoscaler-autodiscover.yaml
   ```

6. Annotate Cluster Autoscaler service account with ARN of the IAM role

   ```bash
   kubectl annotate iamserviceaccount cluster-autoscaler \
     -n kube-system \
     eks.amazonaws.com/role-arn=arn:aws:iam::<ACCOUNT_ID>:role/<AmazonEKSClusterAutoscalerRole>
   ```

7. Patch the deployment to add the `cluster-autoscaler.kubernetes.io/safe-to-evict` annotation

   ```bash
   kubectl patch deployment cluster-autoscaler \
     -n kube-system \
     -p '{"spec":{"template":{"metadata":{"annotations":{"cluster-autoscaler.kubernetes.io/safe-to-evict": "false"}}}}}'
   ```

8. Edit Cluster Autoscaler deployment

   ```bash
   kubectl -n kube-system edit deployment.apps/cluster-autoscaler
   ```

9. Replace `<YOUR CLUSTER NAME>` with cluster name, and add these options:
   `--balance-similar-node-groups`
   `--skip-nodes-with-system-pods=false`
   E.g

   ```yaml
       spec:
         containers:
         - command:
           - ./cluster-autoscaler
           - --v=4
           - --stderrthreshold=info
           - --cloud-provider=aws
           - --skip-nodes-with-local-storage=false
           - --expander=least-waste
           - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/<YOUR CLUSTER NAME>
           - --balance-similar-node-groups
           - --skip-nodes-with-system-pods=false
   ```

   Save

10. From Cluster Autoscaler releases page on Github, find version that matches Kubernetes cluster version. E.g. if K8s version is 1.21, must use Autoscaler version that starts with 1.21, ie 1.21.n

11. Set the Cluster Autoscaler image tag to the corresponding version

    ```bash
    kubectl set image deployment cluster-autoscaler \
      -n kube-system \
      cluster-autoscaler=k8s.gcr.io/autoscaling/cluster-autoscaler:v<1.21.n>
    ```

12. View Autoscaler logs to verify it is monitoring

    ```bash
    kubectl -n kube-system logs -f deployment.apps/cluster-autoscaler
    ```

    

