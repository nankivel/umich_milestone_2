
Package and Tool installations

- [AWS CLI](https://github.com/conda-forge/awscli-feedstock)


AWS CLI Configuration

S3 bucket is named `umichmilestone2nyd` and can be accessed via access key for IAM user `milestone2nyd`


Configure the AWS CLI with the key and region information to access the S3 bucket

```
➜  ~  aws configure

AWS Access Key ID [None]: 
AWS Secret Access Key [None]: 
Default region name [None]: us-east-2
Default output format [None]: json

```

In the repo's top level directory, Initialize DVC

```
➜  ~  dvc init
Initialized DVC repository.

You can now commit the changes to git.

+---------------------------------------------------------------------+
|                                                                     |
|        DVC has enabled anonymous aggregate usage analytics.         |
|     Read the analytics documentation (and how to opt-out) here:     |
|             <https://dvc.org/doc/user-guide/analytics>              |
|                                                                     |
+---------------------------------------------------------------------+

What's next?
------------
- Check out the documentation: <https://dvc.org/doc>
- Get help and share ideas: <https://dvc.org/chat>
- Star us on GitHub: <https://github.com/iterative/dvc>
```

Add the S3 bucket as the default DVC remote datastore

```
➜  ~  dvc remote add --default datastore s3://umichmilestone2nyd
Setting 'datastore' as a default remote.
```


