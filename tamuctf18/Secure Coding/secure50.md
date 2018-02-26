>I created a login form for my web page. Somehow people are logging in as admin without my password though!
Can you fix my login code for me?

```php
    $user = $_POST['username'];
    $pass = $_POST['password']; 

    // Ensure admin will always be the first record, though really unnecessary
    $sql = "SELECT * FROM Users WHERE User='$user' AND Password='$pass' ORDER BY ID";
```
```php
	$user = $conn->real_escape_string($_POST['username']);
    $pass = $conn->real_escape_string($_POST['password']); 

    // Ensure admin will always be the first record, though really unnecessary
    $sql = "SELECT * FROM Users WHERE User='$user' AND Password='$pass' ORDER BY ID";
```
