from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
import traceback

# OpenAI 라이브러리 버전에 따른 import
try:
    from openai import OpenAI  # 새 버전 (1.x)
    NEW_OPENAI = True
    logger = logging.getLogger(__name__)
    logger.info("새 버전 OpenAI 라이브러리 사용 (1.x)")
except ImportError:
    import openai  # 구 버전 (0.x)
    NEW_OPENAI = False
    logger = logging.getLogger(__name__)
    logger.info("구 버전 OpenAI 라이브러리 사용 (0.x)")

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# OpenAI API 키 설정
api_key = os.getenv('OPENAI_API_KEY')
logger.info(f"환경변수 OPENAI_API_KEY: {'설정됨' if api_key else '설정되지 않음'}")

if api_key:
    logger.info(f"API 키 길이: {len(api_key)}")
    logger.info(f"API 키 시작: {api_key[:15]}...")
    
    if NEW_OPENAI:
        # 새 버전 OpenAI 클라이언트 초기화
        client = OpenAI(api_key=api_key)
    else:
        # 구 버전 OpenAI 설정
        openai.api_key = api_key
        client = None
else:
    client = None

# 시스템 프롬프트
SYSTEM_PROMPT = """
당신은 김형주라는 사람에 대해 잘 알고있습니다. 답변은 제시된 정보에 대한 내용 또는 IT 기술 관련 내용에만 답해주세요. 그 외 질문에는 잘 모르겠다고 공손하게 답하세요.

## 김형주의 정보:
- 이름은 김형주, 나이는 94년 1월 생 남성이며, 군대는 의경 만기제대 함.
- 고등학교는 중국 천진과 북경에서 다녔으며, 학부는 가천대학교 경제학과 주전공, 물리학과 복수전공 함. 석사는 광주과학기술원(GIST)에서 전기전자컴퓨터공학부 졸업.
- 석사 연구 주제는 양자내성 전자서명 알고리즘과 블록체인 합의체 구성 알고리즘에 관한 연구.
- 한국전자통신연구원(ETRI) 위촉연구원 경험 : NIST에서 진행중인 양자내성 암호 공모에 대한 세미나 진행 및 블록체인 지갑 보안을 위한 테스트베드 구축.
- Spring Boot Backend 개발 인턴 경험 : 솔트룩스 회사의 생성형 AI 부서에서 법률 보조 서비스 챗봇 백엔드 개발 참여. 주로 사용자 관리 및 문서 작성 템플릿 등의 서비스 개발.
- 교육 경험 : 2025년 2월부터 6개월간 클라우드, 네트워크, 리눅스 서버 구축 교육을 수강. 또한 2024년 3월부터 6개월간 java, spring framework(spring boot), Database, 머신러닝, 인공지능 교육 수강. 
- 가상화 기술 : Docker 이미지 생성 및 docker hub에 배포 실습. vagrant로 Kubernetes 클러스터 구축 실습.
- AWS 클라우드 :  EC2로 인스턴스를 만들고, Route53에서 도메인 및 인증서 생성. 로드밸랜서, 보안 그룹 등을 만들어서 https 도메인 보안 연결 구축.
- CI 구축 : Git action으로 dev환경에서 코드 push하면 자동으로 aws ec2 환경에 배포 (포트폴리오 웹사이트 개발).
- 프로젝트 : RAG를 활용하여 청년 정책에 대한 질의응답을 해주는 챗봇 서비스 외 3개의 프로젝트 있음(project 항목 참고).
- 네트워크 지식 : Cisco Packet tracer를 이용한 네트워크 토폴로지 구축 실습해봄. 여러 네트워크 프로토콜과 OSI계층에 대한 지식 보유.
- 리눅스 : 보안 지식과, proxy, dhcp, log, SMTP, 백업 등 여러 서비스를 구축해봄(project 항목 참고)

## 역할:
1. 주어진 정보이외에 절대로 임의로 만들어 내지 않음
2. IT 기술 관련 질문 답변
3. 친근하고 전문적인 톤으로 응답
4. 답변은 한국어로 제공하며 200글자를 넘지 않음

"""

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "openai_configured": bool(api_key),
        "openai_version": "1.x" if NEW_OPENAI else "0.x"
    }), 200

@app.route('/chat', methods=['POST'])
def chat():
    try:
        logger.info("=== 채팅 요청 시작 ===")
        
        # 요청 데이터 확인
        data = request.get_json()
        logger.info(f"받은 데이터: {data}")
        
        if not data or 'message' not in data:
            logger.error("메시지가 없음")
            return jsonify({"error": "메시지가 필요합니다."}), 400
        
        user_message = data['message']
        logger.info(f"사용자 메시지: {user_message}")
        
        # API 키 확인
        if not api_key:
            logger.error("API 키가 설정되지 않음")
            return jsonify({
                "response": "안녕하세요! 현재 AI 서비스 설정 중입니다. 곧 정상적인 답변을 드릴 수 있을 예정입니다. 😊",
                "status": "success"
            }), 200
        
        # OpenAI API 호출
        logger.info("OpenAI API 호출 시작")
        
        try:
            if NEW_OPENAI and client:
                # 새 버전 API 호출
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_message}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                ai_response = response.choices[0].message.content
                
            else:
                # 구 버전 API 호출
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_message}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                ai_response = response.choices[0].message.content
                
            logger.info("OpenAI API 호출 성공")
            logger.info(f"AI 응답: {ai_response[:100]}...")
            
            return jsonify({
                "response": ai_response,
                "status": "success"
            }), 200
            
        except Exception as openai_error:
            logger.error(f"OpenAI API 에러: {str(openai_error)}")
            logger.error(f"OpenAI 에러 타입: {type(openai_error)}")
            
            # 사용자에게 친근한 에러 메시지
            return jsonify({
                "response": "죄송합니다. AI 서비스에 일시적인 문제가 발생했습니다. 잠시 후 다시 시도해 주세요. 🤖",
                "status": "success"  # 사용자에게는 성공으로 표시
            }), 200
            
    except Exception as e:
        logger.error(f"예상치 못한 에러: {str(e)}")
        logger.error(f"스택 트레이스:\n{traceback.format_exc()}")
        
        return jsonify({
            "response": "죄송합니다. 일시적인 오류가 발생했습니다. 다시 시도해 주세요.",
            "status": "success"  # 사용자에게는 성공으로 표시
        }), 200

@app.route('/test', methods=['GET'])
def test():
    return jsonify({
        "message": "Flask API가 정상 작동 중입니다!",
        "openai_configured": bool(api_key),
        "openai_version": "1.x" if NEW_OPENAI else "0.x"
    }), 200

if __name__ == '__main__':
    logger.info("=== Flask 앱 시작 ===")
    logger.info(f"OpenAI 버전: {'1.x (새 버전)' if NEW_OPENAI else '0.x (구 버전)'}")
    logger.info(f"환경변수 상태: OPENAI_API_KEY = {'설정됨' if api_key else '설정되지 않음'}")
    app.run(host='0.0.0.0', port=5000, debug=True)