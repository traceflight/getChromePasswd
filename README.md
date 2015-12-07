# getChromePasswd
>You can get all accounts and passwords saved by Google Chrome browser.
------

### Something to know...
Google Chrome browser save all users login data to ``C:\Users\%username%\AppData\Local\Google\Chrome\User Data\Default\Login Data``.
Sqlite is used to deal with them. The hosts and acocounts infomations are plain and only passwords are encrypted by win32crypt. So you can decrypt them on the target host. This is not a design deficiency as long as your Windows Operation is safe.

### Descripiton

*  *collector.py* runs on your machine. It sends command to target host to get chome password.
* *getpwd.py* runs on target machine. It gets chrome login data file, and decrypt it. Then send them to your host.

   (module requirement:    pywin32   )
 
   You should modify the IP address and port to your host.


### Existing problems

You have to turn off windows firewall, or you can use windows api to add your host ip to whitelist which is not difficult to do. 
