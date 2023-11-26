<?php

include('config.php'); // 데이터베이스 설정 파일
$conn = mysqli_connect($servername, $username, $password, $dbname);

// 파라미터 확인 : 업데이트할 데이터 받아오기
$number = isset($_GET['number']) ? $_GET['number'] : '123가4567';
$speed = isset($_GET['speed']) ? intval($_GET['speed']) : null;
$direction = isset($_GET['direction']) ? $_GET['direction'] : null;

// 데이터베이스 쿼리
if ($number !== null)
{
        if ($speed !== null)
        {
                $stmt = $conn->prepare("UPDATE Controll SET speed=? WHERE number=?");
                $stmt->bind_param("is", $speed, $number);

                if ($stmt->execute())
                        echo "SUCCESS! speed=".$speed;

                $stmt->close();
        }
        elseif ($direction !== null)
        {
                $stmt = $conn->prepare("UPDATE Controll SET direction=? WHERE number=?");
                $stmt->bind_param("ss", $direction, $number);

                if ($stmt->execute())
                        echo "SUCCESS! direction=".$direction;

                $stmt->close();
        }
}

mysqli_close($conn);

?>