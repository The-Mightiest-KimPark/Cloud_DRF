# 냉장고를 부탁해요우
# Please Take Care of My Refridgerator

- [회의록](#회의록)
- [실행방법](#실행방법)
- [REST API 정보](document/rest-api.md)



## 회의록

#### 11월

| 일 | 월 | 화 | 수 | 목 | 금 | 토 |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  | [19](document/topic.md#NOV19) | [20](document/topic.md#NOV20) | [21](document/topic.md#NOV21) |
| 22 | [23](document/meeting.md#NOV23) | [24](document/meeting.md#NOV24) | [25](document/meeting.md#NOV25) | [26](document/meeting.md#NOV26) | [27](document/meeting.md#NOV27) | [28](document/meeting.md#NOV28) |
| 29 | [30](document/meeting.md#NOV30) |



#### 12월

| 일 | 월 | 화 | 수 | 목 | 금 | 토 |
| --- | --- | --- | --- | --- | --- | --- |
|  |  | [1] | [2] | [3] | [4] | 5 |
| 6 | [7] | [8] | [9] | [10] | [11]| [12] |
| [13] | [14] | [15] | [16] | [17] | [18] | [19] |
| [20] | [21] | [22] | [23] | [24] |  |  |




## 실행방법

1. 가상환경 폴더 생성
```bash
python -m venv venv
```

2. 프로젝트가 가상환경을 바라보도록 설정

```bash
source venv/Scripts/activate     # bash
source venv/Scripts/activate.bat # cmd
```

3. 가상폴더를 바라보도록 한 뒤 모듈 설치
```bash
pip install -r requirements.txt
```


4. 프로젝트 로컬 서버에 띄우기
```bash
python manage.py runserver
```


