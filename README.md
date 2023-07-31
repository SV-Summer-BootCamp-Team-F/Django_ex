## 🛠️ Tech Stack
| Frontend | Backend | DevOps | Monitoring |  ETC |
|:--------:|:-------:|:------:|:----------:|:----:|
|<img src="https://img.shields.io/badge/React-61DAFB?style=flat&logo=React&logoColor=white"/><br><img src="https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=HTML5&logoColor=white" /><br><img src="https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=CSS3&logoColor=white" /><br><img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=TypeScript&logoColor=white"/><br><img src="https://img.shields.io/badge/D3.js-F9A03C?style=flat&logo=D3.jst&logoColor=white"/><br><img src="https://img.shields.io/badge/Three.js-000000?style=flat&logo=Three.js&logoColor=white"/>|<img src="https://img.shields.io/badge/Django-092E20?style=flat&logo=Django&logoColor=white" /><br><img src="https://img.shields.io/badge/Neo4j-4581C3?style=flat&logo=Neo4j&logoColor=white" />|<img src="https://img.shields.io/badge/Docker-2496ED?style=flat&logo=Docker&logoColor=white"/><br><img src="https://img.shields.io/badge/NGINX-009639?style=flat&logo=NGINX&logoColor=white"/><br><img src="https://img.shields.io/badge/Amazon EC2-FF9900?style=flat&logo=Amazon EC2&logoColor=white"/>|<img src="https://img.shields.io/badge/Grafana-F46800?style=flat&logo=Grafana&logoColor=white"/><br><img src="https://img.shields.io/badge/Prometheus-E6522C?style=flat&logo=Prometheus&logoColor=white"/><br><img src="https://img.shields.io/badge/-Google%20Analytics-%23FFBB00?logo=Google%20Analytics"/>|<img src="https://img.shields.io/badge/Slack-4A154B?style=flat&logo=Slack&logoColor=white"/><br><img src="https://img.shields.io/badge/Notion-000000?style=flat&logo=Notion&logoColor=white"/><br><img src="https://img.shields.io/badge/Postman-FF6C37?style=flat&logo=Postman&logoColor=white"/><br><img src="https://img.shields.io/badge/Swagger-85EA2D?style=flat&logo=Swagger&logoColor=white"/>

## docker-compose 빌드 관련
- 보통의 경우
    1. 터미널을 연다
    2. (docker-compose down 해준다. (혹시나 해서 삭제(아예 삭제 아님)))
    3. docker-compose up / docker-compose up —build
- 발생했던 에러
    1. 권한 문제 (permission denied)
    > sudo chown -R ($USER /Users/경로쓰는곳/.docker/)

## Neo4j 관련

- "7689:7687”로 안들어가져요!
    1. "7476:7474” 바로 아래 줄에 코드 추가 해주시고, 도커 다시 빌드 해주세요!
    이후 저 포트로 들어가면 연결이 됩니다!
- connect가 안돼요!
    1. 아이디 neo4j / 비밀번호 123412341234 를 잘 입력했는지 확인
    2. port가 bolt인지 확인 해주세요!
- 노드를 삭제,생성, 전체보기 하고 싶어요!
    1. 전체 노드 보기! → match (n) return n
    2. 노드 하나 보기! → match (변수:노드속성) return (변수)
    ![image](https://github.com/SV-Summer-BootCamp-Team-F/backend/assets/96772297/94989651-dc50-49ad-b79c-e42ffaf7017a)

    4. 노드 생성하기! → create (변수:노드속성 {속성:값}) return (변수)
    ![image](https://github.com/SV-Summer-BootCamp-Team-F/backend/assets/96772297/bc9139d1-9c94-4f59-a5ee-e28c3a564289)
    
    5. 전체 노드 삭제하기 → MATCH (n) DETACH DELETE n
    6. 어떤 하나의 관계 삭제하고 싶어! → MATCH (변수:노드속성 {속성: 값})-[관계변수:관계속성]->(변수:노드속성 {속성: 값}) DELETE 관계변수
    ![image](https://github.com/SV-Summer-BootCamp-Team-F/backend/assets/96772297/3f6f644b-453a-4db1-b89c-2c258c16391d)

    7. 하나의 관계를 생성하기! → match 문으로 찾고, create로 생성
    ![image](https://github.com/SV-Summer-BootCamp-Team-F/backend/assets/96772297/3cafd510-0453-41ea-a6be-5717b5b44c4a)

