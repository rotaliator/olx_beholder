# Olx Beholder ;)
Simple watcher and email notifier for recent OLX offers

## Usage

required python >=3.6

	$ git clone https://github.com/rotaliator/olx_beholder.git	
	$ cd olx_beholder
	$ pip install bs4 requests pyhiccup
	$ cp olx_beholder.ini.sample olx_beholder.ini

Set SMTP and message settings in `olx_beholder.ini`
	
Go to [http://olx.pl](http://olx.pl), specify query filter, copy generated url and append it to file `urls.txt`. Each url should be in new line.

Run `python olx_beholder.py` in cron task.


## License

Copyright © 2019 rotaliator

Released under the MIT license.
