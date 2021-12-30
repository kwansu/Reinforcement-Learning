# Othello Game RL

## 프로젝트 설명
- pyagme으로 오델로 구성
- 규칙은 기존 오델로와 동일
- 규칙에 맞지 않는 수를 둘 경우 게임 종료
- 학습 편의를 위해 현재 상황에서 놓을 수 있는 곳에만 수를 두는 put_random_cell()을 구현
- 한쪽 색은 반자동모드로 수를 두고 나머지 한쪽은 확률적으로 explore(반자동, 완전자동)과 predict를 사용하며 학습시킴

## Jorldy 사용하기
- othello_config.py를 config/dqn 하위로 위치
- othello.py를 core/env 하위로 위치
- head.py의 내용을 core/network/head.py에 추가
- dqn_othello.py를 core/agent 하위로 위치
- 명령줄에 입력하여 실행
```python
python single_train.py --config config.dqn.othello --env.othello
```

## 학습결과
- eavl로 explor없이 실행  

![othello](https://user-images.githubusercontent.com/15683086/147729416-df90b2c8-0f0d-4ce9-8e94-92ce31e4e1c6.gif)