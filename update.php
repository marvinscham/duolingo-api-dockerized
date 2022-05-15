<?php
exec("python3 get_random_string.py", $random_string);

if ($_GET['i'] === $random_string) {
    exec("python3 duo_main.py");
}