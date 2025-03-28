import pytest
import psutil
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import time
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.mark.dependency()
def test_main_visual_display_normal(driver,reset_state):
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
def test_maple_story_logo_display_normal(driver,reset_state):
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
def test_helper_watermark_display_correct(driver,reset_state):
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
def test_helper_watermark_click_redirect(driver,reset_state):
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
        # helper.click()
        # logger.info("關閉小幫手floating對話框")
    except Exception as e:
        logger.error(f"小幫手floating跳轉測試失敗: {str(e)}")
        raise

@pytest.mark.dependency(depends=["test_helper_watermark_display_correct"])
def test_helper_watermark_scroll_follow(driver,reset_state):
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


def test_beanfun_icon_redirect(driver,reset_state):
    try:
        logger.info("點擊Beanfun Icon並檢查跳轉")
        icon = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mKv-social-bf"))
        )
        icon.click()
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[-1])
        assert "https://www.beanfun.com/" in driver.current_url, "Beanfun Icon未跳轉至正確頁面"
        logger.info("Beanfun Icon跳轉測試通過")
        # 關閉新標籤頁並切回原始頁面
        # driver.close()
        # driver.switch_to.window(driver.window_handles[0])
    except Exception as e:
        logger.error(f"Beanfun Icon跳轉測試失敗: {str(e)}")
        raise

def test_facebook_icon_redirect(driver,reset_state):
    try:
        logger.info("點擊Facebook Icon並檢查跳轉")
        icon = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mKv-social-fb"))
        )
        icon.click()
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[-1])
        assert "https://www.facebook.com/www.maplestory.msfans.com.tw" in driver.current_url, "Facebook Icon未跳轉至官方臉書頁面"
        logger.info("Facebook Icon跳轉測試通過")

    except Exception as e:
        logger.error(f"Facebook Icon跳轉測試失敗: {str(e)}")
        raise

@pytest.mark.dependency()
def test_instagram_icon_redirect(driver,reset_state):
    try:
        logger.info("點擊Instagram Icon並檢查跳轉")
        icon = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mKv-social-ig"))
        )
        icon.click()
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[-1])
        assert "https://www.instagram.com/maplestory_tw" in driver.current_url, "Instagram Icon未跳轉至官方IG頁面"
        logger.info("Instagram Icon跳轉測試通過")
    except Exception as e:
        logger.error(f"Instagram Icon跳轉測試失敗: {str(e)}")
        raise

@pytest.mark.dependency()
def test_sound_play_normal(driver,reset_state):
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
def test_sound_close_normal(driver,reset_state):
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
def test_sound_switch_normal_with_default_play(driver,reset_state):
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
def test_sound_marquee_display_normal(driver,reset_state):
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
def test_game_start_not_logged_in_redirect(driver,reset_state):
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
def test_game_start_hover_animation(driver,reset_state):
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
def test_game_download_redirect(driver,reset_state):
    try:
        logger.info("點擊遊戲下載並檢查跳轉")
        download_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mKv-shortcuts-download"))
        )
        download_btn.click()
        time.sleep(2)
        assert "download" in driver.current_url, "未跳轉至下載專區"
        logger.info("遊戲下載跳轉測試通過")
    except Exception as e:
        logger.error(f"遊戲下載跳轉測試失敗: {str(e)}")
        raise

@pytest.mark.dependency()
def test_register_account_redirect(driver,reset_state):
    try:
        logger.info("點擊申請帳號並檢查跳轉")
        register_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mKv-shortcuts-apply"))
        )
        register_btn.click()
        time.sleep(2)
        assert "Register" in driver.current_url, "未跳轉至註冊頁面"
        logger.info("申請帳號跳轉測試通過")
    except Exception as e:
        logger.error(f"申請帳號跳轉測試失敗: {str(e)}")
        raise

def test_navigation_bar_fixed_on_scroll(driver,reset_state):
    try:
        logger.info("檢查導覽列是否在下滑時固定")
        driver.execute_script("window.scrollTo(0, 500);")
        logger.info("下滑至出現導航列")
        nav_bar = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME,"mainmenu-wrap"))
        )
        driver.execute_script("window.scrollTo(0, 1000);")
        logger.info("再次下滑測試導航列是否固定")
        time.sleep(2)
        assert nav_bar.is_displayed(), "導覽列未固定顯示"
        logger.info("導覽列固定測試通過")
    except Exception as e:
        logger.error(f"導覽列固定測試失敗: {str(e)}")
        raise

def test_navigation_bar_titles_display(driver,reset_state):
    try:
        # 預期的標題清單
        expected_titles = [
            "最新消息",
            "楓葉圖書",
            "下載專區",
            "楓葉會員",
            "香港專區"
        ]
        
        logger.info("開始檢查主選單大標題")
        
        # 等待主選單元素出現
        menu_wrapper = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mMainmenu-wrap"))
        )
        
        # 獲取所有主分類標題元素
        menu_titles = menu_wrapper.find_elements(By.CLASS_NAME, "mMenumenu-cate-link")
        
        
        # 檢查標題數量是否匹配
        assert len(menu_titles) == len(expected_titles), \
            f"預期有 {len(expected_titles)} 個標題，但找到 {len(menu_titles)} 個"
        
        # 逐一檢查每個標題
        actual_titles = [title.text.strip() for title in menu_titles]
        for expected, actual in zip(expected_titles, actual_titles):
            logger.info(f"預期: {expected} 實際: {actual}")
            assert expected == actual, \
                f"標題不匹配 - 預期: {expected}, 實際: {actual}"
        
        logger.info("所有主選單大標題檢查通過")
        
    except Exception as e:
        logger.error(f"主選單大標題檢查失敗: {str(e)}")
        raise

def test_nav_news_anchor_redirect(driver,reset_state):
    try:
        logger.info("點擊最新消息並檢查錨點跳轉")
        
        # 先找到主選單容器並滾動
        menu_wrapper = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mMainmenu-wrap"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'start', behavior: 'smooth'});", menu_wrapper)
        time.sleep(2)
        

        news_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mmBulletin"))
        )
        
        # 確保可見並點擊
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", news_link)
        time.sleep(1)
        
        news_link.click()
        time.sleep(2)
        
        news_section = driver.find_element(By.CLASS_NAME, "mBulletin-tabs")
        assert news_section.is_displayed(), "未跳轉至最新消息區塊"
        
        logger.info("最新消息錨點跳轉測試通過")
        
    except Exception as e:
        logger.error(f"最新消息錨點跳轉測試失敗: {str(e)}")
        raise
        

def test_nav_books_anchor_redirect(driver,reset_state):
    try:
        logger.info("點擊楓葉圖書並檢查錨點跳轉")
        # 先找到主選單容器並滾動
        menu_wrapper = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mMainmenu-wrap"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'start', behavior: 'smooth'});", menu_wrapper)
        time.sleep(2)
        
        books_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mmMedia"))
        )
        books_link.click()
        time.sleep(2)
        books_section = driver.find_element(By.CLASS_NAME, "mPageTitle")
        assert books_section.is_displayed(), "未跳轉至職業介紹區塊"
        logger.info("楓葉圖書錨點跳轉測試通過")
    except Exception as e:
        logger.error(f"楓葉圖書錨點跳轉測試失敗: {str(e)}")
        raise

def test_nav_download_redirect(driver,reset_state):
    try:
        logger.info("點擊下載專區並檢查跳轉")
        # 先找到主選單容器並滾動
        menu_wrapper = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mMainmenu-wrap"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'start', behavior: 'smooth'});", menu_wrapper)
        time.sleep(2)
        
        download_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mmDownload"))
        )
        download_link.click()
        
        time.sleep(2)
        assert "download" in driver.current_url, "未跳轉至下載專區頁面"
        logger.info("下載專區跳轉測試通過")
    except Exception as e:
        logger.error(f"下載專區跳轉測試失敗: {str(e)}")
        raise


def test_nav_member_not_clickable(driver, reset_state):
    try:
        logger.info("檢查楓葉會員是否不可點擊")
        
        # 找到楓葉會員
        member_link = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'mMenumenu-cate-link') and text()='楓葉會員']"))
        )
        
        # 用 JavaScript 檢查 pointer-events 屬性
        pointer_events = driver.execute_script(
            "return window.getComputedStyle(arguments[0]).getPropertyValue('pointer-events');", 
            member_link
        )
        
        # 斷言 pointer-events 為 none
        assert pointer_events == "none", f"楓葉會員應不可點擊，但 pointer-events 是 '{pointer_events}'"
        
        logger.info("楓葉會員不可點擊測試通過")
        
    except Exception as e:
        logger.error(f"楓葉會員不可點擊測試失敗: {str(e)}")
        raise

'''
疑似棄用
# def test_nav_hk_redirect(driver, reset_state):
#     try:
#         logger.info("點擊香港專區並檢查跳轉")
#         #找到香港專區
#         hk_link = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'mMenumenu-cate-link') and text()='香港專區']"))
#         )
        
#         hk_link.click()
#         time.sleep(2)
#         assert "hk" in driver.current_url, "未跳轉至香港遊戲橘子官網"
#         logger.info("香港專區跳轉測試通過")
#     except Exception as e:
#         logger.error(f"香港專區跳轉測試失敗: {str(e)}")
#         raise
'''

def test_news_submenu_links(driver, reset_state):
    try:
        logger.info("開始測試最新消息子選單連結功能")
        
        # 先找到主選單容器並滾動
        menu_wrapper = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mMainmenu-wrap"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'start', behavior: 'smooth'});", menu_wrapper)
        time.sleep(0.5)

        # Hover 展開子選單
        news_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mmBulletin"))
        )
        ActionChains(driver).move_to_element(news_link).perform()
        time.sleep(0.5)

        # 檢查子選單是否展開
        submenu = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "mMenumenu-sub"))
        )
        assert submenu.is_displayed(), "最新消息子選單未展開"
        submenu_links = submenu.find_elements(By.TAG_NAME, "a")
        logger.info(f"子選單中找到 {len(submenu_links)} 個連結")

        # 關閉浮動按鈕並重新 hover
        try:
            watermarker = driver.find_element(By.CLASS_NAME, "mWatermarker")
            if watermarker.is_displayed():
                close_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "mWatermarker-close"))
                )
                close_button.click()
                logger.info("已關閉浮動按鈕")
                time.sleep(0.5)
                ActionChains(driver).move_to_element(news_link).perform()
                time.sleep(0.5)
                assert submenu.is_displayed(), "關閉浮動按鈕後子選單關閉"
        except TimeoutException:
            logger.info("未找到浮動按鈕或關閉按鈕，繼續測試")

        # 定義要測試的子選單錨點
        anchors = ["全部", "活動", "更新", "重要"]

        # 儲存原始窗口句柄
        original_window = driver.current_window_handle

        # 測試子選單中的四個錨點
        for anchor_text in anchors:
            logger.info(f"測試子選單錨點: {anchor_text}")
            link = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[@class='mMenumenu-sub']//a[contains(text(), '{anchor_text}')]"))
            )
            
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", link)
            time.sleep(0.5)
            logger.info(f"點擊前 class: {link.get_attribute('class')}")
            logger.info(f"點擊前位置: {link.location}, 大小: {link.size}")

            actions = ActionChains(driver)
            actions.move_to_element(news_link).pause(0.5).move_to_element(link).pause(0.5).click(link).perform()
            time.sleep(0.5)

            assert submenu.is_displayed(), f"點擊 {anchor_text} 後子選單關閉"

            try:
                active_link = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, f"//div[@class='mMenumenu-sub']//a[contains(text(), '{anchor_text}') and contains(@class, 'active')]"))
                )
                logger.info(f"點擊後 class: {active_link.get_attribute('class')}")
            except TimeoutException:
                logger.info(f"{anchor_text} 點擊後無 active 狀態，當前 class: {link.get_attribute('class')}")

        # 測試「合作聯繫」
        logger.info("測試合作聯繫連結")
        contact_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='mailto:maplestoryevent@gamania.com']"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", contact_link)
        time.sleep(0.5)

        # 記錄當前進程
        before_processes = {p.pid: p.name() for p in psutil.process_iter()}
        
        # 點擊合作聯繫
        actions = ActionChains(driver)
        actions.move_to_element(news_link).pause(0.5).move_to_element(contact_link).pause(0.5).click(contact_link).perform()
        time.sleep(1)

        # 多檢查幾次以捕捉進程
        email_process = None
        for _ in range(3):  # 重試 3 次，每次間隔 0.5 秒
            after_processes = {p.pid: p.name() for p in psutil.process_iter()}
            new_processes = set(after_processes.keys()) - set(before_processes.keys())
            
            for pid in new_processes:
                process_name = after_processes.get(pid, "").lower()
                if any(x in process_name for x in ["mailapp", "outlook", "thunderbird", "olk"]):
                    email_process = psutil.Process(pid)
                    logger.info(f"偵測到新 email 進程: {process_name} (PID: {pid})")
                    break
            if email_process:
                break
            time.sleep(0.5)

        if email_process:
            try:
                email_process.kill()
                logger.info(f"已強制關閉 email 進程: {email_process.name()} (PID: {email_process.pid})")
            except psutil.NoSuchProcess:
                logger.info("email 進程已自行關閉")
        else:
            if new_processes:
                logger.info("未找到預期 email 進程，列出所有新進程：")
                for pid in new_processes:
                    logger.info(f"PID: {pid}, Name: {after_processes.get(pid, '未知')}")
            else:
                logger.info("未偵測到任何新進程，email 視窗可能已快速關閉或未觸發")

        logger.info("最新消息子選單連結測試通過")
        
    except Exception as e:
        logger.error(f"最新消息子選單連結測試失敗: {str(e)}")
        raise

def test_maplebook_submenu_links(driver, reset_state):
    try:
        logger.info("開始測試楓葉圖書子選單連結功能")
        
        # 主選單容器
        menu_wrapper = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mMainmenu-wrap"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'start', behavior: 'smooth'});", menu_wrapper)
        time.sleep(0.5)

        # Hover 展開楓葉圖書子選單
        maplebook_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mmMedia"))
        )
        ActionChains(driver).move_to_element(maplebook_link).perform()
        time.sleep(0.5)

        # 檢查子選單
        submenu = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//a[@class='mMenumenu-cate-link mmMedia']/following-sibling::div[@class='mMenumenu-sub']"))
        )
        assert submenu.is_displayed(), "楓葉圖書子選單未展開"
        submenu_links = submenu.find_elements(By.TAG_NAME, "a")
        logger.info(f"子選單中找到 {len(submenu_links)} 個連結")

        # 定義子選單錨點
        anchors = [
            {"text": "職業介紹", "class": "mmRoles"},
            {"text": "系統介紹", "class": "mmSys"},
            {"text": "多媒體園地", "class": "mmArt"},
            {"text": "機率型道具說明", "href": "https://tw-event.beanfun.com/MapleStory/eventad/EventAD.aspx?EventADID=5325", "new_window": True},
            {"text": "聯盟戰地排行榜", "href": "https://tw-event.beanfun.com/MapleStory/UnionWebRank/Index.aspx", "redirect": True},
            {"text": "初入遊戲說明", "href": "https://tw-event.beanfun.com/MapleStory/eventad/EventAD.aspx?EventADID=10121", "new_window": True}
        ]

        # 儲存原始窗口句柄
        original_window = driver.current_window_handle

        # 測試子選單錨點
        for anchor in anchors:
            logger.info(f"測試子選單錨點: {anchor['text']}")
            if "href" in anchor:
                link = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, f"//div[@class='mMenumenu-sub']//a[contains(@href, '{anchor['href']}')]"))
                )
            else:
                link = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, f"//div[@class='mMenumenu-sub']//a[contains(@class, '{anchor['class']}')]"))
                )
            
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", link)
            time.sleep(0.5)
            initial_y = driver.execute_script("return window.scrollY;")
            logger.info(f"點擊前 class: {link.get_attribute('class')}")
            logger.info(f"點擊前位置: {link.location}, 大小: {link.size}, 視窗 Y: {initial_y}")

            # 點擊連結
            actions = ActionChains(driver)
            actions.move_to_element(maplebook_link).pause(0.5).move_to_element(link).pause(0.5).click(link).perform()
            time.sleep(1)

            # 根據連結類型處理
            if anchor.get("new_window", False):
                try:
                    WebDriverWait(driver, 5).until(lambda driver: len(driver.window_handles) > 1)
                    logger.info(f"{anchor['text']} 開啟新窗口")
                    new_window = [handle for handle in driver.window_handles if handle != original_window][0]
                    driver.switch_to.window(new_window)
                    logger.info(f"新窗口 URL: {driver.current_url}")
                    driver.close()
                    driver.switch_to.window(original_window)
                except TimeoutException:
                    logger.error(f"{anchor['text']} 未開啟新窗口，預期 target='_blank' 行為失敗，當前窗口數: {len(driver.window_handles)}")
                    raise
            elif anchor.get("redirect", False):
                try:
                    WebDriverWait(driver, 10).until(
                        lambda driver: "UnionWebRank" in driver.current_url,
                        f"{anchor['text']} 未跳轉到預期頁面"
                    )
                    logger.info(f"已跳轉到 URL: {driver.current_url}")
                    driver.back()
                    time.sleep(2)
                    maplebook_link = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "mmMedia"))
                    )
                    ActionChains(driver).move_to_element(maplebook_link).perform()
                    submenu = WebDriverWait(driver, 20).until(
                        EC.visibility_of_element_located((By.XPATH, "//a[@class='mMenumenu-cate-link mmMedia']/following-sibling::div[@class='mMenumenu-sub']"))
                    )
                    assert submenu.is_displayed(), f"返回後楓葉圖書子選單未展開"
                except TimeoutException:
                    logger.error(f"{anchor['text']} 未跳轉到預期頁面，當前 URL: {driver.current_url}")
                    raise
            else:
                assert submenu.is_displayed(), f"點擊 {anchor['text']} 後子選單關閉"
                new_y = driver.execute_script("return window.scrollY;")
                logger.info(f"點擊後視窗 Y: {new_y}")
                if new_y == initial_y:
                    logger.info(f"{anchor['text']} 未觸發視窗滑動，可能是正常行為")

        logger.info("楓葉圖書子選單連結測試通過")
        
    except Exception as e:
        logger.error(f"楓葉圖書子選單連結測試失敗: {str(e)}")
        raise

def test_download_submenu_links(driver, reset_state):
    try:
        logger.info("開始測試下載專區子選單連結功能")
        
        # 主選單容器
        menu_wrapper = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mMainmenu-wrap"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'start', behavior: 'smooth'});", menu_wrapper)
        time.sleep(0.5)

        # Hover 展開下載專區子選單
        download_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mmDownload"))
        )
        ActionChains(driver).move_to_element(download_link).perform()
        time.sleep(0.5)

        # 檢查子選單
        submenu = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//a[@class='mMenumenu-cate-link mmDownload']/following-sibling::div[@class='mMenumenu-sub']"))
        )
        assert submenu.is_displayed(), "下載專區子選單未展開"
        submenu_links = submenu.find_elements(By.TAG_NAME, "a")
        logger.info(f"子選單中找到 {len(submenu_links)} 個連結")

        # 關閉浮動按鈕
        try:
            watermarker = driver.find_element(By.CLASS_NAME, "mWatermarker")
            if watermarker.is_displayed():
                close_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "mWatermarker-close"))
                )
                close_button.click()
                logger.info("已關閉浮動按鈕")
                time.sleep(0.5)
                ActionChains(driver).move_to_element(download_link).perform()
                time.sleep(0.5)
                assert submenu.is_displayed(), "關閉浮動按鈕後子選單關閉"
        except TimeoutException:
            logger.info("未找到浮動按鈕或關閉按鈕，繼續測試")

        # 定義子選單錨點
        anchors = [
            {"text": "遊戲主程式", "href": "https://maplestory.beanfun.com/download", "redirect": True},
            {"text": "遊戲更新檔案", "href": "https://maplestory.beanfun.com/download?download_type=2", "redirect": True},
            {"text": "完整安裝說明", "href": "https://maplestory.beanfun.com/download?ins=install", "redirect": True},
            {"text": "手動更新說明", "href": "https://maplestory.beanfun.com/download?ins=update", "redirect": True},
            {"text": "遊戲配備需求", "href": "https://maplestory.beanfun.com/download?ins=require", "redirect": True}
        ]

        # 儲存原始窗口句柄
        original_window = driver.current_window_handle

        # 測試子選單錨點
        for anchor in anchors:
            logger.info(f"測試子選單錨點: {anchor['text']}")
            link = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[@class='mMenumenu-sub']//a[contains(@href, '{anchor['href']}')]"))
            )
            
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", link)
            time.sleep(0.5)
            initial_y = driver.execute_script("return window.scrollY;")
            logger.info(f"點擊前 class: {link.get_attribute('class')}")
            logger.info(f"點擊前位置: {link.location}, 大小: {link.size}, 視窗 Y: {initial_y}")

            # 點擊連結
            actions = ActionChains(driver)
            actions.move_to_element(download_link).pause(0.5).move_to_element(link).pause(0.5).click(link).perform()
            time.sleep(1)

            # 處理跳轉
            if anchor.get("redirect", False):
                try:
                    WebDriverWait(driver, 10).until(
                        lambda driver: anchor["href"] in driver.current_url,
                        f"{anchor['text']} 未跳轉到預期頁面"
                    )
                    logger.info(f"已跳轉到 URL: {driver.current_url}")
                    driver.back()
                    time.sleep(2)
                    download_link = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "mmDownload"))
                    )
                    ActionChains(driver).move_to_element(download_link).perform()
                    submenu = WebDriverWait(driver, 20).until(
                        EC.visibility_of_element_located((By.XPATH, "//a[@class='mMenumenu-cate-link mmDownload']/following-sibling::div[@class='mMenumenu-sub']"))
                    )
                    assert submenu.is_displayed(), f"返回後下載專區子選單未展開"
                except TimeoutException:
                    logger.error(f"{anchor['text']} 未跳轉到預期頁面，當前 URL: {driver.current_url}")
                    raise

        logger.info("下載專區子選單連結測試通過")
        
    except Exception as e:
        logger.error(f"下載專區子選單連結測試失敗: {str(e)}")
        raise

def test_membership_submenu_links(driver, reset_state):
    try:
        logger.info("開始測試楓葉會員子選單連結功能")
        
        # 一開始滑動到 y=1000
        driver.execute_script("window.scrollTo(0, 1000);")
        time.sleep(1)

        # Hover 展開楓葉會員子選單
        membership_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='mMenumenu-cate-link' and contains(text(), '楓葉會員')]"))
        )
        ActionChains(driver).move_to_element(membership_link).perform()
        time.sleep(1)

        # 檢查子選單
        submenu = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), '楓葉會員')]/following-sibling::div[@class='mMenumenu-sub']"))
        )
        assert submenu.is_displayed(), "楓葉會員子選單未展開"
        submenu_links = submenu.find_elements(By.TAG_NAME, "a")
        logger.info(f"子選單中找到 {len(submenu_links)} 個連結")

        # 定義子選單錨點
        anchors = [
            {"text": "修改第二組密碼", "href": "https://tw-event.beanfun.com/MapleStory/SetSecondPassword/index.aspx", "new_window": True},
            {"text": "客服中心", "href": "https://tw.beanfun.com/customerservice/www/main.aspx", "new_window": True},
            {"text": "外掛檢舉專區", "href": "https://event.beanfun.com/customerservice/PluginReporting/PluginBoard/PluginBoardJQ.aspx", "new_window": True},
            {"text": "道具兌換專區", "href": "https://tw-event.beanfun.com/maplestory/ItemToGame/Item_List.aspx", "new_window": True},
            {"text": "遊戲帳號申請", "href": "https://bfweb.beanfun.com/Register/register", "new_window": True},
            {"text": "序號查詢", "href": "https://maplestory.beanfun.com/sn_query", "redirect": True, "expected_url": "https://tw.newlogin.beanfun.com/loginform.aspx"},
            {"text": "遊戲管理規章", "href": "https://maplestory.beanfun.com/policy", "redirect": True},
            {"text": "Code of Conduct", "href": "https://maplestory.beanfun.com/policy?section=content07", "redirect": True},
            {"text": "處罰名單", "href": "https://maplestory.beanfun.com/blacklist", "redirect": True}
        ]

        # 儲存原始窗口句柄
        original_window = driver.current_window_handle

        # 測試子選單錨點
        for anchor in anchors:
            logger.info(f"測試子選單錨點: {anchor['text']}")
            link = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[@class='mMenumenu-sub']//a[contains(@href, '{anchor['href']}')]"))
            )
            
            driver.execute_script("window.scrollTo(0, 1000);")
            time.sleep(1)
            ActionChains(driver).move_to_element(membership_link).perform()
            time.sleep(1)
            
            initial_y = driver.execute_script("return window.scrollY;")
            logger.info(f"點擊前 class: {link.get_attribute('class')}")
            logger.info(f"點擊前位置: {link.location}, 大小: {link.size}, 視窗 Y: {initial_y}")

            # 點擊連結
            actions = ActionChains(driver)
            actions.move_to_element(membership_link).pause(1).move_to_element(link).pause(1).click(link).perform()
            time.sleep(1)

            # 根據連結類型處理
            if anchor.get("new_window", False):
                try:
                    WebDriverWait(driver, 5).until(lambda driver: len(driver.window_handles) > 1)
                    logger.info(f"{anchor['text']} 開啟新窗口")
                    new_window = [handle for handle in driver.window_handles if handle != original_window][0]
                    driver.switch_to.window(new_window)
                    logger.info(f"新窗口 URL: {driver.current_url}")
                    driver.close()
                    driver.switch_to.window(original_window)
                except TimeoutException:
                    logger.error(f"{anchor['text']} 未開啟新窗口，預期 target='_blank' 行為失敗，當前窗口數: {len(driver.window_handles)}")
                    raise
            elif anchor.get("redirect", False):
                try:
                    if anchor["text"] == "序號查詢":
                        expected_url = anchor["expected_url"]
                        WebDriverWait(driver, 10).until(
                            lambda driver: expected_url in driver.current_url,
                            f"{anchor['text']} 未跳轉到預期登入頁面"
                        )
                    else:
                        WebDriverWait(driver, 10).until(
                            lambda driver: anchor["href"] in driver.current_url,
                            f"{anchor['text']} 未跳轉到預期頁面"
                        )
                    logger.info(f"已跳轉到 URL: {driver.current_url}")
                    driver.get('https://maplestory.beanfun.com/main')
                    time.sleep(2)
                    driver.execute_script("window.scrollTo(0, 1000);")
                    time.sleep(1)
                    membership_link = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[@class='mMenumenu-cate-link' and contains(text(), '楓葉會員')]"))
                    )
                    ActionChains(driver).move_to_element(membership_link).perform()
                    submenu = WebDriverWait(driver, 20).until(
                        EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), '楓葉會員')]/following-sibling::div[@class='mMenumenu-sub']"))
                    )
                    assert submenu.is_displayed(), f"返回後楓葉會員子選單未展開"
                except TimeoutException:
                    logger.error(f"{anchor['text']} 未跳轉到預期頁面，當前 URL: {driver.current_url}")
                    raise

        logger.info("楓葉會員子選單連結測試通過")
        
    except Exception as e:
        logger.error(f"楓葉會員子選單連結測試失敗: {str(e)}")
        raise

def test_hongkong_submenu_links(driver, reset_state):
    try:
        logger.info("開始測試香港專區子選單連結功能")
        
        # 一開始滑動到 y=1000
        driver.execute_script("window.scrollTo(0, 1000);")
        time.sleep(2)

        # Hover 展開香港專區子選單
        hongkong_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'mMenumenu-cate-link') and contains(text(), '香港專區')]"))
        )
        logger.info("成功定位到 '香港專區' 主連結")
        ActionChains(driver).move_to_element(hongkong_link).perform()
        time.sleep(1)

        # 檢查子選單
        submenu = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), '香港專區')]/following-sibling::div[@class='mMenumenu-sub']"))
        )
        assert submenu.is_displayed(), "香港專區子選單未展開"
        submenu_links = submenu.find_elements(By.TAG_NAME, "a")
        logger.info(f"子選單中找到 {len(submenu_links)} 個連結")

        # 定義子選單連結
        submenu_items = [
            {"text": "申請會員帳號(港澳)", "href": "https://bfweb.hk.beanfun.com/beanfun_web_ap/signup/", "new_window": True},
            {"text": "創建遊戲帳號", "href": "https://bfweb.hk.beanfun.com/game_zone/", "new_window": True},
            {"text": "客服中心(港澳)", "href": "https://csp.hk.beanfun.com/", "new_window": True, "has_alert": True},
            {"text": "香港官網", "href": "https://bfweb.hk.beanfun.com/", "new_window": True}
        ]

        # 儲存原始窗口句柄
        original_window = driver.current_window_handle

        # 測試子選單連結
        for item in submenu_items:
            logger.info(f"測試子選單連結: {item['text']}")
            
            driver.execute_script("window.scrollTo(0, 1000);")
            time.sleep(1)
            hongkong_link = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'mMenumenu-cate-link') and contains(text(), '香港專區')]"))
            )
            ActionChains(driver).move_to_element(hongkong_link).perform()
            submenu = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), '香港專區')]/following-sibling::div[@class='mMenumenu-sub']"))
            )
            assert submenu.is_displayed(), f"測試 {item['text']} 前子選單未展開"
            
            link = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[@class='mMenumenu-sub']//a[contains(@href, '{item['href']}') and contains(text(), '{item['text']}')]"))
            )
            
            initial_y = driver.execute_script("return window.scrollY;")
            logger.info(f"點擊前 class: {link.get_attribute('class')}")
            logger.info(f"點擊前位置: {link.location}, 大小: {link.size}, 視窗 Y: {initial_y}")

            # 點擊連結
            actions = ActionChains(driver)
            actions.move_to_element(hongkong_link).pause(1).move_to_element(link).pause(1).click(link).perform()
            time.sleep(2)

            # 處理新窗口
            if item.get("new_window", False):
                current_windows = driver.window_handles
                logger.info(f"當前窗口數: {len(current_windows)}")
                
                if len(current_windows) > 1:
                    new_window = [handle for handle in current_windows if handle != original_window][0]
                    logger.info(f"{item['text']} 開啟新窗口")
                    
                    if item.get("has_alert", False):
                        logger.info(f"{item['text']} 檢測到可能有 alert，直接關閉新窗口")
                        driver.execute_script("window.close();", driver.switch_to.window(new_window))
                    else:
                        driver.switch_to.window(new_window)
                        logger.info(f"新窗口 URL: {driver.current_url}")
                        WebDriverWait(driver, 10).until(
                            lambda driver: driver.execute_script("return document.readyState") == "complete"
                        )
                        logger.info(f"{item['text']} 頁面載入完成")
                        driver.close()
                    
                    driver.switch_to.window(original_window)
                    time.sleep(1)
                else:
                    logger.error(f"{item['text']} 未開啟新窗口，測試失敗")
                    raise Exception(f"{item['text']} 未如預期開啟新窗口")

        logger.info("香港專區子選單連結測試通過")
        
    except Exception as e:
        logger.error(f"香港專區子選單連結測試失敗: {str(e)}")
        raise
        
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