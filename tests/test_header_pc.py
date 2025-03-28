import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_gamania_logo_redirect_to_official(driver,reset_state):
    try:
        logger.info("查找遊戲橘子LOGO")
        logo = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "BF_Logo"))
        )
        logo.click()
        time.sleep(2)
        assert "https://tw.beanfun.com/" in driver.current_url, "未跳轉至遊戲橘子官網"
        logger.info("LOGO跳轉測試通過")
    except Exception as e:
        logger.error(f"LOGO跳轉測試失敗: {str(e)}")
        raise

@pytest.mark.dependency()
def test_game_dropdown_expandable(driver,reset_state):
    try:
        logger.info("查找遊戲下拉按鈕")
        game_btn = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "BF_Drop"))
        )
        ActionChains(driver).move_to_element(game_btn).perform()
        time.sleep(2)
        submenu = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "BF_Drop_menu"))
        )
        assert submenu.is_displayed(), "遊戲下拉選單未展開"
        logger.info("遊戲下拉展開測試通過")
    except Exception as e:
        logger.error(f"遊戲下拉展開測試失敗: {str(e)}")
        raise

@pytest.mark.dependency(depends=["test_game_dropdown_expandable"])
def test_game_dropdown_online_redirect(driver):
    try:
        logger.info("點擊線上遊戲選項")
        online_option = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "BFNavi_OnlineGame"))
        )
        online_option.click()
        time.sleep(2)
        assert "https://tw.beanfun.com/game_zone/" in driver.current_url, "未跳轉至線上遊戲館"
        logger.info("線上遊戲跳轉測試通過")
    except Exception as e:
        logger.error(f"線上遊戲跳轉測試失敗: {str(e)}")
        raise

'''
疑似棄用
# @pytest.mark.dependency()
# def test_game_dropdown_mobile_redirect(driver):
#     try:
#         logger.info("點擊手機遊戲選項")
#         mobile_option = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".game-dropdown-mobile"))
#         )
#         mobile_option.click()
#         time.sleep(2)
#         assert "mobile-games" in driver.current_url, "未跳轉至手機遊戲館"
#         logger.info("手機遊戲跳轉測試通過")
#     except Exception as e:
#         logger.error(f"手機遊戲跳轉測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_tw_dropdown_expandable(driver):
#     try:
#         logger.info("查找TW下拉按鈕")
#         tw_btn = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".tw-dropdown-btn"))
#         )
#         ActionChains(driver).move_to_element(tw_btn).perform()
#         time.sleep(2)
#         submenu = WebDriverWait(driver, 20).until(
#             EC.visibility_of_element_located((By.CSS_SELECTOR, ".tw-dropdown-menu"))
#         )
#         assert submenu.is_displayed(), "TW下拉選單未展開"
#         logger.info("TW下拉展開測試通過")
#     except Exception as e:
#         logger.error(f"TW下拉展開測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_tw_dropdown_taiwan_redirect(driver):
#     try:
#         logger.info("點擊Taiwan選項")
#         taiwan_option = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".tw-dropdown-taiwan"))
#         )
#         taiwan_option.click()
#         time.sleep(2)
#         assert "taiwan" in driver.current_url, "未跳轉至官網"
#         logger.info("Taiwan跳轉測試通過")
#     except Exception as e:
#         logger.error(f"Taiwan跳轉測試失敗: {str(e)}")
#         raise

# @pytest.mark.dependency()
# def test_header_content_layout_normal(driver):
#     try:
#         logger.info("檢查Header圖文排列")
#         content = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".header-content"))
#         )
#         assert content.is_displayed(), "Header圖文排列未正常顯示"
#         logger.info("Header圖文排列測試通過")
#     except Exception as e:
#         logger.error(f"Header圖文排列測試失敗: {str(e)}")
#         raise
     
'''
    
if __name__ == "__main__":
    result = pytest.main(["-v", "--html=report.html", __file__])


