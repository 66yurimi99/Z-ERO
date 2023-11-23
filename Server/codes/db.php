<?php

include('config.php'); // 데이터베이스 설정 파일
$conn = mysqli_connect($servername, $username, $password, $dbname);

// 정보를 업데이트할 데이터 - HTTP 요청에서 파라미터를 받아옴
$number = isset($_GET['number']) ? $_GET['number'] : null;
$car = isset($_GET['car']) ? intval($_GET['car']) : null;
$driver = isset($_GET['driver']) ? intval($_GET['driver']) : null;

// 데이터베이스 쿼리
if ($number !== null)
{
        if ($car !== null)
        {
                $stmt = $conn->prepare("UPDATE Information SET car=? WHERE number=?");
                $stmt->bind_param("is", $car, $number);

                if ($stmt->execute())
                        echo "SUCCESS! car=".$car;

                $stmt->close();
        }
        elseif ($driver !== null)
        {
                $stmt = $conn->prepare("UPDATE Information SET driver=? WHERE number=? and car=1");
                $stmt->bind_param("is", $driver, $number);

                if ($stmt->execute())
                        echo "SUCCESS! driver=".$driver;

                $stmt->close();
        }
        else
        {
                $stmt = $conn->prepare("INSERT IGNORE INTO Information (number) VALUES (?)");
                $stmt->bind_param("s", $number);

                if ($stmt->execute())
                        echo "SUCCESS! number=".$number;

                $stmt->close();
        }
}

mysqli_close($conn);

?>
