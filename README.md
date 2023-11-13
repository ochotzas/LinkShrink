# LinkShrink

Meet LinkShrink, a straightforward URL shortener built with Python using Flask. It's super basic, but it gets the job done.

No need to sign up. Just click on your link or hit the button on the main page to see how popular it is. Only you, the link creator, can see how many visits it's getting, thanks to your IP address. Quick heads up: once a link is made, it's here to stay. You can't delete it (at least not yet). Check out all your links on the "Your Shortened URLs" page.

And here's a twist - every link comes with an expiration date. When it's time's up, it won't vanish, but it'll be labeled as expired in the database. Easy peasy!

## Installation

Clone the repository and install the requirements:

```bash
git clone https://github.com/ochotzas/LinkShrink.git
cd LinkShrink
pip install -r requirements.txt
```

## Usage

Run the server:

```bash
python run.py
```

## Note

- Some code is not optimized as it is not intended to be used in production.
- In the templates folder, things could have been more organized, but I didn't want to spend more time on that.
- The project is using a JSON file as a database as it is not intended to be used in production. It's easy to switch to a real NoSQL database like MongoDB, for example.


## License
**What is [MIT](https://choosealicense.com/licenses/mit/) License?** The MIT license is a permissive free software license originating at the Massachusetts Institute of Technology (MIT) in the late 1980s. As a permissive license, it puts only very limited restriction on reuse and has, therefore, high license compatibility. The MIT license permits reuse within proprietary software provided all copies of the licensed software include a copy of the MIT License terms and the copyright notice.

### Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

--

Made with ❤️ by Olger Chotza, Thessaloníki, Greece.