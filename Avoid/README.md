# Avoid Game RL

## 프로젝트 설명
- pyagme으로 피하기 게임환경 구성
- 떨어지는 장애물에 맞으면 게임이 끝나고, 별을 먹으면 점수를 획득
- 제한된 프레임(2000)에서 최대 점수를 얻도록 DQN으로 학습

## Jorldy 사용하기
- avoid_config.py를 config/dqn 하위로 위치
- avoid2.py를 core/env 하위로 위치
- head.py의 내용을 core/network/head.py에 추가
- 명령줄에 입력하여 실행
```python
python single_train.py --config config.dqn.avoid --env.avoid2 
```

## 학습결과
- eavl로 explor없이 실행  


![avoid](https://user-images.githubusercontent.com/15683086/147727426-8fb03e59-6ece-4a5d-b1c3-01918f02be82.gif)