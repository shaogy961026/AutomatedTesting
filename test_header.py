import pytest
import warnings
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

# 設置日誌以捕獲更多資訊
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

warnings.filterwarnings("ignore", category=DeprecationWarning)

_final_width = None
_final_height = None

def setup_browser_with_size(target_inner_width=1200, target_inner_height=900):
    global _final_width, _final_height
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")  # 增加穩定性
    options.add_argument("--disable-dev-shm-usage")  # 避免共享記憶體問題
    
    if _final_width is not None and _final_height is not None:
        options.add_argument(f"--window-size={_final_width},{_final_height}")
        logger.info("使用快取尺寸啟動瀏覽器")
        driver = webdriver.Chrome(service=service, options=options)
        time.sleep(1)
        final_inner_width = driver.execute_script("return window.innerWidth;")
        final_inner_height = driver.execute_script("return window.innerHeight;")
        logger.info(f"使用快取尺寸: innerWidth={final_inner_width}, innerHeight={final_inner_height}")
        return driver
    
    logger.info("第一次計算尺寸")
    options.add_argument("--window-size=1000,1000")
    driver = webdriver.Chrome(service=service, options=options)
    time.sleep(1)
    
    dpi = driver.execute_script("return window.devicePixelRatio;")
    inner_w = driver.execute_script("return window.innerWidth;")
    inner_h = driver.execute_script("return window.innerHeight;")
    logger.info(f"DPI={dpi}, 初始 innerWidth={inner_w}, innerHeight={inner_h}")
    
    width_scale = 1000 / inner_w if inner_w != 0 else 1
    height_scale = 1000 / inner_h if inner_h != 0 else 1
    
    base_width = int(target_inner_width / dpi * width_scale)
    base_height = int(target_inner_height / dpi * height_scale)
    
    driver.quit()
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--window-size={base_width},{base_height}")
    
    logger.info(f"設置初始尺寸: {base_width}x{base_height}")
    driver = webdriver.Chrome(service=service, options=options)
    time.sleep(1)
    
    final_inner_width = driver.execute_script("return window.innerWidth;")
    final_inner_height = driver.execute_script("return window.innerHeight;")
    
    if final_inner_width != target_inner_width or final_inner_height != target_inner_height:
        width_diff = target_inner_width - final_inner_width
        height_diff = target_inner_height - final_inner_height
        _final_width = base_width + width_diff
        _final_height = base_height + height_diff
        
        driver.quit()
        options.add_argument(f"--window-size={_final_width},{_final_height}")
        logger.info(f"微調後尺寸: {_final_width}x{_final_height}")
        driver = webdriver.Chrome(service=service, options=options)
        time.sleep(1)
        
        final_inner_width = driver.execute_script("return window.innerWidth;")
        final_inner_height = driver.execute_script("return window.innerHeight;")
    else:
        _final_width = base_width
        _final_height = base_height
    
    logger.info(f"第一次計算結果: innerWidth={final_inner_width}, innerHeight={final_inner_height}")
    return driver

@pytest.fixture(scope="module")
def driver():
    driver = setup_browser_with_size(1600, 731)
    logger.info("開始加載網頁")
    driver.get("https://maplestory.beanfun.com/main")
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    logger.info("頁面加載完成")
    yield driver
    logger.info("關閉瀏覽器")
    driver.quit()

@pytest.mark.dependency()
def test_menu_expansion(driver):
    try:
        logger.info("滾動到 Y=500")
        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(1)
        
        logger.info("查找 header_link")
        header_link = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "a.mMenumenu-cate-link.mmBulletin"))
        )
        logger.info("找到 header_link")
        
        logger.info("執行懸停操作")
        ActionChains(driver).move_to_element(header_link).perform()
        time.sleep(1)
        
        logger.info("查找 submenu")
        submenu = WebDriverWait(driver, 10).until(
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
        all_link = WebDriverWait(driver, 10).until(
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
    pytest.main(["-v", "--html=report.html"])