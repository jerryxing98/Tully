"INSERT INTO comments_log (comment, timestamp) VALUES ('" . str_replace("'", "\\'", $_POST['comment']) . "', NOW());"
