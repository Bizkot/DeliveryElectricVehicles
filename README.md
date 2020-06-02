# DeliveryElectricVehicles
The goal here is to minimize the number of vehicles used to do a tour to deliver clients.
It is also to maximize the number of client delivered. If some clients are not delivered, we're applying a penalty.
## Installation
```bash
git clone https://github.com/Bizkot/DeliveryElectricVehicles.git
cd DeliveryElectricVehicles
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```
Test the server by pinging [localhost](http://127.0.0.1:8000/api)

## Testing a heuristic
To test a heuristic you need to use an API request builder such as Postman.

You need 5 elements to perform a test:
* The route/URL to the heuristic
* A visit file
* A distance file
* A time file
* A vehicle configuration file

![Postman example 1](images/postman_1.png)

The important point here is that you must have the same "Key" as on the image:
* visits for the visit file
* distance for the distance file
* times for the time file
* vehicle for the vehicle configuration file

## Heuristic list
### api/firstheuristic
The first heuristic only uses 1 vehicle. It loops through the visit list and check if the vehicle has enough:
* energy
* time
* capacity

to go from the previous visit to the next one and also to go back to the depot.
Whenever the vehicle is lacking one of these components, the tour stops and the heuristic is completed.

### api/secondheuristic
The second heuristic uses unlimited amount of vehicles and add one vehicle to the tour if one of the above component is lacking.