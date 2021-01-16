# AutoDataBasics
Simplifies Timesheet Entry for DataBasics Timesheets. This should make it much easier to submit your timesheets without having to deal with DataBasics' UI.

Tested in Windows only so far.

### Requirements:
* A Python **3.6+** environment
* Selenium (can be installed using ``pip install selenium``)

### Setup:
* Clone this repository into a dedicated directory (the ``adb.py`` file is really the only thing you need).
* Download the **[Selenium Chrome driver](https://chromedriver.chromium.org/downloads)** and place the executable file in the same directory alongside ``adb.py``
* Create an ``auth.txt`` file with 3 lines: The **URL** for your DataBasics login page, your **username** and your **password**. Example:
```
https://xxx.data-basics.net/xxx/databasics.ext#
sergiome@gmail.com
p455w0rd
```
* On DataBasics, **[create as many Favorite/Memorized](https://databasics.atlassian.net/wiki/spaces/PG6/pages/526544/Favorites+Timesheet) rows as you will need** to cover your timesheet entries. For example, create one for your project, one for vacations, one for meetings, and so on.

### Filling your Timesheet
Anytime you want to fill your timesheet, prepare a ``timesheet.txt`` file following the format detailed below and place it in the same directory as the script, auth and driver. Each line in this file corresponds to a timesheet entry, with its values separated by commas. 

The first value of every line is the **position of the favorite/memorized entry to be used for this line, as displayed in your Favorites table, starting from 0** (see the picture below for an example). You may need to login to DataBasics and look at your Favorites table to figure out what number each Favorite corresponds to.

<img src="https://i.imgur.com/WpdlWMN.png" width=550>

The rest of the values of each line are self-explanatory: The second value is the entry note/description, and the following 5 values are the time values from Monday to Friday. 

Example: 
```
0, This is a note for an entry that uses the favorite in the FIRST row (e.g. project work), 1,5,0,6,6
1, This is a note for an entry using the favorite in SECOND row (e.g. vacations), 7,0,0,0,0
1, This is a note for another entry that uses the favorite in the SECOND row (more vacations), 0,0,8,0,0
2, Finally this note is for an entry using the favorite in the THIRD row (e.g. meetings), 0,3,0,2,2
```
(This is a CSV file and is ingested as one, so feel free to use your favorite CSV Editor to prepare it!)

### Execution:
Just execute the script!

```python adb.py```

If all goes well, you should see a Chrome window open, and the entire process will be automated. Once finished, **review your timesheet** and submit! **This script does not auto-submit your timesheet**. You have to press that button yourself :)

### Optional: Using Aliases:
You can set up an **alias file** to replace the numeric row values for your Favorites with the words of your choosing, like "project", "meeting" or "vacations". Simply create an ``alias.txt`` file in the same directory as the script with the mappings specified like so:
```
project:0
vacations:1
meetings:2
```
Then you can uses those aliases instead of the numbers in your timesheet file:
```
project, This is a note for an entry that uses the project favorite, 1,5,0,6,6
vacations, This is a note for an entry using the vacations favorite, 7,0,0,0,0
vacations, This is a note for another entry that uses the vacations favorite, 0,0,8,0,0
meetings, Finally this note is for an entry using the meetings favorite, 0,3,0,2,2
```

---

### For Developers:

If you want to build a UI for this, change the input file format or extend it in any other way, it should be fairly easy to do. You can just import the script and use the ``runDataBasics`` function, which receives the **login url**, **username**, **password** and **timesheet lines** which is a list of dict/json objects with ``fav``, ``note`` and ``times`` attributes. **Aliases** are submitted through the optional ``alias`` parameter as a dictionary of ``str`` keys and ``int`` values.

Example:
``` py
import adb

db_url = ...
username = ...
password = ...

alias_dict = {"project":0, "meetings":1}

ts = [{"fav":"project", "note":"this is a note", "times":[1,1,2,4,5]},
      {"fav":"meetings", "note":"this is another note", "times":[2,2,3,1,1]},
      {"fav":"project", "note":"this is a third note", "times":[1,1,0,0,0]}]
 
 adb.runDataBasics(db_url, username, password, ts, alias=alias_dict)
 ```
