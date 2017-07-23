#! /bin/bash

for i in $(seq -f "%02g" 1 30)
do
	mv Paypal$i.pcapng PayPal$i.pcapng
done

