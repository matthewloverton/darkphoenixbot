# Dark Phoenix

One man's desire to have ALL of the Marvel Strike Force information in one place, it's not perfect i'll admit but for those of you who use discord I hope you'll find it useful.

Due to Foxnext's lack of an API I manually converted most of the information on [msf.gg](https://msf.gg/) into json format, which in hindsight was very painful. I have many ideas and plans for more interactive options with this bot including a website frontend where you can view/update your roster and access it from discord using !profile. Though that would be difficult to regulate without official account information pulled from an API (Please beg foxnext for more developer tools!).

### Prerequisites

This project uses Python 3.7. To install the prerequisites you'll need pip for Python 3.

```
discord.py - pip3 install discord.py
tinydb - pip3 install tinydb
```

## Deployment

The official Dark Phoenix Bot uses environment variables set up through Heroku, if you'd like to run it for personal use you can set up heroku yourself with the correct environment variables or alternatively switch the way the variables are loaded in bot.py.

## Built With

* [discord.py](https://github.com/Rapptz/discord.py) - The bot framework
* [tinydb](https://tinydb.readthedocs.io/en/latest/) - Database Management


## Authors

* **Matthew Overton** - *Initial work* - [theHoncho](https://github.com/theHoncho)

See also the list of [contributors](github.com/theHoncho/darkphoenixbot/contributors) who participated in this project.

## License

This project is licensed under the MIT License.

## Acknowledgments

* [OriannaBot](https://github.com/molenzwiebel/OriannaBot) - A discord.js bot for league of legends.
* [msf.gg](https://msf.gg/) - A website with a TON of information about MSF.