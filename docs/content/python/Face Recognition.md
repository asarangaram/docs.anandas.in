---
title: Face Recognition
---

# Face Recognition

## APIs to build database

| End point                    | Description                                                                                                                                                                                                                                                           |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| POST /faces                  | Registers a new face and associates it with a person.<br>`image_file`: The face image<br>`person_name`: person's name<br>`person_id`: person's ID<br>either `person_name` or `person_id` must be provided, not both<br>Returns <br>face_id, person_id = both non null |
| PUT /persons/{person_id}     | Updates a person's information<br>`name`:  to rename a person (optiona)<br>`is_hidden`: boolean to set or hide the person<br>`key_face_id`: face ID to be set as the key face                                                                                         |
| PUT /faces/{face_id}         | Updates the person associated with this face. <br>`person_name`: person's name<br>`person_id`: person's ID <br>either `person_name` or `person_id` must be provided, not both                                                                                         |
| DELETE /faces/{face_id}      | Deletes the face from the database                                                                                                                                                                                                                                    |
| DELETE  /persons/{person_id} | Deletes the person and all the faces associated with.                                                                                                                                                                                                                 |

## Query APIs

|                             |                                                                                                                   |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| GET /persons                | Retrieves a list of all person records. For each person, it includes the face id list<br>Response: List\<Person\> |
| GET /persons/{person_id}    | Retrieves a person's record along with all face ids associated with that person<br>Response:Person                |
| GET /faces/{face_id}/person | returns the ID of the person associated with that face<br>Response:Person                                         |
| GET /faces/{face_id}        | download the face image<br>Resonse: Image                                                                         |

## Detect Face 

|                 |                                                                                  |
| --------------- | -------------------------------------------------------------------------------- |
| GET /faces/scan | accept a single image and return information about every face detected within it |
|                 |                                                                                  |
