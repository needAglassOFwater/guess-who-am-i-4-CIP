import streamlit as st
import random
from PIL import Image
import os

# 页面配置
st.set_page_config(
    page_title="Guess Who Am I",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        text-align: center;
        font-size: 1.2rem;
        color: #7f8c8d;
        margin-bottom: 2rem;
    }
    .game-title {
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .question-section {
        background-color: #ecf0f1;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .guess-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .result-correct {
        text-align: center;
        font-size: 2.5rem;
        color: #27ae60;
        font-weight: bold;
    }
    .result-wrong {
        text-align: center;
        font-size: 2.5rem;
        color: #e74c3c;
        font-weight: bold;
    }
    .character-grid {
        display: flex;
        justify-content: center;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 角色info
@st.cache_data
def get_characters():
    return {
        "Sam": {
            "long_hair": False,
            "beard": True,
            "glasses": False,
            "hat": False,
            "male": True,
            "happy": False
        },
        "Vera": {
            "long_hair": True,
            "beard": False,
            "glasses": False,
            "hat": False,
            "male": False,
            "happy": False
        },
        "Devin": {
            "long_hair": False,
            "beard": False,
            "glasses": False,
            "hat": False,
            "male": True,
            "happy": True
        },
        "Heidi": {
            "long_hair": False,
            "beard": False,
            "glasses": False,
            "hat": False,
            "male": False,
            "happy": True
        },
        "Trevor": {
            "long_hair": False,
            "beard": False,
            "glasses": False,
            "hat": True,
            "male": True,
            "happy": False
        },
        "Mae": {
            "long_hair": True,
            "beard": False,
            "glasses": False,
            "hat": False,
            "male": False,
            "happy": True
        },
        "Lewis": {
            "long_hair": False,
            "beard": False,
            "glasses": False,
            "hat": False,
            "male": True,
            "happy": False
        },
        "George": {
            "long_hair": False,
            "beard": False,
            "glasses": True,
            "hat": False,
            "male": True,
            "happy": False
        },
        "Anita": {
            "long_hair": True,
            "beard": False,
            "glasses": False,
            "hat": True,
            "male": False,
            "happy": True
        },
        "Curtis": {
            "long_hair": False,
            "beard": True,
            "glasses": False,
            "hat": False,
            "male": True,
            "happy": True
        }
    }

# first page 
def initialize_game():
    if 'game_state' not in st.session_state:
        st.session_state.game_state = 'menu'
    if 'target_character' not in st.session_state:
        st.session_state.target_character = None
    if 'questions_asked' not in st.session_state:
        st.session_state.questions_asked = 0
    if 'question_history' not in st.session_state:
        st.session_state.question_history = []
    if 'last_answer' not in st.session_state:
        st.session_state.last_answer = None

# 開始game開始game
def start_game():
    characters = get_characters()
    st.session_state.target_character = random.choice(list(characters.keys()))
    st.session_state.questions_asked = 0
    st.session_state.question_history = []
    st.session_state.last_answer = None
    st.session_state.game_state = 'playing'

# 問問
def ask_question(question_text, attribute):
    characters = get_characters()
    answer = characters[st.session_state.target_character][attribute]
    st.session_state.questions_asked += 1
    st.session_state.question_history.append({
        'question': question_text,
        'answer': 'Yes' if answer else 'No'
    })
    st.session_state.last_answer = 'Yes' if answer else 'No'

# 猜
def make_guess(guessed_name):
    st.session_state.guessed_name = guessed_name
    st.session_state.game_state = 'result'

# 显示角色图片
def display_character_image():
    
    if os.path.exists("characters.png"):
        image = Image.open("characters.png")
        st.image(image, caption="Character Gallery", use_column_width=True)
    else:
        st.warning("cant find  characters.png ")
        
           
                          

# 主函数
def main():
    initialize_game()
    
    # 菜单页面
    if st.session_state.game_state == 'menu':
        st.markdown('<div class="main-title">GUESS WHO AM I</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-title">by: Kyle.C , CID</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎮 START GAME", type="primary", use_container_width=True):
                start_game()
                st.rerun()
    
    # 游戏页面
    elif st.session_state.game_state == 'playing':
        st.markdown('<div class="game-title">🎭 Guess Who Am I! 🎭</div>', unsafe_allow_html=True)
        
        # 显示角色图片
        display_character_image()
        
        # 创建两列布局
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 🤔 Ask Questions:")
            st.markdown('<div class="question-section">', unsafe_allow_html=True)
            
            questions = [
                ("Do you have long hair?", "long_hair"),
                ("Do you have beard?", "beard"),
                ("Do you wear glasses?", "glasses"),
                ("Do you wear hat?", "hat"),
                ("Are you male?", "male"),
                ("Are you happy?", "happy")
            ]
            
            # 创建问题按钮
            for question_text, attribute in questions:
                if st.button(question_text, key=f"q_{attribute}"):
                    ask_question(question_text, attribute)
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 显示问答历史
            if st.session_state.question_history:
                st.markdown("### 📝 Question History:")
                for i, qa in enumerate(st.session_state.question_history, 1):
                    st.write(f"{i}. {qa['question']} → **{qa['answer']}**")
        
        with col2:
            st.markdown("###  Make Your Guess:")
            st.markdown('<div class="guess-section">', unsafe_allow_html=True)
            
            names = ["Curtis", "Anita", "George", "Lewis", "Mae", 
                    "Trevor", "Heidi", "Devin", "Vera", "Sam"]
            
            # answer butt
            for i in range(0, len(names), 2):
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button(names[i], key=f"guess_{names[i]}", use_container_width=True):
                        make_guess(names[i])
                        st.rerun()
                with col_b:
                    if i + 1 < len(names):
                        if st.button(names[i + 1], key=f"guess_{names[i + 1]}", use_container_width=True):
                            make_guess(names[i + 1])
                            st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 显示统计信息
            st.markdown("### 📊 Game Stats:")
            st.write(f"Questions asked: **{st.session_state.questions_asked}**")
    
    # 结果页面
    elif st.session_state.game_state == 'result':
        # 判断结果
        if st.session_state.guessed_name == st.session_state.target_character:
            st.markdown('<div class="result-correct">🎉 CORRECT! 🎉</div>', unsafe_allow_html=True)
            result_color = "#27ae60"
        else:
            st.markdown('<div class="result-wrong">❌ WRONG! ❌</div>', unsafe_allow_html=True)
            result_color = "#e74c3c"
        
        st.markdown(f"### The correct answer was: **{st.session_state.target_character}**")
        st.markdown(f"### You asked **{st.session_state.questions_asked}** questions")
        
        # 评级系统
        if st.session_state.questions_asked <= 2:
            grade = "🕵️‍♂️ Excellent Detective!"
            grade_color = "#f39c12"
        elif st.session_state.questions_asked <= 4:
            grade = "👍 Good Job!"
            grade_color = "#3498db"
        else:
            grade = "💪 Keep Practicing!"
            grade_color = "#9b59b6"
        
        st.markdown(f'<div style="text-align: center; font-size: 1.5rem; color: {grade_color}; font-weight: bold; margin: 2rem 0;">{grade}</div>', unsafe_allow_html=True)
        
        # 显示问答历史
        if st.session_state.question_history:
            st.markdown("### 📝 Your Questions:")
            for i, qa in enumerate(st.session_state.question_history, 1):
                st.write(f"{i}. {qa['question']} → **{qa['answer']}**")
        
        # 按钮
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("🔄 PLAY AGAIN", type="primary", use_container_width=True):
                start_game()
                st.rerun()
        with col2:
            if st.button("🏠 MAIN MENU", use_container_width=True):
                st.session_state.game_state = 'menu'
                st.rerun()

if __name__ == "__main__":
    st.markdown("""
    ## 
    """)
    
    main()