# 개발 2주차

## DEC07

**최수녕**

* S3버킷 이미지 AI에게 전달하는 방법 찾기 - 람다에서 AI api 호출
* Django EC2에 올리고 세팅
* S3에서 이미지 저장하고 장고 호출하는 람다 작성하기
* trigger연결





**강륜화**

* Amazon RDS에 올릴 MariaDB 생성





**류제룡**

* 이미지 수집 및 전처리





**김지현**

* 스토리 사진에 프로그레스바 구현

* 앱 전체적인 레이아웃 정리

* custom dialog 정리

* 레시피 상세보기 프래그먼트 구현 완료 - 액션바에 즐겨찾기, 리스트 버튼 생성

  



**박근웅**

* 이미지 데이터셋 찾기
* labeling



---



### 논의사항

* 메인 메뉴 탭에 [패밀리 / 홈 / 마이페이지] 로 되어있는 것을 [내 냉장고 / 홈 / 마이페이지]로 바꾸고,

  메인 화면에 [가족스토리 / 현재집안 온습도 / 외출모드 / 오늘의레시피추천]으로 변경

* 가족 추가는 마이페이지에서 설정하도록

* 레시피 크롤링해오는 사이트의 조회수도 recipe에 column으로 추가

  * 레시피 추천할 때, 식재료 data가 부족하면 조회수 내림차순으로 추천 우선순위 부여

* 냉장고 식재료 사진을 IoT가 S3에 올리면 바로 DB에 저장하는 대신, URL로 저장하도록 하자

  or 사진의 갯수를 한정지은 뒤 사진들의 각 int값을 DB에 저장하거나..

---

## DEC08

### 논의사항

* 레시피 추천을 재료 한 번 스캔 당 하나 추천해주는가? -> 한 번에 10개 가량은 보여주는 것으로

* 한국 식재료의 영어 번역본과 실제 영어 단어가 나타내는 식재료간의 불일치 여전히 존재

  한국 애호박을 squash라고 해도, zucchini라고 해도 우리가 원하는 바로 그 애호박이 나오지 않는다

  -> 데이터셋을 마련하기가 어려움

  -> 일일이 식재료 사진을 찍을까?

---

## DEC09

**최수녕**

* 기능별로 나누어 데이터베이스 마이그레이션
* 전체 재료 조회
* 냉장고 번호 유효성 검사 및 사용자 정보 insert
* 사용자가 입력한 & 이미지로 인식한 재료 삽입 / 조회
* 친구 팔로우 / 언팔로우
* 팔로우 된 친구의 가장 최근 사진 조회 및 읽음 표시
* aws SNS 세팅



**류제룡**

* PySpark 공부
* 레시피 크롤링 코드 수정





**김지현**

* 레시피 목록, 레시피 상세페이지 구현





**박근웅**

- annotation : yolo version → pascal voc version 으로 변경
- xml 파일 불러와서 annotation 작성
- sample로 만든 grocery data를 이용한 학습

---

### 논의사항

* 사진마다 식료품 크기가 다르게 드러나면 학습에 지장이 생기기 때문에

  우리가 원하는 사진 데이터의 형식을 지정해놓고 그것 위주로 모아야한다

* 식료품 옆에 생수병을 놓고 찍는 등 명확하게 크기를 알 수 있는 장치가 필요
* 카메라 높이에 따른 변수도 예상해야 함.. 하드웨어 설계가 빠르게 되어야 하는 이유

* 레시피 테이블의 fk는 역시 냉장고 고유번호 대신 사용자 아이디로 해도 될 것 같다
  * 어차피 회원가입용 이메일은 사용자당 하나이므로 이메일을 아이디==fk로 써도 된다!

---

## DEC10

**최수녕**

* 외출모드 OFF 상태시, 설정기간 동안 모션감지 없을 시 보호자에게 문자보내는 람다함수 작성(Cloud Watch와 연동)
* (불꽃/모션/온도/습도) 센서값 삽입 람다합수 작성
* 불꽃 센서 값 50이하일 때 보호자에게 문자보내는 람다함수 작성



**류제룡**

* 하드웨어 제작





**김지현**

* 하드웨어 제작





**박근웅**

* 하드웨어 제작


### **!!!하드웨어 제작 D+1!!!**

---

### 논의사항

* 외출모드 off == 모션센서 on 하려면 무조건 보호자 번호를 입력하도록 하자

* 안드로이드 어플을 까는 것은 배포가 아니라 각자 자기 핸드폰에 까는 것이고 통신은 서버랑만 하는거라서 안드로이드 내부db는 자기 폰에서 자기 개인정보 저장할때만 쓰인다

  그러니까 공용 정보는 s3버킷같은데 담던가 해야한다!

```java
var aws = require('aws-sdk');
var db_config = require('../config/db_config.json');
aws.config.loadFromPath('./config/aws_config.json');
var multer = require('multer');
var multerS3 = require('multer-s3');
var router = express.Router();
var s3 = new aws.S3();
```

```java
var upload = multer({
    storage: multerS3({
        s3: s3,
        bucket: 'sopt-hj',
        acl: 'public-read',
        key: function(req, file, cb) {
            cb(null, Date.now() + '.' + file.originalname.split('.').pop());
        }
    })
});
```

```java

router.post('/add', upload.single('wish_image'),function(req, res, next) {
    console.log(req.body);


    pool.getConnection(function(error, connection) {
        if (error) {
            console.log("getConnection Error" + error);
            res.sendStatus(500);
        } else {
            var sql, value;
            console.log(req.body.user_id);
            console.log(req.body.pro_id);

            if (req.file) {


                var url=url_table[req.body.brand_id];

                sql = 'insert into WishList(user_id, brand_id, pro_id, wish_title, wish_price, wish_image, wish_memo, pro_url) values(?,?,-1,?,?,?,?,?)';
                value = [req.body.user_id, req.body.brand_id, req.body.wish_title, req.body.wish_price, req.file.location, req.body.wish_memo, url];
                connection.query(sql, value, function(error, rows) {
                    if (error) {
                        console.log("Connection Error" + error);
                        res.sendStatus(500);
                        connection.release();
                    } else {
                        console.log("add WishList");
                        var sql2 = 'SELECT wish_id FROM WishList WHERE user_id = ? ORDER BY wish_id DESC LIMIT 1';
                        connection.query(sql2, [req.body.user_id], function (error2, rows2) {
                          if(error2){
                            console.log("Connection Error" + error);
                            res.sendStatus(500);
                            connection.release();
                          }else {


                             //   console.log("test2"+rows2[0].wish_id);
                            var sql3='select * from WishList where wish_id = ?';
                            connection.query(sql3,[rows2[0].wish_id],function(error3, rows3){
                                if(error3){
                                    console.log("Connection Error" + error);
                                    res.sendStatus(500);
                                    connection.release();

                               }else{
                                    console.log(rows3[0]);
                                    res.status(200).send(rows3[0]);
                                    connection.release();
                                }
                            });
                          }
                        });
                    }
                });
            }
```

* 사진과 다른 정보를 담아서 보내는 코드

```  javascript
    @Multipart
    @POST("/wishlists/modify")
    Call<Object> modifyWishList1(@Part MultipartBody.Part file,
                                 @Part("wish_id") RequestBody wish_id,
                                 @Part("wish_title") RequestBody wish_title,
                                 @Part("wish_price") RequestBody wish_price,
                                 @Part("wish_memo") RequestBody wish_memo);
```

---

## DEC11

**최수녕**

* 회원가입(암호화 방식) 함수
* 로그인 (토큰 값 생성 방식) 함수
* 인가된 사용자인지 확인 함수
* 즐겨찾기한 추천레시피 조회
* 추천레시피 




**류제룡**

* 하드웨어 제작





**김지현**

* 하드웨어 제작





**박근웅**

* 하드웨어 제작

### **!!!하드웨어 제작 D+2!!!**

---

### 논의사항

* cognito를 쓰는 것은 시간이 너무 오래 걸려서 django로 우선 백엔드 로직 구현
* 프론트는 안드로이드로 하자
* 카카오로 로그인기능 이런것은 하지 말자..
* 빅데이터 분석때문에 회원가입 할때 이용자 성별&연령층 받으려고 하는 이유
  * 빅데이터 활용을 위해!
  * 연령대 성별에 따른 선호 식재료 데이터가 축적되면 비슷한 집단에게 레시피/식재료 추천 등 활용가능
  * 복잡하면 빼도 되지만 복잡하지 않으니 하자!

---

## DEC12

### 멘토링때 보고드릴 진척사항

#### 1. 하드웨어

* 제작 80퍼센트 가량 완성
* 냉장고 모형은 우드락으로 구현

#### 2. 빅데이터

* AI학습에 필요한 이미지 수집, 전처리 하였으나 우리에게 맞는 이미지를 만들기 위해 하드웨어부터 제작
* pandas와 sklearn으로 작성한 기존 레시피 추천 코드를 spark로 바꿀 예정

#### 3. AI

* 식료품 이미지로 YOLO학습 완료

* 실제 냉장고에서 찍힐 사진과 크롤링 데이터셋의 차이, 이미지 물체의 크기가 다양하다는 단점 때문에 object detection이 실패하는 경우 다수 발생

  -> 정확도를 위해 직접 사진을 찍어 올려서 데이터셋을 생성하려고 함

* django에 yolo 연동중

#### 4. IoT

* 어플리케이션 메인화면 구현 완료
* 레시피 추천 목록화면 구현 완료
* 즐겨찾기 및 레시피 카카오톡 공유 기능 구현 중
* 현재 냉장고에 식재료를 사용자가 추가하는 기능 구현 중

#### 5. 클라우드

* AWS SNS와 Cloudwatch연동 완료
* Api gateway연결 완료
* s3 와 람다함수 연동을 통해 빅데이터와 ai에게 데이터 전송중
* DRF를 통해 백엔드 구축 완료
* EC2 배포 완료
