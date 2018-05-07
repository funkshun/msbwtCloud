## VM Startup
1. Create a new VM instance. We recommend a machine type of 2 virtual CPUs (vCPUs) with 52 GB memory, an Ubuntu 14.04 LTS OS, 
and SSD disk of 48 GB (dependent on the size of your msbwt, as a general rule add 10GB of memory to the size of your msbwt).
2. [Only needs to be done ONCE per project] Add a Firewall rule in Google Compute Engine to allow traffic to port 8080. Within the GPC dashboard, navigate to Networking --> VPC network --> Firewall rules. Add an ingress rule that filters on all IP ranges (`0.0.0.0/0`) and the 8080 port (`tcp:8080`).
  - Name you instance and provide a description
  - Network: default
  - Priority: 1000
  - Direction of traffic: Ingress
  - Action on match: Allow
  - Targets: All instances in the network
  - Source filter: IP ranges
  - Source IP ranges: `0.0.0.0/0`
  - Second source filter: None
  - Protocols and ports: Specified protocols and ports, `tcp:8080`
3. SSH into the VM.
4. Pull down the msbwtCloud startup script via: 
```
wget https://raw.githubusercontent.com/mnajarian/msbwtCloud/master/startup.sh
```
5. Run the startup script via: ```source startup.sh```. Navigate through the prompts. When prompted, enter a host server and msbwt location. For example:
```
mnajarian@csbio-desktop008.cs.unc.edu:/csbiodata/perlegen/CC_bwt/CC001M4363_UNC_NYGC/
```
6. Navigate to the msbwtCloud directory at ```cd ~/msbwtCloud```
7. (Optional) Create a logs directory
8. Start the server: ```nohup python core.py /playpen/[msbwtName] > logs/[logFile] & ```
