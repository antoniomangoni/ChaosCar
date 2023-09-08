# ChaosCar

Step 1: Install Anaconda
Download and install Anaconda from the official website.

Step 2: Open Anaconda Prompt
After the installation, open the Anaconda Prompt (on Windows) or terminal (on MacOS and Linux).

Step 3: Create a New Environment
Using the Anaconda Prompt or terminal, create a new environment using the YAML file environment.yaml.

conda env create -f environment.yaml

Step 4: Activate the New Environment
After creating the environment,  activate it using the following command:

conda activate env_name

Note: env_name would be the name of the environment specified in the YAML file.

Step 5: Verify the Installation
To verify that the environment was created correctly, use the following command to list all available environments:

conda env list

The new environment should appear in the list.

Step 6: Deactivate the Environment
Deactivate it using the following command:

conda deactivate
