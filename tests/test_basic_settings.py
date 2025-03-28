import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import warnings

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_page_display_normal(driver,reset_state):
    try:
        logger.info("檢查頁面是否正常顯示")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        logger.info("頁面主體已加載")
        assert driver.find_element(By.TAG_NAME, "body").is_displayed(), "頁面未正常顯示"
        logger.info("頁面顯示正常測試通過")
    except Exception as e:
        logger.error(f"頁面顯示測試失敗: {str(e)}")
        raise

def test_page_title_display_correct(driver,reset_state):
    try:
        logger.info("檢查頁面標題是否正確")
        title = driver.title
        logger.info(f"當前標題: {title}")
        assert title == "新楓之谷 maplestory 最團結的冒險！", "標題錯誤"
        logger.info("頁面標題顯示正確測試通過")
    except Exception as e:
        logger.error(f"標題顯示測試失敗: {str(e)}")
        raise

def test_page_reload_no_layout_error(driver,reset_state):
    try:
        logger.info("重新載入頁面")
        driver.refresh()
        time.sleep(2)
        logger.info("檢查頁面佈局")
        body = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        assert body.is_displayed(), "頁面重新載入後跑版或錯誤"
        logger.info("頁面重新載入無錯誤測試通過")
    except Exception as e:
        logger.error(f"頁面重新載入測試失敗: {str(e)}")
        raise

def test_page_navigation_no_layout_error(driver,reset_state):
    try:
        logger.info("模擬點擊上一頁")
        driver.execute_script("window.history.back();")
        time.sleep(2)
        logger.info("模擬點擊下一頁")
        driver.execute_script("window.history.forward();")
        time.sleep(2)
        body = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        assert body.is_displayed(), "上下一頁切換後跑版或錯誤"
        logger.info("頁面切換無錯誤測試通過")
    except Exception as e:
        logger.error(f"頁面切換測試失敗: {str(e)}")
        raise

def test_browser_tab_switch_no_layout_error(driver,reset_state):
    try:
        logger.info("模擬開新分頁並切換")
        driver.execute_script("window.open('about:blank', '_blank');")
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        body = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        assert body.is_displayed(), "分頁切換後跑版或錯誤"
        logger.info("分頁切換無錯誤測試通過")
    except Exception as e:
        logger.error(f"分頁切換測試失敗: {str(e)}")
        raise

def test_pc_loading_animation_on_first_visit(driver,reset_state):
    try:
        # 清空緩存和cookies以模擬首次進入
        logger.info("清空瀏覽器緩存和cookies")
        driver.delete_all_cookies()  # 清空所有cookies
        driver.execute_script("window.localStorage.clear();")  # 清空localStorage
        driver.execute_script("window.sessionStorage.clear();")  # 清空sessionStorage
        driver.refresh()
        
        logger.info("檢查進站動畫是否在頁面載入時出現並播放")
        video = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "mKvVideo"))
        )
        logger.info("找到進站動畫video元素")
        
        # 檢查video元素是否可見
        assert video.is_displayed(), "進站動畫未顯示"
        logger.info("進站動畫可見")
        
        # 檢查video是否正在播放（檢查autoplay屬性或當前播放時間）
        is_playing = driver.execute_script(
            "return arguments[0].currentTime > 0 && !arguments[0].paused && !arguments[0].ended;", 
            video
        )
        assert is_playing, "進站動畫未自動播放"
        logger.info("進站動畫自動播放測試通過")
    except Exception as e:
        logger.error(f"進站動畫測試失敗: {str(e)}")
        raise

if __name__ == "__main__":
    result = pytest.main(["-v", "--html=report.html", __file__])