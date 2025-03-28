import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.mark.dependency()
def test_menu_expansion(driver):
    try:
        logger.info("滾動到 Y=500")
        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(2)
        
        logger.info("查找 header_link")
        header_link = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.mMenumenu-cate-link.mmBulletin"))
        )
        logger.info("找到 header_link")
        
        logger.info("執行懸停操作")
        ActionChains(driver).move_to_element(header_link).perform()
        time.sleep(2)
        
        logger.info("查找 submenu")
        submenu = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "mMenumenu-sub"))
        )
        logger.info("找到 submenu")
        
        assert submenu.is_displayed(), "選單未展開"
        logger.info("Testcase 1: 選單展開測試通過")
    except Exception as e:
        logger.error(f"Testcase 1 失敗: {str(e)}")
        raise

@pytest.mark.dependency(depends=["test_menu_expansion"])
def test_page_navigation(driver):
    try:
        logger.info("查找 all_link")
        all_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.mMenumenu-sub-link.mmAll"))
        )
        logger.info("找到 all_link")
        
        logger.info("點擊 all_link")
        all_link.click()
        time.sleep(2)
        
        current_y = driver.execute_script("return window.scrollY;")
        expected_y = 1674
        tolerance = 10
        assert abs(current_y - expected_y) <= tolerance, (
            f"Testcase 2 失敗: 頁面未滾動到 Y={expected_y}, 當前 Y={current_y}"
        )
        logger.info(f"Testcase 2: 頁面滾動到 Y={current_y}，測試通過")
    except Exception as e:
        logger.error(f"Testcase 2 失敗: {str(e)}")
        raise
        


if __name__ == "__main__":
    result = pytest.main(["-v", "--html=report.html", __file__])