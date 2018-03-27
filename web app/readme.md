#### Dependencies
1. Flask - pip install flask



#### How to execute the application

### Update the path to the database
1. Navigate to configurations.py file in the services folder
2. Update the value in the variable db_location to the location where your database (.db) file is present

### Run the service 

1. python /path_to_app.py_in_service_folder/app.py
2. Navigate to the URL in your browser that is shown in the console when executing 1

### Service endpoints

1. Get views by user id: 
   GET /views/<<user_id>> 
   
   E.g. http://127.0.0.1:5000/views/1007

2. Add new view of user: 
   
   POST /views/add  
   Request header: Content-Type:application/json  
   Request body:  
   
   ```json
   {
	"userid":"1007",
	"streamid":"561",
	"moduleid":"491",
	"cardid":"8889"
   }
   ```
   
   E.g. http://127.0.0.1:5000/views/add  
     
   Note: A text response is sent which can be checked for errors. A text of "OK" is sent for success, else an error text is returned.
   
3. Get details of a stream: 
   
   GET /streams/neighbors/<<stream_id>>
   
   E.g. http://127.0.0.1:5000/streams/neighbors/580
   The response from the service is of the below format:
   ```json
	{
      "Target": {
      "streamid": "580",
      "organization": "28",
      "streamname": "Nokia 6",
      "tags": [
        "Nokia 6"
      ],
      "cards": [
       {
         "cardid": "3029",
         "cardname": "Nokia 6 Colours"
       },
       {
         "cardid": "9394",
         "cardname": "Nokia 6 Outside & Inside"
       }
      ]
    },
      "Neighbors": [
      {
        "streamid": "683",
        "organization": "28",
        "streamname": "Nokia 6",
        "tags": [
          "Nokia 6"
        ],
        "cards": [
          {
            "cardid": "4548",
            "cardname": "Nokia 6 ????? ????"
          },
          {
            "cardid": "4549",
            "cardname": "Nokia 6 ???????? ???????? ?????"
          }
        ]
      },
      {
        "streamid": "704",
        "organization": "28",
        "streamname": "Nokia 6",
        "tags": [
          "Nokia 6"
        ],
        "cards": [
        {
          "cardid": "3713",
          "cardname": "Nokia 6 : les accessoires"
        },
        {
          "cardid": "3714",
          "cardname": "Nokia 6 : contenu du coffret"
        }
        ]
       }
      ]
    }
   ```