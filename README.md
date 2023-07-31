# 

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

