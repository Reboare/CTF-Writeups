```
eployment# nikto -h http://34.201.73.166/
- Nikto v2.1.6
---------------------------------------------------------------------------
+ Target IP:          34.201.73.166
+ Target Hostname:    34.201.73.166
+ Target Port:        80
+ Start Time:         2018-02-10 14:42:30 (GMT-5)
---------------------------------------------------------------------------
+ Server: Apache/2.4.7 (Ubuntu)
+ Server leaks inodes via ETags, header found with file /, fields: 0x44c 0x564a0f28b70b4 
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ Apache/2.4.7 appears to be outdated (current is at least Apache/2.4.12). Apache 2.0.65 (final release) and 2.2.29 are also current.
+ Allowed HTTP Methods: OPTIONS, GET, HEAD, POST 
+ OSVDB-3233: /icons/README: Apache default file found.
+ OSVDB-3092: /.git/index: Git Index file may contain directory listing information.
+ /.git/HEAD: Git HEAD file found. Full repo details may be present.
+ /.git/config: Git config file found. Infos about repo details may be present.
+ 7535 requests: 0 error(s) and 10 item(s) reported on remote host
+ End Time:           2018-02-10 14:55:00 (GMT-5) (750 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested
```

```
git log -p
diff --git a/3e90c63922fa145442bb58d18b62af6c21717fee/index.php b/3e90c63922fa145442bb58d18b62af6c21717fee/index.php
deleted file mode 100644
index 2fe7e98..0000000
--- a/3e90c63922fa145442bb58d18b62af6c21717fee/index.php
+++ /dev/null
@@ -1,35 +0,0 @@
-<html>
-    <head>
-        <link rel="stylesheet" type="text/css" media="screen" href="style.css" />
-    </head>
-    <body>
-    <form class="login" method="post">
-    <h1 class="login-title">Login for flag</h1>
-        <input name="user" id="user" type="text" class="login-input" placeholder="Username" autofocus>
-        <input name="pass" id="pass" type="password" class="login-input" placeholder="Password">
-        <input type="submit" value="Lets Go" class="login-button">
-
-
-  <?php
-error_reporting(0);
-$FLAG = readfile('/var/flags/level1.txt');
-if (!empty($_POST['user']) && !empty($_POST['pass'])) {
-    if(checklogin($_POST['user'],$_POST['pass'])){
-        echo "<font style=\"color:#FF0000\"><h3>The flag is: $FLAG</h3><br\></font\>";
-    }else{
-        echo "<br /><font style=\"color:#FF0000\">Invalid credentials! Please try again!<br\></font\>";
-    }
-}
-
-
-function checklogin($u,$p)
-{
-    if (($u) === "passwordisinrockyou" && crc32($p) == "550274426"){ //
-        return true;
-        }
-    }
-?>
-</form>
-
-</body>
-</html>
```

Login to the above directory with passwordisinrockyou:trumpet
