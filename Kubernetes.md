# Kubernetes

[TOC]

## kubectl

### Get lists

```bash
kubectl get <item>
```

For:

* `deployments`
* `pods`
* `services`
* ReplicaSets: `rs`

### Describe

```bash
kubectl describe <item>
```



### Create a deployment

### Create a namespace

```bash
kubectl create namespace <namespace>
```



### Deploy a manifest

```bash
kubectl apply -f <manifest_file>
```

### Expose a service

### Scale ReplicaSet

```bash
kubectl scale deployments/<deployment_name> --replicas=<num_replicas>
```

### Updating

#### Update deployment

```bash
kubectl set image deployments/<deployment_name> <pod_name>=<image_name>:<image_version_tag>
```

e.g.

```bash
kubectl set image deployments/kubernetes-bootcamp kubernetes-bootcamp=jocatalin/kubernetes-bootcamp:v2
```

#### Check rollout status

````bash
kubectl rollout status deployments/<deployment_name>
````

#### Rollback

```bash
kubectl rollout undo deployments/<deployment_name>
```

### Restarting

#### Deployments

```bash
kubectl rollout restart deployment/<deployment_name>    
```



### Accessing pods

#### Access container shell
```bash
kubectl exec -it <pod_name> --container <container_name> -- /bin/bash
````

## Configuration files

### Parts

1. metadata - including kind of item
2. ## specification
3. status - auto-generated and added by k8s

### Format

### Multiple configs in one file

If you have multiple deployments, services, and secretes that need to be set up for your cluster, you can include all in one file.

Separate each config with

```yaml
---
```



## Environment variables

Passed to containers via:

1. ConfigMap (for non-sensitive data)
2. Secret (for passwords)

These can both passed directly to the k8s cluster via config files. For Secrets, must be passed as base64-encoded strings

Secrets must be created BEFORE the deployments

### Use ConfigMap as environment variable

```yaml
containers:
    - name: test-container
      image: k8s.gcr.io/busybox
      command: [ "/bin/sh", "-c", "env" ]
      env:
        # Define the environment variable
        - name: SPECIAL_LEVEL_KEY
          valueFrom:
            configMapKeyRef:
              # The ConfigMap containing the value you want to assign to SPECIAL_LEVEL_KEY
              name: special-config
              # Specify the key associated with the value
              key: special.how
```



## Services

Provides:

* Persistent stable IP address
* Load-balancing between pods in a replicaset
* 

### Types

`ClusterIP`: Internal service, exposed to other services within the cluster only. Default type

`LoadBalancer`: Exposed to external access

`NodePort`: Service that is accessible on a fixed port on each worker node. Requests will not route via ingress component.

`Headless`: When pods want to speak to specific pods. Set `clusterIP` to `None`.

### External service

Assign type `LoadBalancer`. This assigns an external IP to the service.

The cluster still needs to handle assigning an IP on external network to the service.

E.g. `minikube service <external-service`, will provision IP and port and open in browser.

#### Ports

`port`: Port exposed by service

`targetPort`: Pod exposed by pod

For multiple ports, we need to have a `name` attribute for each.

### Forwarding requests

Using selectors. Use key-value pairs (`labels`) to identify pods

### Endpoints

K8s creates Endpo

## Namespaces

Like a virtual cluster inside your cluster.

May not need for smaller project.

But useful for 

* Grouping resources in large projects
* Multiple teams working on same cluster
* Staging and development in separate namespaces

Can also limit resources on each namespace.

Each namespace defines its own configmap and secrets

But services can be accessed from other namespaces

Volumes and nodes cannot be assigned to a namespace

kubectl by default uses `default` namespce

we can specify namespace with

```bash
kubectl <commands> -n <namespace>
# E.g.
kubectl get deployments -n <namespace>
```

Or can specify in config files.

## Ingress

In production, instead of using external service, we should use an ingress component

In Ingress component, we define rules for paths, redirecting paths to services.

We can use ingress component to configure HTTPS 

To implement ingress, we need to also have an ingress controller, which runs as a pod on its own

Many third party implementations

From k8s itself, default is Nginx ingress controller

### In minikube

```bash
minikube addons enable ingress
```

You can spoof a domain name by inserting in hosts file

### In cloud

Request -> Cloud load balancer -> Ingress

### With TLS

Store in secret, `type: kubernetes.io/tls`

Actual file contents in base64 are in the secret

Must be in same namespace as ingress component

## Helm charts

Bundles of yaml files

You can also define common blueprint for config files, with variables that can be fetched from external configuration

You could use this to manage different environments e.g. Staging, production, development,

Use the same config yaml, but pass different variables in

Normally values from value.yml. But you can provide an override file that overrides only specified values.

## Kubernetes Volumes

### Persistent Volumes

Specified by YAML file.

Specify how much storage etc.

Specifications can be specific to the storage type, e.g. local, AWS EBS, NFS etc.

Persistent volumes are not namespaced - available to entire cluster

#### Persistent Volume Claim

Claim by a service on a Persistent Volume

The claim must be mentioned in the Pod configuration

Claims _are_ namespaced.

### ConfigMap and Secrets

Are also volume types.

### StorageClass

Provisions storage dynamically. Whenever a claim requests it.

Requuires a provisioner backend e.g. EBS

## StatefulSet

 Stateless applications managed using deployments,

but Statefull applications managed using StatefulSets.

Configure pods and storage the same way

But StatefulSet maintains a sticky identifier for each pod, even on spin down and spin up.

They also don't have access to the same storage - they each have their own storage.

Pod identifiers are stored in the pod's volumes.

StatefulSet pods get fixed ordered names, e.g. mysql-0, mysql-1, mysql-2 etc.

All the pods use 

1. Single service
2. Plus their own individual service names