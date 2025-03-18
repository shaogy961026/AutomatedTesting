import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import logging
import warnings

# 設置日誌
logging.basicConfig(level=logging.INFO)  # 加回這行
logger = logging.getLogger(__name__)

@pytest.mark.dependency()
def test_main_visual_display_normal(driver):
    try:
        logger.info("檢查主視覺是否正常顯示")
        main_visual = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "mKv"))
        )
        assert main_visual.is_displayed(), "主視覺未正常顯示"
        logger.info("主視覺顯示測試通過")
    except Exception as e:
        logger.error(f"主視覺顯示測試失敗: {str(e)}")
        raise

@pytest.mark.dependency(depends=["test_main_visual_display_normal"])
def test_maple_story_logo_display_normal(driver):
    try:
        logger.info("檢查新楓之谷LOGO是否正常顯示")
        logo = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mKv-logo"))
        )
        assert logo.is_displayed(), "新楓之谷LOGO未正常顯示"
        logger.info("新楓之谷LOGO顯示測試通過")
    except Exception as e:
        logger.error(f"LOGO顯示測試失敗: {str(e)}")
        raise

'''
疑似棄用
# @pytest.mark.dependency()
# def test_ad_watermark_display_normal(driver):
#     try:
#         logger.info("檢查廣宣浮水印是否顯示")
#         watermark = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".ad-watermark"))
#         )
#         assert watermark.is_displayed(), "廣宣浮水印未顯示"
#         logger.info("廣宣浮水印顯示測試通過")
#     except Exception as e:
#         logger.error(f"廣宣浮水印顯示測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_ad_watermark_click_redirect(driver):
#     try:
#         logger.info("點擊廣宣浮水印並檢查跳轉")
#         watermark = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".ad-watermark"))
#         )
#         watermark.click()
#         time.sleep(2)
#         assert "ad-page" in driver.current_url, "廣宣浮水印未跳轉至廣宣頁"
#         logger.info("廣宣浮水印跳轉測試通過")
#     except Exception as e:
#         logger.error(f"廣宣浮水印跳轉測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_ad_watermark_close_normal(driver):
#     try:
#         logger.info("關閉廣宣浮水印")
#         close_btn = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".ad-watermark-close"))
#         )
#         close_btn.click()
#         time.sleep(2)
#         watermark = driver.find_elements(By.CSS_SELECTOR, ".ad-watermark")
#         assert len(watermark) == 0 or not watermark[0].is_displayed(), "廣宣浮水印未關閉"
#         logger.info("廣宣浮水印關閉測試通過")
#     except Exception as e:
#         logger.error(f"廣宣浮水印關閉測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_ad_watermark_reappear_on_reload(driver):
#     try:
#         logger.info("重新載入頁面檢查廣宣浮水印是否再次出現")
#         driver.refresh()
#         time.sleep(2)
#         watermark = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".ad-watermark"))
#         )
#         assert watermark.is_displayed(), "廣宣浮水印未重新出現"
#         logger.info("廣宣浮水印重新出現測試通過")
#     except Exception as e:
#         logger.error(f"廣宣浮水印重新出現測試失敗: {str(e)}")
#         raise

'''

@pytest.mark.dependency()
def test_helper_watermark_display_correct(driver):
    try:
        logger.info("檢查小幫手floating是否顯示正確")
        helper = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "gim-bot-tool-button"))
        )
        assert helper.is_displayed(), "小幫手floating未顯示"
        logger.info("小幫手floating顯示測試通過")
    except Exception as e:
        logger.error(f"小幫手floating顯示測試失敗: {str(e)}")
        raise

@pytest.mark.dependency(depends=["test_helper_watermark_display_correct"])
def test_helper_watermark_click_redirect(driver):
    try:
        logger.info("檢查小幫手floating是否可以點擊")
        helper = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "gim-bot-tool-button"))
        )
        helper.click()

        logger.info("檢查點擊小幫手是否跳出對話框")
        chat_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "gim-bot-tool"))
        )
        assert chat_box.is_displayed(), "小幫手floating未顯示"
        logger.info("小幫手floating對話框顯示測試通過")
        helper.click()
        logger.info("關閉小幫手floating對話框")
    except Exception as e:
        logger.error(f"小幫手floating跳轉測試失敗: {str(e)}")
        raise

@pytest.mark.dependency(depends=["test_helper_watermark_display_correct"])
def test_helper_watermark_scroll_follow(driver):
    try:
        logger.info("檢查小幫手floating是否隨頁面滑動跟隨")
        helper = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "gim-bot-tool-button"))
        )
        initial_position = helper.location['y']
        logger.info(f"初始位置{initial_position}")
        driver.execute_script("window.scrollTo(0, 500);")
        logger.info("滑動至0,500")
        time.sleep(2)
        new_position = helper.location['y']
        logger.info(f"新位置{new_position}")
        assert new_position != initial_position, "小幫手floating未隨滾動跟隨"
        logger.info("小幫手flaoting跟隨測試通過")
        driver.execute_script("window.scrollTo(0, 0);")
        logger.info("滑動至0,0")        
        
    except Exception as e:
        logger.error(f"小幫手floating跟隨測試失敗: {str(e)}")
        raise

'''
疑似棄用
# @pytest.mark.dependency(depends=["test_helper_watermark_display_correct"])
# def test_helper_watermark_drag_movable(driver):
#     try:
#         logger.info("測試小幫手floating是否可拖動")
#         helper = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.ID, "gim-bot-tool-button"))
#         )
#         initial_position = helper.location
#         ActionChains(driver).drag_and_drop_by_offset(helper, 100, 100).perform()
#         time.sleep(2)
#         new_position = helper.location
#         assert new_position != initial_position, "小幫手floating未移動"
#         logger.info("小幫手floating拖動測試通過")
#     except Exception as e:
#         logger.error(f"小幫手flaoting拖動測試失敗: {str(e)}")
#         raise
'''


@pytest.mark.dependency()
def test_beanfun_icon_redirect(driver):
    try:
        logger.info("點擊Beanfun Icon並檢查跳轉")
        icon = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mKv-social-bf"))
        )
        icon.click()
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[1])
        assert "https://www.beanfun.com/" in driver.current_url, "Beanfun Icon未跳轉至正確頁面"
        logger.info("Beanfun Icon跳轉測試通過")
        # 關閉新標籤頁並切回原始頁面
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except Exception as e:
        logger.error(f"Beanfun Icon跳轉測試失敗: {str(e)}")
        raise

@pytest.mark.dependency()
def test_facebook_icon_redirect(driver):
    try:
        logger.info("點擊Facebook Icon並檢查跳轉")
        icon = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mKv-social-fb"))
        )
        icon.click()
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[1])
        assert "https://www.facebook.com/www.maplestory.msfans.com.tw" in driver.current_url, "Facebook Icon未跳轉至官方臉書頁面"
        logger.info("Facebook Icon跳轉測試通過")
        # 關閉新標籤頁並切回原始頁面
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except Exception as e:
        logger.error(f"Facebook Icon跳轉測試失敗: {str(e)}")
        raise

@pytest.mark.dependency()
def test_instagram_icon_redirect(driver):
    try:
        logger.info("點擊Instagram Icon並檢查跳轉")
        icon = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mKv-social-ig"))
        )
        icon.click()
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[1])
        assert "https://www.instagram.com/maplestory_tw" in driver.current_url, "Instagram Icon未跳轉至官方IG頁面"
        logger.info("Instagram Icon跳轉測試通過")
        # 關閉新標籤頁並切回原始頁面
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except Exception as e:
        logger.error(f"Instagram Icon跳轉測試失敗: {str(e)}")
        raise

@pytest.mark.dependency()
def test_sound_play_normal(driver):
    try:
        logger.info("點擊音樂ON按鈕並檢查播放")
        on_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mKv-musicPlayer-on"))
        )
        # 用 ActionChains 模擬使用者點擊
        actions = ActionChains(driver)
        actions.move_to_element(on_button).click().perform()
        time.sleep(2)  # 等待音樂開始播放
        
        # 檢查音樂是否播放
        is_playing = driver.execute_script("return !document.getElementById('mKvAudio').paused;")
        assert is_playing, "點擊ON按鈕後音樂未播放"
        logger.info("音樂播放測試通過")
    except Exception as e:
        logger.error(f"音樂播放測試失敗: {str(e)}")
        raise

@pytest.mark.dependency(depends=["test_sound_play_normal"])
def test_sound_close_normal(driver):
    try:
        logger.info("測試音樂關閉功能")
        off_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mKv-musicPlayer-off"))
        )
        actions = ActionChains(driver)
        actions.move_to_element(off_button).click().perform()
        time.sleep(2)
        is_paused = driver.execute_script("return document.getElementById('mKvAudio').paused;")
        assert is_paused, "點擊OFF按鈕後音樂未停止"
        logger.info("音樂停止測試通過")
    except Exception as e:
        logger.error(f"音樂關閉測試失敗: {str(e)}")
        raise

@pytest.mark.dependency()
def test_sound_switch_normal_with_default_play(driver):
    try:
        logger.info("測試點擊下一首按鈕是否切換歌曲")
        
        # 獲取當前歌曲標題
        initial_title_elem = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "marquee-wrap"))
        )
        initial_title = initial_title_elem.text.strip()
        logger.info(f"初始歌曲標題: {initial_title}")
        
        # 獲取當前音頻 src
        initial_src = driver.execute_script("return document.getElementById('mKvAudio').querySelector('source').src;")
        logger.info(f"初始音頻 src: {initial_src}")
        
        # 點擊下一首按鈕
        next_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mKv-musicPlayer-next"))
        )
        actions = ActionChains(driver)
        actions.move_to_element(next_button).click().perform()  # 模擬使用者點擊
        time.sleep(3)  # 等待歌曲切換
        
        # 檢查新歌曲標題
        new_title_elem = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "marquee-wrap"))
        )
        new_title = new_title_elem.text.strip()
        logger.info(f"新歌曲標題: {new_title}")
        
        # 檢查新音頻 src
        new_src = driver.execute_script("return document.getElementById('mKvAudio').querySelector('source').src;")
        logger.info(f"新音頻 src: {new_src}")
        
        # 驗證歌曲是否切換
        assert initial_title != new_title or initial_src != new_src, "點擊下一首按鈕後歌曲未切換"
        logger.info("歌曲切換測試通過")
    except Exception as e:
        logger.error(f"音樂切換測試失敗: {str(e)}")
        raise

@pytest.mark.dependency()
def test_sound_marquee_display_normal(driver):
    try:
        logger.info("檢查歌名跑馬燈是否正常顯示")
        marquee = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "marquee-wrap"))
        )
        assert marquee.is_displayed(), "歌名跑馬燈未顯示"
        logger.info("歌名跑馬燈顯示測試通過")
    except Exception as e:
        logger.error(f"歌名跑馬燈顯示測試失敗: {str(e)}")
        raise

@pytest.mark.dependency()
def test_game_start_not_logged_in_redirect(driver):
    try:
        logger.info("未登入狀態下點擊GAME START")
        game_start = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mKv-shortcuts-webstart"))
        )
        game_start.click()
        time.sleep(5)
        logger.info(f"目前網頁為{driver.current_url}")
        assert "https://tw.newlogin.beanfun.com/loginform" in driver.current_url, "未引導至共登頁面"
        logger.info("未登入GAME START跳轉測試通過")
        driver.get('https://maplestory.beanfun.com/main')
        time.sleep(2)
        logger.info("從登入畫面回首頁")
    except Exception as e:
        logger.error(f"未登入GAME START跳轉測試失敗: {str(e)}")
        raise

'''
需PROD測試帳號
# @pytest.mark.dependency()
# def test_game_start_logged_in_redirect(driver):
#     try:
#         logger.info("已登入狀態下點擊GAME START")
#         game_start = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".game-start-btn"))
#         )
#         game_start.click()
#         time.sleep(2)
#         assert "game" in driver.current_url, "未引導至遊戲館"
#         logger.info("已登入GAME START跳轉測試通過")
#     except Exception as e:
#         logger.error(f"已登入GAME START跳轉測試失敗: {str(e)}")
#         raise
'''

@pytest.mark.dependency()
def test_game_start_hover_animation(driver):
    try:
        
        logger.info("測試webstart按鈕hover背景變化")
        
        button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mKv-shortcuts-webstart"))
        )
        logger.info(f"按鈕是否可見: {button.is_displayed()}")
        logger.info(f"按鈕位置: {button.location}, 大小: {button.size}")
        
        # 確保滑鼠不在按鈕上，移到左上角
        actions = ActionChains(driver)
        actions.move_by_offset(10, 10).perform()
        time.sleep(1)
        
        # 初始狀態
        initial_background = driver.execute_script(
            "return window.getComputedStyle(document.querySelector('.mKv-shortcuts-webstart'), ':after').background;"
        )
        logger.info(f"初始狀態（滑鼠不在按鈕上） - :after background: {initial_background}")
        
        # 滑鼠移到按鈕上
        actions = ActionChains(driver)
        actions.move_to_element(button).perform()
        time.sleep(2)
        
        # hover後狀態
        hover_background = driver.execute_script(
            "return window.getComputedStyle(document.querySelector('.mKv-shortcuts-webstart'), ':after').background;"
        )
        logger.info(f"滑鼠移到按鈕上狀態 - :after background: {hover_background}")
        
        # 比較
        logger.info(f"差異比較：初始 {'!=' if initial_background != hover_background else '=='} hover")
        
        assert initial_background != hover_background, "滑鼠移入前後背景應不同"
        logger.info("webstart按鈕hover背景測試通過")
        
    except Exception as e:
        logger.error(f"webstart按鈕背景測試失敗: {str(e)}")
        raise

@pytest.mark.dependency()
def test_game_download_redirect(driver):
    try:
        logger.info("點擊遊戲下載並檢查跳轉")
        download_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mKv-shortcuts-download"))
        )
        download_btn.click()
        time.sleep(2)
        assert "download" in driver.current_url, "未跳轉至下載專區"
        logger.info("遊戲下載跳轉測試通過")
        driver.get('https://maplestory.beanfun.com/main')
        logger.info("從下載頁回首頁")
        time.sleep(2)
    except Exception as e:
        logger.error(f"遊戲下載跳轉測試失敗: {str(e)}")
        raise

@pytest.mark.dependency()
def test_register_account_redirect(driver):
    try:
        logger.info("點擊申請帳號並檢查跳轉")
        register_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mKv-shortcuts-apply"))
        )
        register_btn.click()
        time.sleep(2)
        assert "Register" in driver.current_url, "未跳轉至註冊頁面"
        logger.info("申請帳號跳轉測試通過")
        driver.get('https://maplestory.beanfun.com/main')
        logger.info("從申請帳號頁回首頁")
        time.sleep(2)
    except Exception as e:
        logger.error(f"申請帳號跳轉測試失敗: {str(e)}")
        raise

@pytest.mark.dependency()
def test_navigation_bar_fixed_on_scroll(driver):
    try:
        logger.info("檢查導覽列是否在下滑時固定")
        driver.execute_script("window.scrollTo(0, 500);")
        logger.info("下滑至出現導航列")
        nav_bar = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME,"mMain"))
        )
        driver.execute_script("window.scrollTo(0, 1000);")
        logger.info("再次下滑測試導航列是否固定")
        time.sleep(2)
        assert nav_bar.is_displayed(), "導覽列未固定顯示"
        logger.info("導覽列固定測試通過")
    except Exception as e:
        logger.error(f"導覽列固定測試失敗: {str(e)}")
        raise

# @pytest.mark.dependency()
# def test_navigation_bar_titles_display(driver):
#     try:
#         logger.info("檢查導覽列大標題是否顯示")
#         titles = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".nav-titles"))
#         )
#         assert titles.is_displayed(), "導覽列大標題未顯示"
#         logger.info("導覽列大標題顯示測試通過")
#     except Exception as e:
#         logger.error(f"導覽列大標題顯示測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_nav_news_anchor_redirect(driver):
#     try:
#         logger.info("點擊最新消息並檢查錨點跳轉")
#         news_link = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".nav-news"))
#         )
#         news_link.click()
#         time.sleep(2)
#         news_section = driver.find_element(By.CSS_SELECTOR, ".news-section")
#         assert news_section.is_displayed(), "未跳轉至最新消息區塊"
#         logger.info("最新消息錨點跳轉測試通過")
#     except Exception as e:
#         logger.error(f"最新消息錨點跳轉測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_nav_books_anchor_redirect(driver):
#     try:
#         logger.info("點擊楓葉圖書並檢查錨點跳轉")
#         books_link = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".nav-books"))
#         )
#         books_link.click()
#         time.sleep(2)
#         books_section = driver.find_element(By.CSS_SELECTOR, ".books-section")
#         assert books_section.is_displayed(), "未跳轉至職業介紹區塊"
#         logger.info("楓葉圖書錨點跳轉測試通過")
#     except Exception as e:
#         logger.error(f"楓葉圖書錨點跳轉測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_nav_download_redirect(driver):
#     try:
#         logger.info("點擊下載專區並檢查跳轉")
#         download_link = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".nav-download"))
#         )
#         download_link.click()
#         time.sleep(2)
#         assert "download" in driver.current_url, "未跳轉至下載專區頁面"
#         logger.info("下載專區跳轉測試通過")
#     except Exception as e:
#         logger.error(f"下載專區跳轉測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_nav_member_not_clickable(driver):
#     try:
#         logger.info("檢查楓葉會員是否不可點擊")
#         member_link = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".nav-member"))
#         )
#         assert not member_link.is_enabled(), "楓葉會員應不可點擊"
#         logger.info("楓葉會員不可點擊測試通過")
#     except Exception as e:
#         logger.error(f"楓葉會員不可點擊測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_nav_hk_redirect(driver):
#     try:
#         logger.info("點擊香港專區並檢查跳轉")
#         hk_link = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".nav-hk"))
#         )
#         hk_link.click()
#         time.sleep(2)
#         assert "hk" in driver.current_url, "未跳轉至香港遊戲橘子官網"
#         logger.info("香港專區跳轉測試通過")
#     except Exception as e:
#         logger.error(f"香港專區跳轉測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_nav_news_buttons_redirect(driver):
#     try:
#         logger.info("檢查最新消息按鈕連結")
#         news_btn = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".nav-news-btn"))
#         )
#         news_btn.click()
#         time.sleep(2)
#         assert "news" in driver.current_url, "最新消息按鈕連結異常"
#         logger.info("最新消息按鈕連結測試通過")
#     except Exception as e:
#         logger.error(f"最新消息按鈕連結測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_nav_books_buttons_redirect(driver):
#     try:
#         logger.info("檢查楓葉圖書按鈕連結")
#         books_btn = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".nav-books-btn"))
#         )
#         books_btn.click()
#         time.sleep(2)
#         assert "books" in driver.current_url, "楓葉圖書按鈕連結異常"
#         logger.info("楓葉圖書按鈕連結測試通過")
#     except Exception as e:
#         logger.error(f"楓葉圖書按鈕連結測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_nav_download_buttons_redirect(driver):
#     try:
#         logger.info("檢查下載專區按鈕連結")
#         download_btn = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".nav-download-btn"))
#         )
#         download_btn.click()
#         time.sleep(2)
#         assert "download" in driver.current_url, "下載專區按鈕連結異常"
#         logger.info("下載專區按鈕連結測試通過")
#     except Exception as e:
#         logger.error(f"下載專區按鈕連結測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_nav_member_buttons_redirect(driver):
#     try:
#         logger.info("檢查楓葉會員按鈕連結")
#         member_btn = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".nav-member-btn"))
#         )
#         member_btn.click()
#         time.sleep(2)
#         assert "member" in driver.current_url, "楓葉會員按鈕連結異常"
#         logger.info("楓葉會員按鈕連結測試通過")
#     except Exception as e:
#         logger.error(f"楓葉會員按鈕連結測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_nav_hk_buttons_redirect(driver):
#     try:
#         logger.info("檢查香港專區按鈕連結")
#         hk_btn = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".nav-hk-btn"))
#         )
#         hk_btn.click()
#         time.sleep(2)
#         assert "hk" in driver.current_url, "香港專區按鈕連結異常"
#         logger.info("香港專區按鈕連結測試通過")
#     except Exception as e:
#         logger.error(f"香港專區按鈕連結測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_ad_banner_display_normal(driver):
#     try:
#         logger.info("檢查廣宣燈箱是否正常顯示")
#         banner = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".ad-banner"))
#         )
#         assert banner.is_displayed(), "廣宣燈箱未顯示"
#         logger.info("廣宣燈箱顯示測試通過")
#     except Exception as e:
#         logger.error(f"廣宣燈箱顯示測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_ad_banner_switch_left_right(driver):
#     try:
#         logger.info("測試廣宣燈箱左右切換")
#         next_btn = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".ad-banner-next"))
#         )
#         next_btn.click()
#         time.sleep(2)
#         slide = driver.find_element(By.CSS_SELECTOR, ".ad-banner-slide")
#         assert slide.is_displayed(), "廣宣燈箱未切換"
#         logger.info("廣宣燈箱左右切換測試通過")
#     except Exception as e:
#         logger.error(f"廣宣燈箱左右切換測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_ad_banner_switch_bottom(driver):
#     try:
#         logger.info("測試廣宣燈箱下方切換")
#         bottom_btn = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".ad-banner-bottom-btn"))
#         )
#         bottom_btn.click()
#         time.sleep(2)
#         slide = driver.find_element(By.CSS_SELECTOR, ".ad-banner-slide")
#         assert slide.is_displayed(), "廣宣燈箱未切換"
#         logger.info("廣宣燈箱下方切換測試通過")
#     except Exception as e:
#         logger.error(f"廣宣燈箱下方切換測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_ad_banner_click_redirect(driver):
#     try:
#         logger.info("點擊廣宣燈箱並檢查跳轉")
#         banner = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".ad-banner"))
#         )
#         banner.click()
#         time.sleep(2)
#         assert "ad-page" in driver.current_url, "廣宣燈箱未跳轉至正確頁面"
#         logger.info("廣宣燈箱跳轉測試通過")
#     except Exception as e:
#         logger.error(f"廣宣燈箱跳轉測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_event_thumbnails_image_display(driver):
#     try:
#         logger.info("檢查活動宣傳縮圖圖片是否顯示")
#         thumbnail = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".event-thumbnail-img"))
#         )
#         assert thumbnail.is_displayed(), "活動宣傳縮圖圖片未顯示"
#         logger.info("活動宣傳縮圖圖片顯示測試通過")
#     except Exception as e:
#         logger.error(f"活動宣傳縮圖圖片顯示測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_event_thumbnails_text_display(driver):
#     try:
#         logger.info("檢查活動宣傳縮圖文字及日期是否顯示")
#         text = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".event-thumbnail-text"))
#         )
#         assert text.is_displayed(), "活動宣傳縮圖文字未顯示"
#         logger.info("活動宣傳縮圖文字顯示測試通過")
#     except Exception as e:
#         logger.error(f"活動宣傳縮圖文字顯示測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_event_thumbnails_click_redirect(driver):
#     try:
#         logger.info("點擊活動宣傳縮圖並檢查跳轉")
#         thumbnail = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".event-thumbnail"))
#         )
#         thumbnail.click()
#         time.sleep(2)
#         assert "event" in driver.current_url, "活動宣傳縮圖未跳轉至活動頁"
#         logger.info("活動宣傳縮圖跳轉測試通過")
#     except Exception as e:
#         logger.error(f"活動宣傳縮圖跳轉測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_news_tabs_display_correct(driver):
#     try:
#         logger.info("檢查最新消息區頁籤是否正確顯示")
#         tabs = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".news-tabs"))
#         )
#         assert tabs.is_displayed(), "最新消息頁籤未顯示"
#         logger.info("最新消息頁籤顯示測試通過")
#     except Exception as e:
#         logger.error(f"最新消息頁籤顯示測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_news_tabs_switch_normal(driver):
#     try:
#         logger.info("測試最新消息頁籤切換")
#         tab = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".news-tab-event"))
#         )
#         tab.click()
#         time.sleep(2)
#         content = driver.find_element(By.CSS_SELECTOR, ".news-content")
#         assert content.is_displayed(), "頁籤切換後內容未顯示"
#         logger.info("最新消息頁籤切換測試通過")
#     except Exception as e:
#         logger.error(f"最新消息頁籤切換測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_news_item_click_redirect(driver):
#     try:
#         logger.info("點擊最新消息項目並檢查跳轉")
#         item = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".news-item"))
#         )
#         item.click()
#         time.sleep(2)
#         assert "news" in driver.current_url, "最新消息項目未跳轉至消息頁"
#         logger.info("最新消息項目跳轉測試通過")
#     except Exception as e:
#         logger.error(f"最新消息項目跳轉測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_news_pagination_switch_normal(driver):
#     try:
#         logger.info("測試最新消息頁碼切換")
#         next_page = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".news-pagination-next"))
#         )
#         next_page.click()
#         time.sleep(2)
#         content = driver.find_element(By.CSS_SELECTOR, ".news-content")
#         assert content.is_displayed(), "頁碼切換後內容未顯示"
#         logger.info("最新消息頁碼切換測試通過")
#     except Exception as e:
#         logger.error(f"最新消息頁碼切換測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_news_arrow_switch_normal(driver):
#     try:
#         logger.info("測試最新消息箭頭切換")
#         arrow = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".news-arrow-next"))
#         )
#         arrow.click()
#         time.sleep(2)
#         content = driver.find_element(By.CSS_SELECTOR, ".news-content")
#         assert content.is_displayed(), "箭頭切換後內容未顯示"
#         logger.info("最新消息箭頭切換測試通過")
#     except Exception as e:
#         logger.error(f"最新消息箭頭切換測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_job_intro_display_normal(driver):
#     try:
#         logger.info("檢查職業介紹區是否正常顯示")
#         job_intro = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".job-intro"))
#         )
#         assert job_intro.is_displayed(), "職業介紹區未顯示"
#         logger.info("職業介紹區顯示測試通過")
#     except Exception as e:
#         logger.error(f"職業介紹區顯示測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_job_intro_tab_switch_normal(driver):
#     try:
#         logger.info("測試職業介紹頁籤切換")
#         tab = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".job-intro-tab"))
#         )
#         tab.click()
#         time.sleep(2)
#         content = driver.find_element(By.CSS_SELECTOR, ".job-intro-content")
#         assert content.is_displayed(), "職業頁籤切換後內容未顯示"
#         logger.info("職業介紹頁籤切換測試通過")
#     except Exception as e:
#         logger.error(f"職業介紹頁籤切換測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_job_intro_thumbnail_switch(driver):
#     try:
#         logger.info("測試職業介紹縮圖左右切換")
#         next_btn = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".job-intro-thumbnail-next"))
#         )
#         next_btn.click()
#         time.sleep(2)
#         thumbnail = driver.find_element(By.CSS_SELECTOR, ".job-intro-thumbnail")
#         assert thumbnail.is_displayed(), "縮圖未切換"
#         logger.info("職業介紹縮圖切換測試通過")
#     except Exception as e:
#         logger.error(f"職業介紹縮圖切換測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_job_intro_thumbnail_click_popup(driver):
#     try:
#         logger.info("點擊職業介紹縮圖並檢查彈窗")
#         thumbnail = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".job-intro-thumbnail"))
#         )
#         thumbnail.click()
#         time.sleep(2)
#         popup = driver.find_element(By.CSS_SELECTOR, ".job-intro-popup")
#         assert popup.is_displayed(), "角色介紹彈窗未出現"
#         logger.info("職業介紹彈窗測試通過")
#     except Exception as e:
#         logger.error(f"職業介紹彈窗測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_job_intro_popup_close_normal(driver):
#     try:
#         logger.info("關閉職業介紹彈窗")
#         close_btn = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".job-intro-popup-close"))
#         )
#         close_btn.click()
#         time.sleep(2)
#         popup = driver.find_elements(By.CSS_SELECTOR, ".job-intro-popup")
#         assert len(popup) == 0 or not popup[0].is_displayed(), "彈窗未關閉"
#         logger.info("職業介紹彈窗關閉測試通過")
#     except Exception as e:
#         logger.error(f"職業介紹彈窗關閉測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_job_intro_popup_switch_left_right(driver):
#     try:
#         logger.info("測試職業介紹彈窗左右切換")
#         next_btn = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".job-intro-popup-next"))
#         )
#         next_btn.click()
#         time.sleep(2)
#         content = driver.find_element(By.CSS_SELECTOR, ".job-intro-popup-content")
#         assert content.is_displayed(), "彈窗內容未切換"
#         logger.info("職業介紹彈窗左右切換測試通過")
#     except Exception as e:
#         logger.error(f"職業介紹彈窗左右切換測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_job_intro_popup_switch_bottom(driver):
#     try:
#         logger.info("測試職業介紹彈窗下方切換")
#         bottom_btn = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".job-intro-popup-bottom-btn"))
#         )
#         bottom_btn.click()
#         time.sleep(2)
#         content = driver.find_element(By.CSS_SELECTOR, ".job-intro-popup-content")
#         assert content.is_displayed(), "彈窗內容未切換"
#         logger.info("職業介紹彈窗下方切換測試通過")
#     except Exception as e:
#         logger.error(f"職業介紹彈窗下方切換測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_job_intro_popup_content_display(driver):
#     try:
#         logger.info("檢查職業介紹彈窗內容是否顯示")
#         content = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".job-intro-popup-content"))
#         )
#         assert content.is_displayed(), "彈窗內容未顯示"
#         logger.info("職業介紹彈窗內容顯示測試通過")
#     except Exception as e:
#         logger.error(f"職業介紹彈窗內容顯示測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_system_intro_display_normal(driver):
#     try:
#         logger.info("檢查系統介紹是否正常顯示")
#         system_intro = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".system-intro"))
#         )
#         assert system_intro.is_displayed(), "系統介紹未顯示"
#         logger.info("系統介紹顯示測試通過")
#     except Exception as e:
#         logger.error(f"系統介紹顯示測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_system_intro_switch_left_right(driver):
#     try:
#         logger.info("測試系統介紹左右切換")
#         next_btn = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".system-intro-next"))
#         )
#         next_btn.click()
#         time.sleep(2)
#         content = driver.find_element(By.CSS_SELECTOR, ".system-intro-content")
#         assert content.is_displayed(), "系統介紹內容未切換"
#         logger.info("系統介紹左右切換測試通過")
#     except Exception as e:
#         logger.error(f"系統介紹左右切換測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_system_intro_thumbnail_click_popup(driver):
#     try:
#         logger.info("點擊系統介紹縮圖並檢查彈窗")
#         thumbnail = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".system-intro-thumbnail"))
#         )
#         thumbnail.click()
#         time.sleep(2)
#         popup = driver.find_element(By.CSS_SELECTOR, ".system-intro-popup")
#         assert popup.is_displayed(), "系統介紹彈窗未出現"
#         logger.info("系統介紹彈窗測試通過")
#     except Exception as e:
#         logger.error(f"系統介紹彈窗測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_system_intro_popup_page_switch(driver):
#     try:
#         logger.info("測試系統介紹彈窗頁面切換")
#         next_btn = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".system-intro-popup-next"))
#         )
#         next_btn.click()
#         time.sleep(2)
#         content = driver.find_element(By.CSS_SELECTOR, ".system-intro-popup-content")
#         assert content.is_displayed(), "彈窗內容未切換"
#         logger.info("系統介紹彈窗頁面切換測試通過")
#     except Exception as e:
#         logger.error(f"系統介紹彈窗頁面切換測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_system_intro_popup_close_normal(driver):
#     try:
#         logger.info("關閉系統介紹彈窗")
#         close_btn = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".system-intro-popup-close"))
#         )
#         close_btn.click()
#         time.sleep(2)
#         popup = driver.find_elements(By.CSS_SELECTOR, ".system-intro-popup")
#         assert len(popup) == 0 or not popup[0].is_displayed(), "彈窗未關閉"
#         logger.info("系統介紹彈窗關閉測試通過")
#     except Exception as e:
#         logger.error(f"系統介紹彈窗關閉測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_system_intro_popup_content_display(driver):
#     try:
#         logger.info("檢查系統介紹彈窗內容是否顯示")
#         content = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".system-intro-popup-content"))
#         )
#         assert content.is_displayed(), "彈窗內容未顯示"
#         logger.info("系統介紹彈窗內容顯示測試通過")
#     except Exception as e:
#         logger.error(f"系統介紹彈窗內容顯示測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_media_zone_display_normal(driver):
#     try:
#         logger.info("檢查多媒體園地是否正常顯示")
#         media_zone = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".media-zone"))
#         )
#         assert media_zone.is_displayed(), "多媒體園地未顯示"
#         logger.info("多媒體園地顯示測試通過")
#     except Exception as e:
#         logger.error(f"多媒體園地顯示測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_media_zone_hover_switch(driver):
#     try:
#         logger.info("測試多媒體園地hover切換")
#         item = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".media-zone-item"))
#         )
#         ActionChains(driver).move_to_element(item).perform()
#         time.sleep(2)
#         content = driver.find_element(By.CSS_SELECTOR, ".media-zone-content")
#         assert content.is_displayed(), "hover後內容未切換"
#         logger.info("多媒體園地hover切換測試通過")
#     except Exception as e:
#         logger.error(f"多媒體園地hover切換測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_media_zone_tab_switch_normal(driver):
#     try:
#         logger.info("測試多媒體園地頁籤切換")
#         tab = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".media-zone-tab"))
#         )
#         tab.click()
#         time.sleep(2)
#         content = driver.find_element(By.CSS_SELECTOR, ".media-zone-content")
#         assert content.is_displayed(), "頁籤切換後內容未顯示"
#         logger.info("多媒體園地頁籤切換測試通過")
#     except Exception as e:
#         logger.error(f"多媒體園地頁籤切換測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_media_zone_player_works_redirect(driver):
#     try:
#         logger.info("點擊多媒體園地玩家創作並檢查跳轉")
#         link = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".media-zone-player-works"))
#         )
#         link.click()
#         time.sleep(2)
#         assert "player-works" in driver.current_url, "未跳轉至玩家創作區"
#         logger.info("多媒體園地玩家創作跳轉測試通過")
#     except Exception as e:
#         logger.error(f"多媒體園地玩家創作跳轉測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_player_works_thumbnail_click_popup(driver):
#     try:
#         logger.info("點擊玩家創作縮圖並檢查彈窗")
#         thumbnail = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".player-works-thumbnail"))
#         )
#         thumbnail.click()
#         time.sleep(2)
#         popup = driver.find_element(By.CSS_SELECTOR, ".player-works-popup")
#         assert popup.is_displayed(), "玩家創作彈窗未出現"
#         logger.info("玩家創作彈窗測試通過")
#     except Exception as e:
#         logger.error(f"玩家創作彈窗測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_player_works_popup_close_normal(driver):
#     try:
#         logger.info("關閉玩家創作彈窗")
#         close_btn = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".player-works-popup-close"))
#         )
#         close_btn.click()
#         time.sleep(2)
#         popup = driver.find_elements(By.CSS_SELECTOR, ".player-works-popup")
#         assert len(popup) == 0 or not popup[0].is_displayed(), "彈窗未關閉"
#         logger.info("玩家創作彈窗關閉測試通過")
#     except Exception as e:
#         logger.error(f"玩家創作彈窗關閉測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_player_works_thumbnail_download(driver):
#     try:
#         logger.info("點擊玩家創作縮圖下載")
#         download_btn = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".player-works-download"))
#         )
#         download_btn.click()
#         time.sleep(2)
#         # 假設下載會開新分頁或觸發下載，檢查新分頁或行為
#         assert len(driver.window_handles) > 1 or "download" in driver.current_url, "未觸發下載"
#         logger.info("玩家創作縮圖下載測試通過")
#     except Exception as e:
#         logger.error(f"玩家創作縮圖下載測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_media_zone_music_redirect(driver):
#     try:
#         logger.info("點擊多媒體園地樂曲並檢查跳轉")
#         link = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".media-zone-music"))
#         )
#         link.click()
#         time.sleep(2)
#         assert "music" in driver.current_url, "未跳轉至樂曲區"
#         logger.info("多媒體園地樂曲跳轉測試通過")
#     except Exception as e:
#         logger.error(f"多媒體園地樂曲跳轉測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_music_play_normal(driver):
#     try:
#         logger.info("測試樂曲播放功能")
#         play_btn = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".music-play-btn"))
#         )
#         play_btn.click()
#         time.sleep(2)
#         audio = driver.find_element(By.CSS_SELECTOR, ".music-player")
#         is_playing = driver.execute_script(
#             "return arguments[0].currentTime > 0 && !arguments[0].paused && !arguments[0].ended;",
#             audio
#         )
#         assert is_playing, "樂曲未播放"
#         logger.info("樂曲播放測試通過")
#     except Exception as e:
#         logger.error(f"樂曲播放測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_music_stop_normal(driver):
#     try:
#         logger.info("測試樂曲停止功能")
#         stop_btn = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".music-stop-btn"))
#         )
#         stop_btn.click()
#         time.sleep(2)
#         audio = driver.find_element(By.CSS_SELECTOR, ".music-player")
#         is_paused = driver.execute_script("return arguments[0].paused;", audio)
#         assert is_paused, "樂曲未停止"
#         logger.info("樂曲停止測試通過")
#     except Exception as e:
#         logger.error(f"樂曲停止測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_music_download_normal(driver):
#     try:
#         logger.info("測試樂曲下載功能")
#         download_btn = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".music-download-btn"))
#         )
#         download_btn.click()
#         time.sleep(2)
#         assert len(driver.window_handles) > 1 or "download" in driver.current_url, "未觸發下載"
#         logger.info("樂曲下載測試通過")
#     except Exception as e:
#         logger.error(f"樂曲下載測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_media_zone_art_redirect(driver):
#     try:
#         logger.info("點擊多媒體園地美術圖並檢查跳轉")
#         link = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".media-zone-art"))
#         )
#         link.click()
#         time.sleep(2)
#         assert "art" in driver.current_url, "未跳轉至美術圖區"
#         logger.info("多媒體園地美術圖跳轉測試通過")
#     except Exception as e:
#         logger.error(f"多媒體園地美術圖跳轉測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_art_thumbnail_click_popup(driver):
#     try:
#         logger.info("點擊美術圖縮圖並檢查彈窗")
#         thumbnail = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".art-thumbnail"))
#         )
#         thumbnail.click()
#         time.sleep(2)
#         popup = driver.find_element(By.CSS_SELECTOR, ".art-popup")
#         assert popup.is_displayed(), "美術圖彈窗未出現"
#         logger.info("美術圖彈窗測試通過")
#     except Exception as e:
#         logger.error(f"美術圖彈窗測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_art_popup_close_normal(driver):
#     try:
#         logger.info("關閉美術圖彈窗")
#         close_btn = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".art-popup-close"))
#         )
#         close_btn.click()
#         time.sleep(2)
#         popup = driver.find_elements(By.CSS_SELECTOR, ".art-popup")
#         assert len(popup) == 0 or not popup[0].is_displayed(), "彈窗未關閉"
#         logger.info("美術圖彈窗關閉測試通過")
#     except Exception as e:
#         logger.error(f"美術圖彈窗關閉測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_art_thumbnail_download(driver):
#     try:
#         logger.info("測試美術圖縮圖下載功能")
#         download_btn = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".art-download-btn"))
#         )
#         download_btn.click()
#         time.sleep(2)
#         assert len(driver.window_handles) > 1 or "download" in driver.current_url, "未觸發下載"
#         logger.info("美術圖縮圖下載測試通過")
#     except Exception as e:
#         logger.error(f"美術圖縮圖下載測試失敗: {str(e)}")
#         raise

if __name__ == "__main__":
    result = pytest.main(["-v", "--html=report.html", __file__])