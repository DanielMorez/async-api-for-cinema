def generate_persons_list() -> list:
    person_data = [
    {
      'id': '578593ee-3268-4cd4-b910-8a44cfd05b73',
      'name': 'Rafael Ferrer',
      'gender': 'male',
      'roles_names': ['actor'],
      'films_names': ['NeverLand'],
      'films': [
        {'id': '2a090dde-f688-46fe-a9f4-b781a985275e', 'title': 'NeverLand'}
      ]
    },
    {
      'id': '2802ff93-f147-49cc-a38b-2f787bd2b875',
      'name': 'John Cygan',
      'gender': 'male',
      'roles_names': ['actor'],
      'films_names': ['Movie 43', 'NeverLand'],
      'films': [
          {'id': '64aa7000-698f-4332-b52f-9469e4d44ee1', 'title': 'Movie 43'},
          {'id': '2a090dde-f688-46fe-a9f4-b781a985275e', 'title': 'NeverLand'}
        ],
    },
    {
      'id': '55dc3cfa-0731-42fe-9d7b-6180b00ab712',
      'name': 'Giuseppe Tornatore',
      'gender': None,
      'roles_names': ['director, writer'],
      'films_names': ['The Star'],
      'films': [
        {'id': '7159c8c2-b9a4-410a-965b-1096b8d1e614', 'title': 'The Star'}
      ]
    },
    {
      'id': 'c740cb33-df3a-4aeb-b3ad-7e79581d857c',
      'name': 'Fabio Rinaudo',
      'gender': 'female',
      'roles_names': ['actor', 'producer'],
      'films_names': ['The Star', 'NeverLand'],
      'films': [
          {'id': '7159c8c2-b9a4-410a-965b-1096b8d1e614', 'title': 'The Star'},
          {'id': '2a090dde-f688-46fe-a9f4-b781a985275e', 'title': 'NeverLand'}
      ],
    },
    {
      'id': 'f142081a-8054-4ec3-ae97-026f8ebdef3e',
      'name': 'Tiziana Lodato',
      'gender': None,
      'roles_names': ['actor'],
      'films_names': ['The Star'],
      'films': [
          {'id': '7159c8c2-b9a4-410a-965b-1096b8d1e614', 'title': 'The Star'}
      ],
    },
    {
      'id': 'a88f14e6-a8e2-4e05-9744-e89fadf960fb',
      'name': 'Franco Scaldati',
      'gender': 'male',
      'roles_names': ['actor'],
      'films_names': ['The Star'],
      'films': [
          {'id': '7159c8c2-b9a4-410a-965b-1096b8d1e614', 'title': 'The Star'}
      ],
    },
    {
      'id': '6d5964ff-e56e-40aa-9e30-6a52ed741e55',
      'name': 'Leopoldo Trieste',
      'gender': 'male',
      'roles_names': ['actor'],
      'films_names': ['The Star'],
      'films': [
          {'id': '7159c8c2-b9a4-410a-965b-1096b8d1e614', 'title': 'The Star'}
      ],
    },
    {
      'id': '8fadd3bf-c272-4b84-be93-0f85f0a0767e',
      'name': 'Ry Russo-Young',
      'gender': None,
      'roles_names': ['director'],
      'films_names': ['Alice in Wonderland'],
      'films': [
          {'id': '523f1a55-51fe-4d3c-a58d-30d8a61bb267', 'title': 'Alice in Wonderland'}
      ],
    },
    {
      'id': 'caf06d3f-19dc-4b7d-8aff-c0cbe7b643d0',
      'name': 'Tracy Oliver',
      'gender': None,
      'roles_names': ['writer'],
      'films_names': ['Alice in Wonderland'],
      'films': [
          {'id': '523f1a55-51fe-4d3c-a58d-30d8a61bb267', 'title': 'Alice in Wonderland'}
      ],
    },
    {
      'id': '54eec180-2bcc-4016-a8d5-13cfcd4a447c',
      'name': 'Nicola Yoon',
      'gender': None,
      'roles_names': ['writer'],
      'films_names': ['Alice in Wonderland'],
      'films': [
          {'id': '523f1a55-51fe-4d3c-a58d-30d8a61bb267', 'title': 'Alice in Wonderland'}
      ],
    },
   {
      'id': '828bd349-45a5-4428-9754-13467884fa88',
      'name': 'Yara Shahidi',
      'gender': 'female',
      'roles_names': ['actor'],
      'films_names': ['Alice in Wonderland'],
      'films': [
          {'id': '523f1a55-51fe-4d3c-a58d-30d8a61bb267', 'title': 'Alice in Wonderland'}
      ]
   },
   {
      'id': '8d253d20-cbe5-4d35-8378-801ddebe77b8',
      'name': 'Anais Lee',
      'gender': None,
      'roles_names': ['actor'],
      'films_names': ['Alice in Wonderland'],
      'films': [
          {'id': '523f1a55-51fe-4d3c-a58d-30d8a61bb267', 'title': 'Alice in Wonderland'}
      ]
   },
   {
      'id': '7ed70fca-4f3e-40ee-b2dd-fc9e11dc218a',
      'name': 'Charles Melton',
      'gender': None,
      'roles_names': ['actor'],
      'films_names': ['Alice in Wonderland'],
      'films': [
          {'id': '523f1a55-51fe-4d3c-a58d-30d8a61bb267', 'title': 'Alice in Wonderland'}
      ]
   },
   {
      'id': '17b36cf5-6f85-4f98-a8b5-7ab6eab58d51',
      'name': 'John Leguizamo',
      'gender': None,
      'roles_names': ['actor'],
      'films_names': ['Alice in Wonderland'],
      'films': [
          {'id': '523f1a55-51fe-4d3c-a58d-30d8a61bb267', 'title': 'Alice in Wonderland'}
      ]
   },
   {
      'id': '28f8edaf-9c20-4fc2-914a-da04c15c88cc',
      'name': 'Anthony Mann',
      'gender': None,
      'roles_names': ['director'],
      'films_names': ['Episod IV'],
      'films': [
          {'id': '8a96580a-6b7b-422e-b4fb-694eaa269ff7', 'title': 'Episod IV'}
      ],
    },
    {
      'id': 'ad12504e-1bb3-4805-ab87-2e84147e2a64',
      'name': 'Joel Kane',
      'gender': None,
      'roles_names': ['writer'],
       'films_names': ['Episod IV'],
      'films': [
          {'id': '8a96580a-6b7b-422e-b4fb-694eaa269ff7', 'title': 'Episod IV'}
      ],
    },
    {
      'id': 'a2a5cf96-1f78-4742-95c8-e8eeef8974ee',
      'name': 'Dudley Nichols',
      'gender': None,
      'roles_names': ['writer'],
       'films_names': ['Episod IV'],
      'films': [
          {'id': '8a96580a-6b7b-422e-b4fb-694eaa269ff7', 'title': 'Episod IV'}
      ],
    },
    {
      'id': '2b841691-00d9-4000-8175-178fd0bb7d5b',
      'name': 'Barney Slater',
      'gender': None,
      'roles_names': ['writer'],
       'films_names': ['Episod IV'],
      'films': [
          {'id': '8a96580a-6b7b-422e-b4fb-694eaa269ff7', 'title': 'Episod IV'}
      ],
    },
    {
      'id': 'ca283661-e10a-49d7-958c-164782cb351c',
      'name': 'Henry Fonda',
      'gender': None,
      'roles_names': ['actor'],
      'films_names': ['Episod IV', 'The War'],
      'films': [
          {'id': '8a96580a-6b7b-422e-b4fb-694eaa269ff7', 'title': 'Episod IV'},
          {'id': 'c2383393-0a55-4717-be0d-6adea3fc43bf', 'title': 'The War'}
      ],
    },
    {
      'id': '6d632920-025b-4e66-aae0-9ba6abaf648c',
      'name': 'Anthony Perkins',
      'gender': None,
      'roles_names': ['actor'],
       'films_names': ['Episod IV'],
      'films': [
          {'id': '8a96580a-6b7b-422e-b4fb-694eaa269ff7', 'title': 'Episod IV'}
      ],
    },
    {
      'id': '035bc2f6-05d3-42a0-b820-bdea903ada05',
      'name': 'Betsy Palmer',
      'gender': None,
      'roles_names': ['actor'],
       'films_names': ['Episod IV'],
      'films': [
          {'id': '8a96580a-6b7b-422e-b4fb-694eaa269ff7', 'title': 'Episod IV'}
      ],
    },
    {
      'id': 'e2fb90a8-45c5-4dfd-9205-29f74d1ddb03',
      'name': 'Michel Ray',
      'gender': None,
      'roles_names': ['actor'],
       'films_names': ['Episod IV'],
      'films': [
          {'id': '8a96580a-6b7b-422e-b4fb-694eaa269ff7', 'title': 'Episod IV'}
      ],
    },
    {
      'id': '5a1e12da-2c5a-4042-bc73-478cd010bb7c',
      'name': 'Hugh Davidson',
      'gender': 'female',
      'roles_names': ['writer'],
      'films_names': ['Jedy', 'Fith element'],
      'films': [
          {'id': '830857b7-64d2-4a95-98c4-b03351daff52', 'title': 'Jedy'},
          {'id': 'd1099968-805e-4a2b-a2ec-18bbde1201ac', 'title': 'Fith element'}
      ],
    },
    {
      'id': 'aa8d115c-aa99-469d-8035-5637f1f03fbf',
      'name': 'Dan Milano',
      'gender': 'male',
      'roles_names': ['writer'],
       'films_names': ['Jedy', 'Fith element'],
      'films': [
          {'id': '830857b7-64d2-4a95-98c4-b03351daff52', 'title': 'Jedy'},
          {'id': 'd1099968-805e-4a2b-a2ec-18bbde1201ac', 'title': 'Fith element'}
      ],
    },
    {
      'id': 'a3487d4e-49f2-4f3e-8951-2c5b0bf7cc0b',
      'name': 'Kevin Shinick',
      'gender': 'male',
      'roles_names': ['writer'],
       'films_names': ['Jedy', 'Fith element'],
      'films': [
          {'id': '830857b7-64d2-4a95-98c4-b03351daff52', 'title': 'Jedy'},
          {'id': 'd1099968-805e-4a2b-a2ec-18bbde1201ac', 'title': 'Fith element'}
      ],
    },
    {
      'id': 'ce3edce4-a7c2-482a-854c-db8dee853ee6',
      'name': 'Zeb Wells',
      'gender': None,
      'roles_names': ['writer'],
       'films_names': ['Jedy', 'Fith element'],
      'films': [
          {'id': '830857b7-64d2-4a95-98c4-b03351daff52', 'title': 'Jedy'},
          {'id': 'd1099968-805e-4a2b-a2ec-18bbde1201ac', 'title': 'Fith element'}
      ],
    },
    {
      'id': '746b394f-7808-4386-a281-b06504c07b58',
      'name': 'Ahmed Best',
      'gender': None,
      'roles_names': ['actor'],
      'films_names': ['Casper', 'Jedy', 'Fith element'],
      'films': [
           {'id': '569e23df-7e00-459d-b92a-6cb4653d36b8', 'title': 'Casper'},
           {'id': '830857b7-64d2-4a95-98c4-b03351daff52', 'title': 'Jedy'},
           {'id': 'd1099968-805e-4a2b-a2ec-18bbde1201ac', 'title': 'Fith element'}
       ],
    },
    {
      'id': 'e73f46a4-cf53-4b12-b5da-52503b6319f7',
      'name': 'Haden Blackman',
      'gender': 'male',
      'roles_names': ['director, writer'],
      'films_names': ['Casper', 'Kolombiana', 'Star Dust'],
      'films': [
           {'id': '569e23df-7e00-459d-b92a-6cb4653d36b8', 'title': 'Casper'},
           {'id': '3cb639db-cd8a-48b0-90e3-9def109a4492', 'title': 'Kolombiana'},
           {'id': 'ed2fb2c4-faea-4d1c-b1e0-a49973e21698', 'title': 'Star Dust'}
       ],
    },
    {
      'id': 'c098fec8-851b-4946-b6bc-c1142236ed12',
      'name': 'Steve Stamatiadis',
      'gender': None,
      'roles_names': ['director'],
      'films_names': ['Kolombiana'],
      'films': [
           {'id': '3cb639db-cd8a-48b0-90e3-9def109a4492', 'title': 'Kolombiana'},
       ],
    },
    {
        'id': 'c098fec8-851b-4946-b6bc-c1042236ed12',
        'name': 'Claire Catherine Danes',
        'gender': 'female',
        'roles_names': ['actor'],
        'films_names': ['Star Dust'],
        'films': [
            {'id': 'ed2fb2c4-faea-4d1c-b1e0-a49973e21698', 'title': 'Star Dust'}
        ],
    }
    ]
    return person_data