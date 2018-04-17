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
   
4. Get streams recommended for a user
   GET /streams/recommendations/<<userid>>
   
   E.g. http://127.0.0.1:5000/streams/recommendations/958
   The response from the service is of the below format:
   ```json
	{
    "RecommendedStreams": [
    {
      "streamid": "675",
      "organization": "28",
      "streamname": "Storytelling Skills",
      "order": 0,
      "tags": [
        "Training",
        "Overcoming Objections",
        "Win Story",
        "Manufacturing"
      ],
      "cards": [
        {
          "cardid": "4661",
          "cardname": "?????? ????? ?????"
        },
        {
          "cardid": "4662",
          "cardname": "?????? ????? ?????"
        },
        {
          "cardid": "4663",
          "cardname": "????? ?????? ?????"
        },
        {
          "cardid": "4664",
          "cardname": "??? ????? ??? ?????? ??? ????? ???"
        },
        {
          "cardid": "4665",
          "cardname": "??? ????? ??? ?????? ??? ????? ???"
        },
        {
          "cardid": "4666",
          "cardname": "??? ????? ??? ?????? ??? ????? ???"
        }
      ]
    },
    {
      "streamid": "762",
      "organization": "28",
      "streamname": "Ch?p h\ufffdnh tuy?t ??p m?i l\ufffdc",
      "order": 3,
      "tags": [
        "Product Feature",
        "Overcoming Objections",
        "Quiz"
      ],
      "cards": [
        {
          "cardid": "3701",
          "cardname": "Ch?p h\ufffdnh tuy?t ??p m?i l\ufffdc v?i Nokia 5"
        },
        {
          "cardid": "3702",
          "cardname": "Ch?p h\ufffdnh tuy?t ??p m?i l\ufffdc v?i Nokia 6"
        },
        {
          "cardid": "3703",
          "cardname": "?ng d?ng Google Photos"
        },
        {
          "cardid": "3704",
          "cardname": "?ng d?ng Google Photos"
        },
        {
          "cardid": "3705",
          "cardname": "photos.google.com"
        },
        {
          "cardid": "3706",
          "cardname": "photos.google.com"
        },
        {
          "cardid": "3707",
          "cardname": "Ch?p selfie tuy?t ??p v?i Nokia 3"
        },
        {
          "cardid": "3708",
          "cardname": "Ch?p h\ufffdnh ??p v\ufffdo m?i th?i ?i?m"
        }
      ]
    },
    {
      "streamid": "768",
      "organization": "28",
      "streamname": "??i t??ng KH & ?i?m nh?n SP",
      "order": 1,
      "tags": [
        
      ],
      "cards": [
        {
          "cardid": "3517",
          "cardname": "Th? h? tr? c?n g\ufffd tr\ufffdn m?t chi?c ?i?n tho?i"
        },
        {
          "cardid": "3518",
          "cardname": "??i t??ng kh\ufffdch h\ufffdng ?i?n tho?i th\ufffdng minh Nokia"
        },
        {
          "cardid": "3519",
          "cardname": "Nokia 3310 ??i t??ng kh\ufffdch h\ufffdng"
        },
        {
          "cardid": "3520",
          "cardname": "Th? h? tr? s?ng c\ufffd m?c ?\ufffdch"
        },
        {
          "cardid": "3521",
          "cardname": "Selfie tuy?t ??p v?i Nokia 3"
        },
        {
          "cardid": "3522",
          "cardname": "Kh\ufffdch h\ufffdng v\ufffd ?i?m nh?n b\ufffdn h\ufffdng"
        }
        ]
      }
     ]
    }
   ```