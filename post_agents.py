"""
This is a full gotten agent:
{
  "lock_version": 2,
  "publish": false,
  "created_by": "admin",
  "last_modified_by": "admin",
  "create_time": "2015-07-21T14:57:58Z",
  "system_mtime": "2015-07-24T16:57:04Z",
  "user_mtime": "2015-07-24T16:57:02Z",
  "jsonmodel_type": "agent_person",
  "agent_contacts": [
    {
      "lock_version": 0,
      "name": "Dallas Pillen",
      "address_1": "22505 Glenwood",
      "city": "Clinton Twp",
      "region": "MI",
      "country": "United States",
      "telephone": "5868505580",
      "email": "djpillen@umich.edu",
      "note": "This is a contact note.",
      "created_by": "admin",
      "last_modified_by": "admin",
      "create_time": "2015-07-24T16:57:03Z",
      "system_mtime": "2015-07-24T16:57:03Z",
      "user_mtime": "2015-07-24T16:57:03Z",
      "jsonmodel_type": "agent_contact"
    }
  ],
  "linked_agent_roles": [

  ],
  "external_documents": [

  ],
  "notes": [

  ],
  "dates_of_existence": [

  ],
  "donor_details": [
    {
      "lock_version": 0,
      "number": "1234",
      "number_auto_generate": false,
      "dart_id": "8888",
      "created_by": "admin",
      "last_modified_by": "admin",
      "create_time": "2015-07-24T16:57:03Z",
      "system_mtime": "2015-07-24T16:57:03Z",
      "user_mtime": "2015-07-24T16:57:03Z",
      "jsonmodel_type": "donor_detail"
    }
  ],
  "names": [
    {
      "lock_version": 0,
      "primary_name": "Pillen",
      "prefix": "Mr.",
      "rest_of_name": "Dallas J.",
      "sort_name": "Pillen, Dallas J., Mr.",
      "sort_name_auto_generate": true,
      "created_by": "admin",
      "last_modified_by": "admin",
      "create_time": "2015-07-24T16:57:03Z",
      "system_mtime": "2015-07-24T16:57:03Z",
      "user_mtime": "2015-07-24T16:57:03Z",
      "authorized": true,
      "is_display_name": true,
      "rules": "dacs",
      "name_order": "inverted",
      "jsonmodel_type": "name_person",
      "use_dates": [

      ]
    }
  ],
  "related_agents": [

  ],
  "uri": "\/agents\/people\/2",
  "agent_type": "agent_person",
  "display_name": {
    "lock_version": 0,
    "primary_name": "Pillen",
    "prefix": "Mr.",
    "rest_of_name": "Dallas J.",
    "sort_name": "Pillen, Dallas J., Mr.",
    "sort_name_auto_generate": true,
    "created_by": "admin",
    "last_modified_by": "admin",
    "create_time": "2015-07-24T16:57:03Z",
    "system_mtime": "2015-07-24T16:57:03Z",
    "user_mtime": "2015-07-24T16:57:03Z",
    "authorized": true,
    "is_display_name": true,
    "rules": "dacs",
    "name_order": "inverted",
    "jsonmodel_type": "name_person",
    "use_dates": [

    ]
  },
  "title": "Pillen, Dallas J., Mr.",
  "is_linked_to_published_record": false
}
"""



"""
This is a successfully posted agent person:


{
  "agent_contacts": [
    {
      "name": "Harry Potter",
      "address_1": "4 Privet Drive",
      "city": "London?",
      "country": "England",
      "telephone": "8675309",
      "email": "hpotter@hogwarts.edu",
      "note": "the boy who lived"
    }
  ],
  "donor_details": [
    {
      "number": "2000",
      "dart_id": "5555"
    }
  ],
  "names": [
    {
      "primary_name": "Potter",
      "prefix": "Mr.",
      "rest_of_name": "Harry J",
      "sort_name_auto_generate": true,
      "source": "local",
      "name_order": "inverted"
    }
  ]
}

This is what ASpace returns:

{"status":"Created","id":7,"lock_version":0,"stale":true,"uri":"/agents/people/7","warnings":[]}

"""
