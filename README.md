Current version : 18.4.0, for Terraria 1.3.3.1 on Windows and Linux.

On the Terraria Forums:
[Link](http://forums.terraria.org/index.php?threads/omnitool-world-creation-mapping-backups-and-more.14664/)

[![Build Status](https://travis-ci.org/Berserker66/omnitool.svg?branch=master)](https://travis-ci.org/Berserker66/omnitool)

Features
========
* Makes world backups on launch.
* Maps worlds on launch.
* Render worlds with 16x16 textures for each block.
* Contains world generators: Planetoids & Terra, Worldify, Flatworld and PVP Dungeon Arena.
* Update notification.
* Linking of other tools (tedit, terrafirma).
* Works with GameLauncher GUI
* Plugin system for extensions.

![Main Menu](https://cloud.githubusercontent.com/assets/3189725/9048286/4926664e-3a38-11e5-94a3-78ea5a750c54.png)

![World Render Function](https://cloud.githubusercontent.com/assets/3189725/9121177/f7ad474c-3c80-11e5-8402-1add361a6cf0.png)

Usage
=====

* Download a matching version for your operating System from the Releases Tab.
* Install & Run
* [optional] drag & drop a tedit exe file onto omnitool.exe, to access tedit from within omnitool
* [optional] drag & drop a terrafirma exe file onto omnitool.exe, to access terrafirma from within omnitool

FAQ
===
Is there a better way to view my world as a map?
------------------------------------------------
You can render a world similar to how Terraria shows them by clicking on a world's image.
This also allows you to create a super image of the world as [website](https://dl.dropboxusercontent.com/u/44766482/superimage/index.html).

Do I need admin rights to use Omnitool?
---------------------------------------
No

Where do I report issues or ideas?
---------------------------------------
Either as a Github issue or on the forums. Both require an account unfortunately.

Available Languages
===================

* Portuguese (BR)
* English
* German
* Czech
* French
* Spanish
* Norwegian
* Japanese
* Danish
* Italian
* Hungarian
* Russian

More detailed info in the [Translation Readme](translation.md) and Language thread [here](http://www.terrariaonline.com/threads/omnitool-language-thread.62981/).

Plugins
-------
More plugins to add features to Omnitool can be found [here](http://www.terrariaonline.com/threads/omnitool-plugin-compendium.82677/#post-1625952).
You can also check out the [documentation](http://www.terrariaonline.com/threads/omnitool-plugin-system-documentation.80960/) to make your own.

Currently the plugin system is unstable, as updating of all systems to Terraria 1.3 continues. Plugins may or may not work.

Dependencies
============

This is only needed, if you want to run Omnitool from source code.
The dependencies can be grabbed through pip using the requirements.txt file.
That is "pip install -r requirements.txt".
Depending on your Python installation, you may need to run one of these instead:
* `py -3 -m pip install -r requirements.txt`. (likely case for windows)
* `python3 -m pip install -r requirements.txt`. (likely case for linux)

For some of the modules, additional packages are required for download.

That is subversion for PGU and mercurial for Pygame.
In Ubuntu this can be satisfied with:
* `sudo apt-get install mercurial`
* `sudo apt-get install subversion`

Credits for Omnitool
====================
* 7UR7L3: testing and ideas
* Ijwu: translation overseer, testing, ideas & skins (Oasis, Underworld, Overworld)
* Berserker66: programming, testing, bundling, setup, ....
* Translation credits in translation thread: [Link](http://www.terrariaonline.com/threads/omnitool-language-thread.62981/)

Other
=====
[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=JBZM8LFAGDK4N), [Patreon](https://www.patreon.com/Berserker55) or [Steam Wishlist](http://steamcommunity.com/profiles/76561198041949197/wishlist/)
