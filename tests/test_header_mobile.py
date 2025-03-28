import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.mark.dependency()
def test_mobile_no_header(mobile_driver,reset_mobile_state):
    try:
        # 等待頁面載入
        WebDriverWait(mobile_driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        logger.info("頁面主體已加載")

        # 檢查是否有class為"BF_MainMenu"的元素
        logger.info("檢查是否有class='BF_MainMenu'的Header元素")
        header_elements = mobile_driver.find_elements(By.CLASS_NAME, "BF_MainMenu")
        
        if header_elements:
            # 如果找到元素，檢查它是否可見
            header = header_elements[0]
            logger.info(f"找到Header元素: {header.get_attribute('outerHTML')}")
            is_displayed = header.is_displayed()
            logger.info(f"Header是否可見: {is_displayed}")
            assert not is_displayed, "手機版Header元素存在且可見，不應顯示"
        else:
            logger.info("未找到class='BF_MainMenu'的Header元素")
        
    except Exception as e:
        logger.error(f"手機版無Header測試失敗: {str(e)}")
        raise

if __name__ == "__main__":
    result = pytest.main(["-v", "--html=report.html", __file__])