In order to upload this application just type "docker-compose up --build"

In order to access the api got to "http://localhost:5000/api/devices"

POST

GET does no require any params

GET /:id get by id requires "id" (device id)

DELETE /:id switches {"deleted": True} by (device id)

PATCH /:id (device id) updated {"description": "..."} (from json payload) It updates only description because this is the only
field that is allowed to updated by the instructions.



