Azure Batch Compute Setup
=========================
The goal of setting up this Azure Batch is to run a python script on an Azure Compute Node. My personal server is small in memory size, and increasing that capacity incurs a higher cost that is not quite necessary for current usage. Only the python script that needs to be run takes up a lot of memory when running, thus for one-time or periodic basis, the Azure Batch comes into play.

## Requirements
The main requirements are Python and an Azure account (there is a free tier that can be taken advantage of for first 12-months by first-time users). I also run Django on my server, so that makes it easier for me to deploy jobs and test scripts making use of the Django views.

### Python Requirements
Python library requirements to run the Azure batch and blob:

*  azure-batch
*  azure-storage-blob

run: `python -m pip install azure-batch azure-storage-blob` in environment. Batch Task below will do the same on the Azure compute node.

### Azure Requirements
Sign up a Blob Storage account and a Batch account in [Azure Portal](https://portal.azure.com/#home)

Documentation can be found here:

*  [Azure Blob Storage](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction)
*  [Azure Batch](https://docs.microsoft.com/en-us/azure/batch/batch-technical-overview)

## Batch Setup
Setting up the batch requires setting up pools, nodes, jobs and tasks. Written in python, the client needs called in order to access the setup for other components.

### Batch Client
Fairly straight forward. Credentials are found on the Azure Portal -- under Batch (account) > Keys.
```python
def createBatchClient():

    credentials = batch_auth.SharedKeyCredentials(os.environ.get('AZURE_BATCH_ACCOUNT_NAME'), os.environ.get('AZURE_BATCH_ACCOUNT_KEY'))
    batch_client = batch.BatchServiceClient(credentials, batch_url=os.environ.get('AZURE_BATCH_ACCOUNT_URL'))

    return batch_client
```

### Batch Pool
When creating the pool, specify the number of nodes and also any starting commands (Start Task). There can only be one start task, but commands can be appended with `&&` as needed. The `vm_size` can be found on the [VM Size](https://docs.microsoft.com/en-us/azure/cloud-services/cloud-services-sizes-specs) page.
```python
def createBatchPool(batch_client, pool_id):

    start_cmd = "/bin/bash -c \"add-apt-repository universe && apt-get update && apt-get install -y python3 python3-pip python3-venv\""
    admin = batchmodels.UserIdentity(auto_user=batchmodels.AutoUserSpecification(elevation_level='admin'))

    new_pool = batch.models.PoolAddParameter(
        id=pool_id,
        virtual_machine_configuration=batchmodels.VirtualMachineConfiguration(
            image_reference=batchmodels.ImageReference(
                publisher="Canonical",
                offer="UbuntuServer",
                sku="18.04-LTS",
                version="latest"
            ),
            node_agent_sku_id="batch.node.ubuntu 18.04"),
        vm_size='STANDARD_A2m_v2',   # VM Type/Size
        target_dedicated_nodes=1,    # pool node count
        start_task=batchmodels.StartTask(command_line=start_cmd, user_identity=admin)
    )
    batch_client.pool.add(new_pool)
```
To set `StartTask` and enable that task to run as `sudo` or *admin* user, see documentation:

*  [Pool Add Parameter](https://docs.microsoft.com/en-us/python/api/azure-batch/azure.batch.models.pooladdparameter?view=azure-python)
*  [Start Task](https://docs.microsoft.com/en-us/python/api/azure-batch/azure.batch.models.starttask?view=azure-python)
*  [User Identity](https://docs.microsoft.com/en-us/python/api/azure-batch/azure.batch.models.useridentity?view=azure-python)
*  [Auto User Specification](https://docs.microsoft.com/en-us/python/api/azure-batch/azure.batch.models.autouserspecification?view=azure-python)

### Batch Job
The batch job is assigned to the pool to handle the tasks within it.
```python
def createBatchJob(batch_client, job_id, pool_id):

    job = batch.models.JobAddParameter(
        id=job_id,
        pool_info=batch.models.PoolInformation(pool_id=pool_id),
        uses_task_dependencies=True)
    batch_client.job.add(job)
```

Setting the `uses_task_dependencies` allows for task dependencies which is specified with `depends_on` field in each Task in the following section.

*  [Task Dependencies](https://docs.microsoft.com/en-us/python/api/azure-batch/azure.batch.models.taskdependencies?view=azure-python)

### Batch Task
Tasks are assigned to each node or all nodes (depends how to set it). In this case, only 1 node, so all tasks are assigned to the same node.
```python
def createTasks(batch_client, job_id, input_files, filenames):

    tasks = list()

    # Environment Variables
    acc_name = batchmodels.EnvironmentSetting(name='AZURE_BLOB_ACCOUNT_NAME',
                                              value=os.environ.get('AZURE_BLOB_ACCOUNT_NAME'))
    acc_key = batchmodels.EnvironmentSetting(name='AZURE_BLOB_ACCOUNT_KEY',
                                             value=os.environ.get('AZURE_BLOB_ACCOUNT_KEY'))

    # input_file = input_files[0]
    req_file = filenames[0]
    # for idx, input_file in enumerate(input_files):
    task_commands = [
        # install latest requirements
        "/bin/bash -c \"python3 -m venv env && source env/bin/activate && " +
        "python3 -m pip install -r {} && ".format(req_file) +

        # print pip list
        "python3 -m pip list && " +

        # run the python script
        "python3 -m calculate_hexgrid_standalone && deactivate\""
    ]

    # Task 0 -- do everything
    tasks.append(batch.models.TaskAddParameter(
        id='Task{}'.format(0),
        command_line=task_commands[0],
        resource_files=input_files,
        environment_settings=[acc_name, acc_key]
    ))

    # add tasks to task collection
    batch_client.task.add_collection(job_id, tasks)
```

Adding parameters to the task creates the task, then add to collection for it to be run. The environment settings can be added to the task to use *environment variables*.

*  [Task Add Parameters](https://docs.microsoft.com/en-us/python/api/azure-batch/azure.batch.models.taskaddparameter?view=azure-python)
*  [Environment Settings](https://docs.microsoft.com/en-us/python/api/azure-batch/azure.batch.models.environmentsetting?view=azure-python)

### Views.py
One method of testing out the functionality is to run it in a Django view.
```python
...

    container = getContainerClient(input_container_name)
    print("Container Retrieved.")

    # Upload Input Files
    filenames = ['requirements.txt',
                 'hexgrid_constructor.py',
                 'calculate_hexgrid_standalone.py',
                 'blank_HexGrid-126_24_-66.5_50r15.json',
                 'stations_2020-01-01.json']
    input_files = uploadInputFiles(container, input_container_name, 'BatchCompute/data', filenames, blob_name, False)
    print("INPUT FILES:", input_files)

    # Create a Batch service client. We'll now be interacting with the Batch service in addition to Storage
    batch_client = createBatchClient()

    try:
        # Create Batch Pool that will contain the compute nodes to execute tasks
        createBatchPool(batch_client, os.environ.get('POOL_ID'))

        # Create Batch Job to run tasks
        createBatchJob(batch_client, os.environ.get('JOB_ID'), os.environ.get('POOL_ID'))

        # Add the tasks to the job.
        createTasks(batch_client, os.environ.get('JOB_ID'), input_files, filenames)

        # Pause execution until tasks reach Completed state.
        waitTaskCompletion(batch_client, os.environ.get('JOB_ID'), dte.timedelta(minutes=120))

        print("  Success! All tasks reached the 'Completed' state within the "
              "specified timeout period.")

        # Print the stdout.txt and stderr.txt files for each task to the console
        printTaskOutput(batch_client, os.environ.get('JOB_ID'))

    except batchmodels.BatchErrorException as err:
        printBatchException(err)

...
```

### Reviewing Progress
While the program is running, the `sys.stdout.flush()` command will print the log to the `stdout.txt` file, but will not print it to the screen running Django. To check on the progress of the job and tasks, navigate to Azure Portal > Batch Account > Jobs > Task, and open up the `stdout.txt` file for preview as below.
![Azure Batch Task](/static/img/markdowns/azure_batch_task.JPG)


## Documentation and Resource Links
*  [QuickStart Python Azure Batch](https://docs.microsoft.com/en-us/azure/batch/quick-run-python)
*  [Install python3-pip on Ubuntu](https://stackoverflow.com/questions/52394543/pip-install-problem-with-ubuntu-18-04-and-python-3-6-5)