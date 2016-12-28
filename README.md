# kube-ec2-node-labeling
Kubernetes node labeling through EC2 tags

## Overview

This application takes a VPC ID and uses it to retrieve the labels of the nodes in the Kubernetes cluster it's running by querying the EC2 API. It uses that information to map those to Kubernetes labels in the nodes metadata.

## Assumptions

This assumes that all the nodes in the Kubernetes cluster exist in the same VPC, which is the one defined in the environment as `$VPC_ID`.

## Requirements

The service account running this application needs `cluster-admin` privileges to be able to update the Kubernetes Node object.

The default template included with the application (`app.yaml`) creates a service account called `node-labeler`. You can grant it the `cluster-admin` role so it just works by running `oadm policy add-cluster-role-to-user cluster-admin system:serviceaccount:NAMESPACE:node-labeler` (replacing `NAMESPACE` with the name of the namespace you're running this application) as a cluster administrator.

The application requires you to create a secret called `aws-config` with AWS credentials with permissions to describe EC2 instances, and to authorize the `node-labeler` service account to use it:

```bash
$ oc secrets new aws-config ~/.aws
$ oc secrets add --for=mount serviceaccount/node-labeler secret/aws-config
```
