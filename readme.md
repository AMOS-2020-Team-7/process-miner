# PSD2Miner
AMOS Project Team 7 (SS 2020)
## Mining Open-Banking Processes
Our application allows business which develop multi-banking gateways to optimize and perfect their workflows. In this way they are able to deliver the most reliable and easy to use product to the end user.

Our web application analyzes the concrete implementation of the process 'Get Transactions' at different banks. It provides visualization of connections and implications of individual implementations.


## Software Architecture
<br><center><img src="/backend/docs/software_architecture.png" alt="Software Architecture" width="700"/></center></br>


## Deployment
The PSD2Miner may be deployed using `docker-compose`. In order to be able to do this certain values in the file `docker-compose.yaml` need to be modified:
* `GRAYLOG_URL` - hostname of the Graylog instance that should be used to retrieve logs from
* `GRAYLOG_API_TOKEN` - API token that is required for accessing the Graylog instance
* `BACKEND_HOST` - hostname of the machine that will run the backend
* `BACKEND_PORT` - number of the port that exposes the backend