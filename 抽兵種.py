import streamlit as st
import random
import time

# 設定網頁標題與圖示
st.set_page_config(page_title="國軍兵種抽籤系統", page_icon="🪖", layout="centered")

# 👇 關鍵步驟：使用 CSS 隱藏右上角的 GitHub 按鈕與選單
st.markdown("""
    <style>
    /* 隱藏右上角的選單、GitHub 圖標和頁尾 */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("🪖 國軍兵種自動抽籤系統")
st.write("公平、公正、公開！請輸入姓名並按下按鈕決定你的命運。")

# 初始化籤筒與紀錄
if 'pool' not in st.session_state:
    st.session_state.pool = (
        ["陸軍 (步兵)"] * 15 +
        ["陸軍 (裝甲兵)"] * 5 +
        ["海軍陸戰隊 (傳說中的天堂路)"] * 2 +
        ["海軍 (艦艇兵)"] * 3 +
        ["空軍"] * 3 +
        ["憲兵"] * 2 +
        ["海巡署 (岸巡)"] * 2 +
        ["外島籤 (金門海龍蛙兵)"] * 1 +
        ["外島籤 (馬祖步兵)"] * 2
    )
    st.session_state.history = []

# 側邊欄顯示目前剩餘籤數
with st.sidebar:
    st.header("📊 剩餘籤筒統計")
    st.write(f"目前籤筒總數：**{len(st.session_state.pool)}** 支")
    
    counts = {}
    for item in st.session_state.pool:
        counts[item] = counts.get(item, 0) + 1
    
    for job, count in counts.items():
        st.write(f"- {job}: {count} 支")
        
    if st.button("🔄 重設籤筒"):
        del st.session_state.pool
        del st.session_state.history
        st.rerun()

# 👤 自訂名稱輸入框
name_input = st.text_input("👤 請輸入抽籤人姓名：", placeholder="例如：張小明", key="user_name")

# 主要抽籤邏輯
if len(st.session_state.pool) > 0:
    # 如果沒輸入名字，按鈕會變成停用狀態
    button_disabled = not name_input.strip()
    
    if button_disabled:
        st.info("💡 請先在上方輸入姓名，才能開始抽籤喔！")
        
    if st.button("🎲 開始抽籤！", type="primary", use_container_width=True, disabled=button_disabled):
        status_text = st.empty()
        bar = st.progress(0)
        
        # 隨機滾動效果
        for i in range(10):
            temp_pick = random.choice(st.session_state.pool)
            status_text.markdown(f"### 🔄 {name_input} 正在盲抽... {temp_pick}")
            bar.progress((i + 1) * 10)
            time.sleep(0.1)
            
        status_text.empty()
        bar.empty()
        
        # 真正抽出籤
        picked = random.choice(st.session_state.pool)
        st.session_state.pool.remove(picked) 
        
        # 將「姓名 + 抽中兵種」紀錄到歷史中
        record_entry = f"**{name_input}** 抽中了 👉 **{picked}**"
        st.session_state.history.insert(0, record_entry)
        
        # 依據抽中結果顯示不同特效
        if "外島" in picked or "海軍陸戰隊" in picked:
            st.error(f"🎉 恭喜老爺！賀喜 **{name_input}**！您抽中了：**{picked}** 🪖")
            st.balloons() 
        else:
            st.success(f"✨ **{name_input}** 抽籤結果：**{picked}**")
else:
    st.warning("⚠️ 籤筒已經空了！請點擊左側側邊欄的「重設籤筒」重新開始。")

# 顯示抽籤歷史紀錄
if st.session_state.history:
    st.write("---")
    st.subheader("📜 最近抽籤紀錄")
    for idx, hist in enumerate(st.session_state.history):
        # 顯示序號與抽籤結果
        st.markdown(f"{len(st.session_state.history) - idx}. {hist}")
