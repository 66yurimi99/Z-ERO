# Fleet Management
Fleet management를 위한 서버 환경을 구축합니다.

## Results
### 1. 데이터베이스 접근을 위한 API
다음 요청들을 통해 DB 데이터를 수정할 수 있습니다. (`HTTP/GET`)
- 차량 등록 (by UI Application)
    ```python
    54.175.8.12/db.php?number=[차량번호]
    ```
- 시동 ON/OFF (by UI Application)
    ```python
    54.175.8.12/db.php?number=[차량번호]&car=[0 | 1]
    ```
- 운전자 상태 변경 (by DMS Service)
    ```python
    54.175.8.12/db.php?number=[차량번호]&driver=[0 | 1 | 2]
    ```

### 2. 웹 페이지 결과 화면 ([link](http://54.175.8.12/))
![./data/output_webpage.png](./data/output_webpage.png)

---
<br>

## Settings
### 1. Server Hosting (using AWS)
서버 호스팅 후 고정 IP를 할당하고, 보안을 위해 서비스별 방화벽 접근 권한을 설정합니다.
- IP Address : 54.175.8.12
- Web Server : http://54.175.8.12
- 방화벽 설정
    |Name|내용|Protocol|Port|Inbound rules|
    |:---:|:---:|:---:|:---:|:---:|
    |SSH|서버 관리자만 접속 허용|TCP|22|서버 관리자 IP|
    |Web Server|누구나 접속 가능|TCP|80|0.0.0.0|
    |MariaDB Server|웹 서버를 통해서만 접근|TCP|3306|웹 서버 IP|

---
### 2. Installation
- Apache2 설치 및 확인
    ```shell
    sudo apt install apache2 -y
    systemctl status apache2
    ```
- MariaDB 설치 및 확인
    ```shell
    sudo apt install mariadb-server mariadb-client -y
    systemctl status mariadb.service 
    ```
- PHP 설치
    ```shell
    $ sudo apt install php php-gd php-mysql -y
    ```

### 3. Database (MariaDB)
요구사항 및 데이터베이스 테이블 구성은 다음과 같습니다.  
#### ERD
![./data/ERD.png](./data/ERD.png)

#### 요구사항
1) Information : 엣지 디바이스의 현재 상태 정보
    - `number` : 차량 번호 (initial setting)
    - `car` : 자동차 시동 여부 (control by UI Application)
        - 0 : 시동 OFF, 주행 안 함
        - 1 : 시동 ON, 주행 중
    - `driver` : 운전자 졸음 상태 (control by DMS)
        - 0 : 각성 상태 (-> 매뉴얼 모드)
        - 1 : 졸린 상태 (-> 자율주행 모드)
        - 2 : 잠든 상태 (-> 자율주행 모드)

2) Logs : 이벤트 로깅
    - Information 테이블의 정보가 업데이트 될 때마다 로깅 (선행 조건: 자동차 시동 ON)
    - `Information.number`, `Information.car`, `Information.driver`
    - `auto` : 운전자
        - 운전자 상태에 따라 값 결정
        - 0 : 매뉴얼 모드
        - 1 : 자율주행 모드
    - `date`, `time` : 이벤트 발생 시간
<br><br>

요구사항과 ERD에 맞게 데이터베이스를 생성합니다.
```sql
-- DB 생성
CREATE DATABASE ZERODB CHARACTER SET utf8;

-- 사용할 DB 선택 - ZERODB
USE ZERODB;

-- 테이블 생성 : Information, Logs
CREATE TABLE IF NOT EXISTS Information (
	number VARCHAR(10) NOT NULL,
	car INT NOT NULL DEFAULT 0,
	driver INT NOT NULL DEFAULT 0,
	PRIMARY KEY (number)
) DEFAULT CHARACTER SET=utf8;

CREATE TABLE IF NOT EXISTS Logs (
	log_id INT NOT NULL AUTO_INCREMENT,
	number VARCHAR(10) NOT NULL,
	car INT NOT NULL,
	driver INT NOT NULL,
	auto INT NOT NULL,
	date DATE NOT NULL DEFAULT CURRENT_DATE(),
	time TIME NOT NULL DEFAULT CURRENT_TIME(),
	PRIMARY KEY (log_id)
) DEFAULT CHARACTER SET=utf8;

-- 트리거 생성 : Information 테이블의 정보가 업데이트될 때마다 Logs 테이블에 로그 추가
DELIMITER //
CREATE TRIGGER add_log_on_car_update
AFTER UPDATE ON Information
FOR EACH ROW
BEGIN
    -- Logs 테이블에 데이터 추가
    INSERT INTO Logs (number, car, driver, auto, date, time)
    VALUES (NEW.number, NEW.car, NEW.driver, CASE WHEN NEW.driver = 0 THEN 0 ELSE 1 END, CURRENT_DATE(), CURRENT_TIME());

END;
//
DELIMITER ;

```

---

### 4. DB Access API
- [config.png](./codes/config.php) : DB 접속 관련 설정 파일 (접속할 계정 정보 등)
- [db.php](./codes/db.php) : DB 접근을 위한 API 구현

---

### 5. Web Page
- [index.html](./codes/index.html) : 메인 페이지
- [logs.php](./codes/logs.php) : DB Logs 테이블 정보를 불러와 실시간으로 출력하는 페이지
- [styles.css](./codes/styles.css) : 디자인 관련 설정 파일

---