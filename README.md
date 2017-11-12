## VM Startup
1. Create a new VM instance. We recommend a machine type of 2 virtual CPUs (vCPUs) with 52 GB memory, an Ubuntu 14.04 LTS OS, 
and SSD disk of 48 GB (dependent on the size of your msbwt).
2. SSH into the VM.
3. Pull down the msbwtCloud startup script via: ```wget https://raw.githubusercontent.com/mnajarian/msbwtCloud/master/startup.sh```
4. Run the startup script via: ```bash startup.sh```. Navigate through the prompts. When prompted, enter a host server and msbwt location 
(for example, ```mnajarian@csbio-desktop008.cs.unc.edu:/csbiodata/perlegen/CC_bwt/CC001M4363_UNC_NYGC/```
5. Navigate to the msbwtCloud directory at ```cd ~/msbwtCloud```
6. (Optional) Create a logs directory
7. Start the server: ```nohup python core.py /playpen/[msbwtName] > logs/[logFile] & 
