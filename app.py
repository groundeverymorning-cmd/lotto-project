import streamlit as st
import random
import time

# --- 페이지 설정 ---
st.set_page_config(
    page_title="프리미엄 로또 번호 생성기",
    page_icon="🍀",
    layout="centered"
)

# --- CSS 스타일 적용 ---
# Streamlit의 기본 UI를 덮어쓰고 커스텀 스타일을 적용합니다.
st.markdown("""
<style>
/* 전체 배경 및 폰트 */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&family=Noto+Sans+KR:wght@400;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    font-family: 'Outfit', 'Noto Sans KR', sans-serif;
    color: white;
}

/* 제목 스타일 */
h1 {
    text-align: center;
    font-size: 3rem !important;
    font-weight: 800 !important;
    letter-spacing: 2px;
    padding-bottom: 0.5rem;
}
h1 span {
    color: #ffd700;
    text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
}

/* 서브 텍스트 */
p {
    text-align: center;
    color: #b0c4de;
    font-size: 1.1rem;
}

/* 감싸는 컨테이너 효과 (Streamlit은 마크다운으로 직접 래퍼를 씌우기 어려워 전체적으로 여백/패딩으로 조절) */
.main .block-container {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 30px;
    padding: 3rem;
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
    margin-top: 3rem;
    max-width: 800px;
}

/* 공 모양 스타일 */
.balls-container {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin-bottom: 3rem;
    flex-wrap: wrap;
    min-height: 80px;
    padding: 20px 0;
}

.ball {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 2rem;
    font-weight: 800;
    color: #333;
    box-shadow:  10px 10px 20px rgba(0,0,0,0.3),
                 -10px -10px 20px rgba(255,255,255,0.1);
    animation: pop 0.4s ease-out forwards;
}

/* 로또 번호 대역별 색상 */
.color-1 { background: linear-gradient(135deg, #f6d365, #fda085); } /* 1~10 노란색 */
.color-2 { background: linear-gradient(135deg, #84fab0, #8fd3f4); } /* 11~20 파란색 */
.color-3 { background: linear-gradient(135deg, #ff9a9e, #fecfef); } /* 21~30 빨간색 */
.color-4 { background: linear-gradient(135deg, #a18cd1, #fbc2eb); } /* 31~40 보라색 */
.color-5 { background: linear-gradient(135deg, #89f7fe, #66a6ff); } /* 41~45 초록/파랑 */

/* 플레이스홀더 */
.ball.placeholder {
    background: rgba(255, 255, 255, 0.1);
    box-shadow: inset 5px 5px 10px rgba(0,0,0,0.2);
    color: #b0c4de;
    animation: none;
}

@keyframes pop {
    0% { transform: translateY(50px) scale(0.5); opacity: 0; }
    50% { transform: scale(1.1); opacity: 1; }
    100% { transform: translateY(0) scale(1); opacity: 1; }
}

/* Streamlit 기본 버튼 커스텀 */
div.stButton > button {
    display: block;
    margin: 0 auto;
    padding: 1.2rem 3rem;
    font-size: 1.2rem;
    font-weight: 700;
    border: none;
    border-radius: 50px;
    background: linear-gradient(90deg, #ff8a00, #e52e71);
    color: white;
    box-shadow: 0 10px 20px rgba(229, 46, 113, 0.3);
    transition: transform 0.2s, box-shadow 0.2s;
    width: auto;
}
div.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 25px rgba(229, 46, 113, 0.5);
    color: white;
    border: none;
}
div.stButton > button:active {
    transform: translateY(1px);
}
div.stButton > button:focus {
    box-shadow: 0 10px 20px rgba(229, 46, 113, 0.3);
    color: white;
}
</style>
""", unsafe_allow_html=True)

# --- 함수 정의 ---
def get_color_class(number):
    if number <= 10: return 'color-1'
    elif number <= 20: return 'color-2'
    elif number <= 30: return 'color-3'
    elif number <= 40: return 'color-4'
    else: return 'color-5'

# --- UI 레이아웃 ---
st.markdown("<h1>Lotto <span>럭키 셀렉터</span></h1>", unsafe_allow_html=True)
st.markdown("<p>당신의 행운을 책임질 6개의 숫자를 만나보세요 (Streamlit 버전)</p>", unsafe_allow_html=True)

# 번호 생성 상태 관리를 위한 session_state
if 'lotto_numbers' not in st.session_state:
    st.session_state.lotto_numbers = []
if 'is_generating' not in st.session_state:
    st.session_state.is_generating = False

# 공을 표시할 빈 공간(placeholder)
balls_placeholder = st.empty()

# 초기 상태 기획 (물음표 공 6개)
def render_empty_balls():
    html_content = '<div class="balls-container">'
    for _ in range(6):
        html_content += '<div class="ball placeholder">?</div>'
    html_content += '</div>'
    balls_placeholder.markdown(html_content, unsafe_allow_html=True)

# 번호 렌더링 함수
def render_balls(numbers, show_up_to=6):
    html_content = '<div class="balls-container">'
    for i in range(6):
        if i < show_up_to:
            num = numbers[i]
            color_class = get_color_class(num)
            html_content += f'<div class="ball {color_class}">{num}</div>'
        else:
            html_content += '<div class="ball placeholder">?</div>'
    html_content += '</div>'
    balls_placeholder.markdown(html_content, unsafe_allow_html=True)

# 생성 버튼
if st.button("번호 생성하기", disabled=st.session_state.is_generating):
    st.session_state.is_generating = True
    
    # 번호 추첨 로직
    numbers = random.sample(range(1, 46), 6)
    numbers.sort()
    st.session_state.lotto_numbers = numbers
    
    # 0.3초마다 하나씩 렌더링하여 애니메이션 효과 흉내내기
    for i in range(1, 7):
        render_balls(numbers, show_up_to=i)
        time.sleep(0.3)
        
    st.session_state.is_generating = False
    st.rerun() # 버튼 상태 리셋을 위해 재실행

# 상태 복원 렌더링
if not st.session_state.is_generating:
    if len(st.session_state.lotto_numbers) == 6:
        render_balls(st.session_state.lotto_numbers, show_up_to=6)
    else:
        render_empty_balls()
