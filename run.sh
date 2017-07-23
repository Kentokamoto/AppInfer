#!/bin/bash 
# Auto run the python script for all cases

apps=("Amex"
"BankOfAmerica"
"CapitalOne"
"Chase"
"CitiMobile"
"Discover"
"Facebook"
"Messenger"
"PayPal"
"Snapchat"
"Spotify"
"Twitter"
"Uber"
"USAA"
"USBank"
"Venmo"
"Waze"
"WellsFargo"
"WhatsApp"
"Yelp")

for i in "${apps[@]}"
do
	python CleanData2.py ${i}
done
