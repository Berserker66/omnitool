Translations
============

* Portuguese (BR)
    * by MiniManolinho
* English
    * by Berserker66
* German
    * by Berserker66
* Czech
    * by luksaman
* French
    * by Unknown
* Spanish
    * by Tyler
* Norwegian
    * by ManeFyre
* Japanese
    * by Unknown
* Danish
    * by SofusTheGreat
* Italian
    * by iMenchi
* Hungarian
    * by danzie
    
Contributing
============

In general, updates can be sent by using [Pull Requests](https://help.github.com/articles/using-pull-requests/)

Updating a Language
-------------------
On Github, grab the language file from [the list of languages](https://github.com/Berserker66/omnitool/tree/master/Language), 
save it as custom.py in your Omnitool installation.
As long as there is a `custom.py` in the Omnitool root directory, it will always use that language.

Now you can update this file and view the results by launching Omnitool. Iterate until you are satisfied.

To submit your update, make a pull request with your updated file. Please name it appropriately for the language and do not leave it as `custom.py`.

Adding a Language
-----------------
You should start by taking the [english.py](https://github.com/Berserker66/omnitool/blob/master/Language/english.py) file, it is usually the most up to date.

Save it as `custom.py` in your Omnitool installation and edit the English phrases into your language.

Unfortunately the GUI system cannot render the full range of unicode so please test if any special characters actually work.

Otherwise, proceed as in updating a language.

Other
-----
The language file can start with a  `__author__ = "name"` line. This indicates the current maintainer of the language and may later be displayed in the language menu.

If you do not want to use github pull requests, it also possible to send the file to [Berserker66 on the new forums](http://forums.terraria.org/index.php?members/berserker66.21440/) or [Ijwu on the old forums](http://www.terrariaonline.com/members/ijwu.14468/)
