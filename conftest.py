import pytest
import logging
import warnings
from browser_setup import setup_browser_with_size,mobile_setup_browser

# 設置日誌
logging.basicConfig(level=logging.INFO)  # 加回這行
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def driver():
    driver = setup_browser_with_size(1600, 731)
    logger.info("開始加載網頁")
    driver.get("https://maplestory.beanfun.com/main")
    driver.implicitly_wait(10)  # 設置隱式等待
    logger.info("頁面加載完成")
    yield driver
    driver.quit()
    
@pytest.fixture(scope="module")
def mobile_driver():
    """手機版測試環境"""
    driver = mobile_setup_browser()
    logger.info("開始加載mobile版網頁")
    driver.get("https://maplestory.beanfun.com/main")
    driver.implicitly_wait(10)
    logger.info("mobile頁面加載完成")
    yield driver
    driver.quit()
    