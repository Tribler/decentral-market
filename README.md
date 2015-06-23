# tsukiji
Tsukiji is a decentralised market. Users can create bids and asks in a decentralised manner, similar to bittorrent. Without a central point of failure, it will prove more resistant to hostile takeover. Tsukiji is still a proof-of-concept in the early stages of development.

Tsukiji market is also the largest fish and seafood market in the world, located in Tokyo.

# Running tests
```bash
nosetests --with-coverage --cover-branches --cover-package=tsukiji --cover-html --cover-erase --nocapture
```

* ```--with-coverage```               Activate statement coverage
* ```--cover-branches```              Activate branch coverage
* ```--cover-package=tsukiji```       Cover only tsukiji
* ```--cover-html```                  Display coverage data in html files instead of printing. Files go in the cover/ directory.
* ```--cover-erase```                 Erase previous coverage data
* ```--nocapture```                   Do not capture stdout
