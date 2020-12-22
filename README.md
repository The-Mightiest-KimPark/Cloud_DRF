# 냉장고를 부탁해요우
## Please Take Care of My Refridgerator

- [회의록](#회의록)
- [실행방법](#실행방법)
- [REST API 정보](document/rest-api.md)

---

## 회의록

#### 11월

| 일 | 월 | 화 | 수 | 목 | 금 | 토 |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  | [19](document/topic.md#NOV19) | [20](document/topic.md#NOV20) | [21](document/topic.md#NOV21) |
| 22 | [23](document/design.md#NOV23) | [24](document/design.md#NOV24) | [25](document/design.md#NOV25) | [26](document/design.md#NOV26) | [27](document/design.md#NOV27) | [28](document/design.md#NOV28) |
| 29 | [30](document/design.md#NOV30) |



#### 12월

| 일 | 월 | 화 | 수 | 목 | 금 | 토 |
| --- | --- | --- | --- | --- | --- | --- |
|  |  | [1](document/develop-1st.md#DEC01) | [2](document/develop-1st.md#DEC02) | [3](document/develop-1st.md#DEC03) | [4](document/develop-1st.md#DEC04) | [5](document/develop-1st.md#DEC05) |
| 6 | [7](document/develop-2nd.md#DEC07) | [8](document/develop-2nd.md#DEC08) | [9](document/develop-2nd.md#DEC09) | [10](document/develop-2nd.md#DEC10) | [11](document/develop-2nd.md#DEC11) | [12](document/develop-2nd.md#DEC12) |
| [13](document/develop-2nd.md#DEC13) | [14](document/develop-3rd.md#DEC14) | [15](document/develop-3rd.md#DEC15) | [16](document/develop-3rd.md#DEC16) | [17](document/develop-3rd.md#DEC17) | [18](document/develop-3rd.md#DEC18) | [19](document/develop-3rd.md#DEC19) |
| [20](document/develop-3rd.md#DEC20) | [21](document/develop-4th.md#DEC21) | [22](document/develop-4th.md#DEC22) | [23](document/develop-4th.md#DEC23) | [24](document/develop-4th.md#DEC24) |  |  |

* 11.19 - 11.21: 주제 선정 및 기획
* 11.23 - 11.30: 구체화 및 사전준비
* 12.01 - 12.23: 개발
* 12.24: 프로젝트 최종 발표

---

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


