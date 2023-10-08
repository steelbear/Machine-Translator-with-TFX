# Machine Translator with TFX
TFX를 이용해 기계 번역 모델을 지속적으로 학습시키고 배포하는 시스템을 구축하는 프로젝트입니다.
해당 프로젝트는 [Semantic Segmentation model within ML pipeline](https://github.com/deep-diver/semantic-segmentation-ml-pipeline/tree/main)에 영향을 받았습니다.

## 목적
![프로젝트 개요](assets/프로젝트%20개요.jpg)
한국어-영어 기계 번역 모델을 지속적으로 학습시키고 배포하는 시스템을 만듭니다.
학습된 모델은 Tensorflow Serving와 Gradio로 제공하고 피드백을 받을 것입니다.
학습할 모델은 Seq2Seq나 Transformer와 같은 다양한 모델을 사용해볼 것입니다.

## 파이프라인 실행
### Local DAG
```bash
poetry run python pipelines/pipeline.py
```

## 데이터셋
[일상생활 및 구어체 한-영 번역 병렬 말뭉치 데이터](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&dataSetSn=71265)