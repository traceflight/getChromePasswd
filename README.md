# getChromePasswd

You can get others' accounts and passwords saved by Google Chrome browser.


### Something to know...
Google Chrome browser save all users login data to ``C:\Users\%username%\AppData\Local\Google\Chrome\User Data\Default\Login Data``.
Sqlite is used to maintain them. The hosts and acocounts infomations are plain and only passwords are encrypted by win32crypt. So you can decrypt them on the target host. This is not a design deficiency as long as your Windows Operation is safe.

### Descripiton

*  *collector.py* runs on your machine. It sends command to target host to get chome password.
* *getpwd.py* runs on target machine. It gets chrome login data file, and decrypt it. Then send them to your host.
   (module requirement:    [pywin32](http://sourceforge.net/projects/pywin32/)   
   You need to modify the IP address and port.
   You can also use [py2exe](http://www.py2exe.org/) or [pyinstaller](https://github.com/pyinstaller/pyinstaller/) to convert *getpwd.py* to a single Windows exe, so that it can run on a pc without python.
   Besides, you can design a specific Get_URL to get any file in target machine.


### Existing problems

1. You have to turn off windows firewall of target machine, or you can use windows api to add your host ip to target machine's whitelist which is not very difficult to do. 
2. The key problem is how to let others run *getpwd.py* (or exe). Phishing ? Or something like it.
