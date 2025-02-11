import spacy
import re
from transformers import BertTokenizer, BertForTokenClassification
from transformers import pipeline
 
# BERT 모델과 토크나이저 로드 (한국어 모델)
model_name = "kykim/bert-kor-base"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForTokenClassification.from_pretrained(model_name)
 
# Hugging Face의 파이프라인을 사용하여 NER 설정
nlp_ner = pipeline("ner", model=model, tokenizer=tokenizer)
 
# 한국어 SpaCy 모델 로드 ; python -m spacy download ko_core_news_sm
nlp_spacy = spacy.load("ko_core_news_sm")
 
# 비정형 데이터 예시
texts = [
    "장비A는 2024년 1월 15일에 고장이 발생했으며, 부품B를 교체했다.",
    "장비C는 2024년 2월 10일에 정기점검했다.",
    "장비D는 2024년 3월 5일에 소프트웨어 업데이트했다.",
    "장비E는 2024년 4월 20일에 부품C를 교체했다.",
    "장비F는 2024년 5월 30일에 고장이 발생했으며, 부품D를 교체했다."
]
 
# NLP 처리 및 정보 추출
for text in texts:
    print(f"처리된 텍스트: {text}")
     
    parts = []  # 부품명 저장 리스트
    devices = []  # 장비명 저장 리스트
    actions = []  # 액션 저장 리스트
    dates = []  # 날짜 저장 리스트
     
    # 날짜 추출 정규 표현식
    date_pattern = r'\d{4}년 \d{1,2}월 \d{1,2}일'
     
    # 날짜 추출
    dates += re.findall(date_pattern, text)
     
    # 장비명 및 부품명 추출을 위한 정규 표현식
    device_pattern = r'장비[A-Z]'
    part_pattern = r'부품[A-Z]'
     
    # 장비명 및 부품명 추출
    devices += re.findall(device_pattern, text)
    parts += re.findall(part_pattern, text)
     
    # NER 추출
    ner_results = nlp_ner(text)
    for entity in ner_results:
        if entity['entity'] == 'B-LOC':  # 예시로 LOC 엔티티를 액션으로 간주
            actions.append(entity['word'])
     
    # spaCy를 사용하여 동사 추출
    doc_spacy = nlp_spacy(text)
    for token in doc_spacy:
        if token.pos_ == "VERB":
            actions.append(token.text)
     
    print("추출된 장비명:", devices)
    print("추출된 부품명:", parts)
    print("추출된 액션:", actions)
    print("추출된 날짜:", dates)
    print()  # 각 텍스트 사이에 빈 줄 추가
 
 
### 실행 결과
처리된 텍스트: 장비A는 2024년 1월 15일에 고장이 발생했으며, 부품B를 교체했다.
추출된 장비명: ['장비A']
추출된 부품명: ['부품B']
추출된 액션: ['부품B를', '교체했다']
추출된 날짜: ['2024년 1월 15일']
 
처리된 텍스트: 장비C는 2024년 2월 10일에 정기점검했다.
추출된 장비명: ['장비C']
추출된 부품명: []
추출된 액션: ['정기점검했다']
추출된 날짜: ['2024년 2월 10일']
 
처리된 텍스트: 장비D는 2024년 3월 5일에 소프트웨어 업데이트했다.
추출된 장비명: ['장비D']
추출된 부품명: []
추출된 액션: ['업데이트했다']
추출된 날짜: ['2024년 3월 5일']
 
처리된 텍스트: 장비E는 2024년 4월 20일에 부품C를 교체했다.
추출된 장비명: ['장비E']
추출된 부품명: ['부품C']
추출된 액션: ['교체했다']
추출된 날짜: ['2024년 4월 20일']
 
처리된 텍스트: 장비F는 2024년 5월 30일에 고장이 발생했으며, 부품D를 교체했다.
추출된 장비명: ['장비F']
추출된 부품명: ['부품D']
추출된 액션: ['교체했다']
추출된 날짜: ['2024년 5월 30일']
