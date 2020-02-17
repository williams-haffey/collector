<?php
/*  Collector (Garcia, Kornell, Kerr, Blake & Haffey)
    A program for running experiments on the web
    Copyright 2012-2016 Mikey Garcia & Nate Kornell


    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 3 as published by
    the Free Software Foundation.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
 
		Kitten release (2019) author: Dr. Anthony Haffey (a.haffey@reading.ac.uk)
*/

require_once ("cleanRequests.php");

$page           = $_GET['page'];
$user_email     = $_GET['email'];
$confirm_code   = $_GET['confirm_code'];

require_once "../../sqlConnect.php";

$sql 		= "SELECT * FROM `users` WHERE email='$user_email'"; // "WHERE email='".$user_email."' LIMIT 1;
$result = $conn->query($sql);

//print_r($result);


if($result->num_rows>1 | $result->num_rows == 0){
	$_SESSION['login_error'] = "Something has gone wrong with your attempt to create a profile. Please confirm that you did not change the content of the link you were instructed to click on.";
} else {        
	$row = mysqli_fetch_array($result);
	$actual_code = $row['email_confirm_code'];
	
	if($confirm_code == $actual_code){            
		$sql = "UPDATE `users` SET `account_status` = 'V' WHERE email='$user_email'";
		if ($conn->query($sql) === TRUE) {
			$_SESSION['login_error'] = "You have succesfully registered. Click <a href='index.php'>here</a> to redirect to the main page.";
		} else {
			$_SESSION['login_error'] = "You have NOT confirmed registration. Please go back <a href='index.php'>here</a> to try again";
		}

	} else {
		$_SESSION['login_error'] = "You have failed to confirm your e-mail address. Please go back <a href='index.php'>here</a> to register again, or double check that nothing was changed in the link you were sent.";
	}
}
header('Location: '.$page);
?>