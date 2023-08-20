/redoc/ GET <--- API DOCUMENTATION


/ GET Response: HTTP_200_OK

/ POST Payload:{
        "phone_number": "string",    |  required=True
        "password": "string",        |  required=False
        "invitation_code": "string"  |  required=False
        } 

       Response:{
        "phone_number": "string",
        "password": "string",
        "invitation_code": "string"
        } HTTP_200_OK


@is_authenticated  - authenticateion required
/profile/

/profile/ GET Response:{
               "phone_number": "string",
               "invited_by": "string",
               "invitation_code": "string"
              }

/profile/ POST Payload:{
                "invited_by": "string"  | required=False
               }
               Response:{
                "phone_number": "string",
                "invited_by": "string",
                "invitation_code": "string"
               } HTTP_200_OK


@is_authenticated  - authenticateion required
/logout/

/logout/ GET HTTP_200_OK
