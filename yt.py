import os
import shutil
import tempfile
import streamlit as st
import yt_dlp

# 設定網頁標題與圖示
st.set_page_config(page_title="YouTube 1080p60 下載器", page_icon="🎬", layout="centered")

st.title("🎬 YouTube 1080p 60fps 影片下載器")
st.write("輸入 YouTube 網址，線上解析並下載最高畫質影片。")

# 建立輸入框
url = st.text_input("請輸入 YouTube 影片網址：", placeholder="https://youtube.com...")

if url:
    # 建立一個按鈕來觸發解析與下載機制
    if st.button("🚀 開始解析影片", use_container_width=True):
        with st.spinner("正在分析並下載影片，請稍候... (高畫質合併需要一點時間)"):
            try:
                # 建立一個臨時資料夾來存放下載的檔案
                with tempfile.TemporaryDirectory() as tmpdir:
                    # 設定 yt-dlp 參數
                    # 輸出檔名格式設為 temp.mp4
                    output_template = os.path.join(tmpdir, "temp.%(ext)s")
                    
                    ydl_opts = {
                        "format": "bestvideo[height<=1080][fps>=60]+bestaudio/bestvideo[height<=1080]+bestaudio/best",
                        "merge_output_format": "mp4",
                        "outtmpl": output_template,
                        "quiet": True,  # 減少日誌輸出
                    }
                    
                    # 1. 擷取影片基本資訊（用來拿標題）
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=False)
                        video_title = info.get("title", "youtube_video")
                        
                        # 2. 正式下載到伺服器暫存區
                        ydl.download([url])
                    
                    # 檢查合併後的檔案是否存在
                    expected_file = os.path.join(tmpdir, "temp.mp4")
                    
                    if os.path.exists(expected_file):
                        # 3. 讀取暫存區的二進位檔案資料
                        with open(expected_file, "rb") as f:
                            video_bytes = f.read()
                        
                        st.success(f"✅ 解析成功！影片標題：{video_title}")
                        
                        # 4. 提供下載按鈕給前端使用者
                        st.download_button(
                            label="💾 點擊這裡下載影片到電腦",
                            data=video_bytes,
                            file_name=f"{video_title}.mp4",
                            mime="video/mp4",
                            use_container_width=True
                        )
                    else:
                        st.error("暫存檔案生成失敗，可能無法成功合併影音。")
                        
            except Exception as e:
                st.error(f"❌ 處理失敗，原因：{str(e)}")

st.markdown("---")
st.caption("💡 提示：本工具會優先尋找 1080p 60fps 規格。若影片本身不支援該規格，將自動調用可用的最高畫質。")
