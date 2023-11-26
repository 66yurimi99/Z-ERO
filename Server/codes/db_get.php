<?php

include('config.php'); // 데이터베이스 설정 파일
$conn = mysqli_connect($servername, $username, $password, $dbname);

// 파라미터 확인 : 조회할 데이터 받아오기
$number = isset($_GET['number']) ? $_GET['number'] : "123가4567";
$stmt = $conn->prepare("SELECT Information.number, car, driver, speed, direction FROM Information JOIN Controll ON Information.number=Controll.number WHERE Information.number=?");
$stmt->bind_param("s", $number);

// 데이터베이스 쿼리
if ($stmt->execute())
{
        $result = $stmt->get_result();
        while($row = $result->fetch_assoc())
        {
                $car = $row['car'];
                $driver = $row['driver'];
                $speed = $row['speed'];
                $direction = $row['direction'];
        }
        $result->free_result();
}
$stmt->close();

// 데이터 출력
if (isset($_GET['car']))
{
        echo $car.',';
}
if (isset($_GET['driver']))
{
        echo $driver.',';
}
if (isset($_GET['speed']))
{
        echo $speed.',';
}
if (isset($_GET['direction']))
{
        echo $direction.',';
}

mysqli_close($conn);

?>