
## Package and Tool installations


[AWS CLI](https://github.com/conda-forge/awscli-feedstock) Configuration

S3 bucket is named `umichmilestone2nyd` and can be accessed via access key for IAM user `milestone2nyd`


Configure the AWS CLI with the key and region information to access the S3 bucket

```
$ aws configure

AWS Access Key ID [None]: 
AWS Secret Access Key [None]: 
Default region name [None]: us-east-2
Default output format [None]: json

```

In the repo's top level directory, Initialize DVC

```
$ dvc init
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
$ dvc remote add --default datastore s3://umichmilestone2nyd
Setting 'datastore' as a default remote.
```

Add the /data directory for DVC to manage

```
$ dvc add data
Computing md5 for a large file '/github/umich_milestone_2/data/raw/outpatient.pkl'. This is only done once.                                                                           
100% Adding...|███████████████████████████████████████████████████████████|1/1 [00:21, 21.29s/file]
                                                                                                                                    
To track the changes with git, run:                                                                                                 
                                                                                                                                    
	git add data.dvc .gitignore

To enable auto staging, run:

	dvc config core.autostage true
```

Commit the DVC related files to git

```
$ git status
Changes to be committed:
        new file:   .dvc/.gitignore
        new file:   .dvc/config
        ...
$ git commit -m "Initialize DVC"
```


Push data to the remote S3 bucket when you have local changes to data you want to commit

```
$ dvc push
 25% Transferring|████████████████████▊                                  |1/4 [00:01<00:03,  1.26s/file]
  5%|▌         |/github/umich_milestone_2/data/raw/outpatient.pkl500M/9.55G [09:24<2:53:19,     935kB/s]
 58%|█████▊    |/github/umich_milestone_2/data/raw/inpatient.pkl500M/868M [09:16<06:49,     942kB/s]
```

## Troubleshooting

If you have a DVC push that is terminated because of a connection issue or you had to terminate it, you may see this when trying to dvc push again:

```
$ dvc push
ERROR: failed to push data to the cloud - Unable to acquire lock. 
Most likely another DVC process is running or was terminated abruptly. 
Check the page <https://dvc.org/doc/user-guide/troubleshooting#lock-issue>
 for other possible reasons and to learn how to resolve this.
```

Removing the .dvc/tmp/lock file manually should allow you to do another push

```
$ rm .dvc/tmp/lock
  0% Transferring|                                                                                       |0/2 [00:00<?,     ?file/s]
  5%|▌         |/Users/nankivel/umich/umich_milestone_2/.dvc/cache/d3/793de9ba07ea9c485476e3e500M/9.55G [04:04<1:13:51,    2.20MB/s]
```

