python-pipedrive
================

Python library for interacting with the pipedrive.com API


This is being developed for my specific use so there's no guarantee I'll cover all of the aspects of the Pipedrive API. Feel free to add features though, I welcome pull requests.

All features should be supported though as this is just a lightweight wrapper around the API.


Usage:

Create a Pipedrive object, passing either the api key or your username and password as the parameters

	from pipedrive import Pipedrive
	pipedrive = Pipedrive(USERNAME, PASSSWORD)

or

	from pipedrive import Pipedrive
	pipedrive = Pipedrive(API_KEY)

The rest of the functions relate to the URL as specified in the [API Docs](https://app.pipedrive.com/docs/auth/login).

E.g. to add a deal:

    pipedrive.deal_add({"deal[title]": "My deal", "deal[value]": 1000, # etc....