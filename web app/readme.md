#### Dependencies
1. Flask - pip install flask



#### How to execute the application

### Set up the data base and load the data - Note this DB needs to be dropped on completion of the project
1. Install SQLite and add it to path. Please follow this: https://www.tutorialspoint.com/sqlite/sqlite_installation.htm
2. Run the below set of commands to import data from CSV to a .db file for SQLite 3

Navigate to the folder with the data CSVs and then type the below one by one in a sqlite3 prompt
   1. .mode csv
   2. .open <db_name>.db
   3. .import <<input_file>>.csv <<db_name>>
   4. .schema <<input_file>>

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
        "cardid": "3030",
        "cardname": "Nokia 6 Companion Products"
      },
      {
        "cardid": "3033",
        "cardname": "Nokia 6 Sales package"
      },
      {
        "cardid": "3034",
        "cardname": "Nokia 6 Sales Pitch"
      },
      {
        "cardid": "3059",
        "cardname": "Nokia 6 Key Selling Points"
      },
      {
        "cardid": "6239",
        "cardname": "Nokia 6 vs Competition"
      },
      {
        "cardid": "6240",
        "cardname": "Nokia 6 vs Samsung J7 Prime"
      },
      {
        "cardid": "6241",
        "cardname": "Nokia 6 vs Vivo v5"
      },
      {
        "cardid": "6242",
        "cardname": "Nokia 6 vs Oppo F1s LTE"
      },
      {
        "cardid": "6243",
        "cardname": "Nokia 6 vs Asus Zenfone 3 Max"
      },
      {
        "cardid": "6244",
        "cardname": "Nokia 6 vs LG K520"
      },
      {
        "cardid": "7571",
        "cardname": "Nokia 6 Training Video"
      },
      {
        "cardid": "7706",
        "cardname": "Nokia 6 Quiz"
      },
      {
        "cardid": "9031",
        "cardname": "Nokia 6 Design & Craftsmanship"
      },
      {
        "cardid": "9032",
        "cardname": "Nokia 6 Always the Latest Android"
      },
      {
        "cardid": "9033",
        "cardname": "Nokia 6 Ready to Entertain"
      },
      {
        "cardid": "9034",
        "cardname": "Nokia 6 Capture Your Best in Class Pictures"
      },
      {
        "cardid": "9393",
        "cardname": "Nokia 6 Outside & Inside"
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
        },
        {
          "cardid": "4550",
          "cardname": "Nokia 6 ???? ????"
        },
        {
          "cardid": "4551",
          "cardname": "Nokia 6 ????? ??? ????"
        },
        {
          "cardid": "4553",
          "cardname": "Nokia 6 ???? ????? ???????? ?????"
        },
        {
          "cardid": "4554",
          "cardname": "Nokia 6"
        },
        {
          "cardid": "5233",
          "cardname": "?????? ????? 6"
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
        },
        {
          "cardid": "3715",
          "cardname": "Nokia 6 : discours de vente"
        },
        {
          "cardid": "3717",
          "cardname": "Nokia 6 : les points cl\ufffds"
        },
        {
          "cardid": "5215",
          "cardname": "Nokia 6 : Le Quizz"
        },
        {
          "cardid": "6333",
          "cardname": "Le Nokia 6 : sp\ufffdcifications"
        }
      ]
    },
    {
      "streamid": "761",
      "organization": "28",
      "streamname": "Nokia 6",
      "tags": [
        "Nokia 6"
      ],
      "cards": [
        {
          "cardid": "3503",
          "cardname": "M\ufffdu s?c c?a Nokia 6"
        },
        {
          "cardid": "3504",
          "cardname": "Nokia 6 c\ufffdc ph? ki?n c\ufffd th? mua k\ufffdm"
        },
        {
          "cardid": "3505",
          "cardname": "Nokia 6 B? s?n ph?m"
        },
        {
          "cardid": "3506",
          "cardname": "Nokia 6 Th\ufffdng ?i?p b\ufffdn h\ufffdng"
        },
        {
          "cardid": "3508",
          "cardname": "Nokia 6 ?i?m nh?n b\ufffdn h\ufffdng"
        },
        {
          "cardid": "3509",
          "cardname": "Nokia 6"
        },
        {
          "cardid": "5224",
          "cardname": "Ki?m tra ki?n th?c Nokia 6"
        },
        {
          "cardid": "9467",
          "cardname": "So s\ufffdnh Nokia 6 v\ufffd Samsung J7 Prime"
        },
        {
          "cardid": "9468",
          "cardname": "So s\ufffdnh Nokia 6 v\ufffd Oppo F1s (2017)"
        },
        {
          "cardid": "9469",
          "cardname": "So s\ufffdnh Nokia 6 v\ufffd Huawei GR5 2017 Pro"
        },
        {
          "cardid": "9470",
          "cardname": "So s\ufffdnh Nokia 6 v\ufffd Vivo VY69"
        }
      ]
    },
    {
      "streamid": "775",
      "organization": "28",
      "streamname": "Nokia 6",
      "tags": [
        "Nokia 6"
      ],
      "cards": [
        {
          "cardid": "5428",
          "cardname": "Nokia 6 Sales Pitch"
        },
        {
          "cardid": "5429",
          "cardname": "Nokia 6 Key Selling Points"
        },
        {
          "cardid": "5430",
          "cardname": "Nokia 6 Sales package"
        },
        {
          "cardid": "5431",
          "cardname": "Nokia 6 Colours"
        },
        {
          "cardid": "5432",
          "cardname": "Nokia 6 Companion Products"
        },
        {
          "cardid": "5433",
          "cardname": "Nokia 6 Quiz"
        }
      ]
    },
    {
      "streamid": "879",
      "organization": "28",
      "streamname": "Nokia 6",
      "tags": [
        "Nokia 6"
      ],
      "cards": [
        {
          "cardid": "3921",
          "cardname": "Warna Nokia 6"
        },
        {
          "cardid": "3922",
          "cardname": "Produk pendukung Nokia 6"
        },
        {
          "cardid": "3923",
          "cardname": "Paket Penjualan Nokia 6"
        },
        {
          "cardid": "3924",
          "cardname": "Nokia 6 Sales Pitch"
        },
        {
          "cardid": "3925",
          "cardname": "Nokia 6 Quiz"
        },
        {
          "cardid": "3926",
          "cardname": "Nilai Jual Utama Nokia 6"
        },
        {
          "cardid": "3927",
          "cardname": "Nokia 6"
        },
        {
          "cardid": "4800",
          "cardname": "Nokia 6 Quiz"
        }
       ]
      }
     ]
   }
   ```