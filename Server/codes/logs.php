<!DOCTYPE html>
<html>
<head>
    <meta charset = "UTF-8">
    <meta http-equiv = "refresh" content="1">
    <link rel="stylesheet" type="text/css" href="styles.css">
</head>

<body>
    <div id="tab1" class="tab-content">
        <table border = '1' align = "center" width = 90%>
        <tr align = "center">
            <th>차량 번호</th>
            <th>차량 시동</th>
            <th>운전자 상태</th>
            <th>자율주행</th>
            <th>시간</th>
        </tr>

        <?php
        include 'config.php';
        $conn = mysqli_connect($servername, $username, $password, $dbname);
        $result = mysqli_query($conn, "select * from Logs order by date desc, time desc");
        while($row = mysqli_fetch_array($result))
        {
            echo "<tr align = center>";
            echo '<th>'.$row['number'].'</td>';

            $car_status = $row['car']?'ON':'OFF';
            echo '<th>'.$car_status.'</td>';
            if ($car_status=='ON')
            {
                    echo '<th>'.'level '.$row['driver'].'</td>';
                    $auto_status = $row['auto']?'O':'X';
                    echo '<th>'.$auto_status.'</td>';
            }
            else
            {
                    echo '<th>-</td>';
                    echo '<th>-</td>';
            }
            echo '<th>'.$row['date'].' '.$row['time'].'</td>';
            echo "</tr>";
        }
        mysqli_close($conn);
    ?>
    </table>
    </div>
</body>
</html>
