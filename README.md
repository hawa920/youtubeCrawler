# youtubeCrawler
A simple youtube page infos crawler implemented in Python3 with Selenium and BS4. Crawler is actually just a part of this project, what comes after it is much more exciting and challenging
## Basic Structure (Prototype)
![](https://i.imgur.com/l99kR92.png)

## Multi-thread Programming
Now the class supported multi-thread programming, you can simply create a class object in your thread functions and have them all work together. 

I suggest users write the records crawled to files after the function 'goCrawl()' is done to reduce the number of times to lock/release the lockers.

## Persistence
In order to keep going on the previous work progress next time you launch the crawler, you can keep the urlQueue and SeenDB into binary files using pickle, and load them in your program next time you launch it.

As for the details, please refer to /src/main.py  
