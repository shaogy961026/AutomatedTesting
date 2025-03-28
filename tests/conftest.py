import pytest
import logging
from browser_setup import setup_browser_with_size,mobile_setup_browser

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def driver():
    driver = setup_browser_with_size(1600, 731)
    logger.info("開始加載網頁")
    driver.get("https://maplestory.beanfun.com/main")
    driver.implicitly_wait(10)  # 設置隱式等待
    logger.info("頁面加載完成")
    yield driver
    logger.info("關閉瀏覽器")
    driver.quit()
    
@pytest.fixture(scope="session")
def mobile_driver():
    """手機版測試環境"""
    mobile_driver = mobile_setup_browser()
    logger.info("開始加載mobile版網頁")
    mobile_driver.get("https://maplestory.beanfun.com/main")
    mobile_driver.implicitly_wait(10)
    logger.info("mobile頁面加載完成")
    yield mobile_driver
    logger.info("關閉mobile瀏覽器")
    mobile_driver.quit()

@pytest.fixture
def reset_state(driver):
    """桌機版: 每次測試開始前，回到首頁並重置滾動位置"""
    driver.get("https://maplestory.beanfun.com/main")  # 確保回到首頁
    driver.execute_script("window.scrollTo(0, 0);")  # 滾動回最上方
    
@pytest.fixture
def reset_mobile_state(mobile_driver):
    """手機版: 每次測試開始前，回到首頁並重置滾動位置"""
    logger.info("手機版: 重置狀態 -> 回到首頁並滾動到最上方")
    mobile_driver.get("https://maplestory.beanfun.com/main")  # 確保回到首頁
    mobile_driver.execute_script("window.scrollTo(0, 0);")  # 滾動回最上方