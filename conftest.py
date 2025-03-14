import pytest
import logging
from browser_setup import setup_browser_with_size

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def driver():
    driver = setup_browser_with_size(1600, 731)
    logger.info("開始加載網頁")
    driver.get("https://maplestory.beanfun.com/main")
    driver.implicitly_wait(10)  # 設置隱式等待
    logger.info("頁面加載完成")
    yield driver
    logger.info("關閉瀏覽器")
    driver.quit()