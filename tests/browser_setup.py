import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_final_width = None
_final_height = None

def setup_browser_with_size(target_inner_width=1600, target_inner_height=731):
    global _final_width, _final_height
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "config.json")
    chromedriver_path = os.path.join(current_dir, "chromedriver.exe")
    logger.info(f"ChromeDriver 路徑: {chromedriver_path}")
    
    try:
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
            _final_width = config.get("final_width")
            _final_height = config.get("final_height")
            if _final_width is not None and _final_height is not None:
                logger.info(f"從設定檔讀取尺寸: {_final_width}x{_final_height}")
                service = Service(chromedriver_path)
                options = Options()
                options.add_argument("--headless")
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument(f"--window-size={_final_width},{_final_height}")
                driver = webdriver.Chrome(service=service, options=options)
                time.sleep(1)
                final_inner_width = driver.execute_script("return window.innerWidth;")
                final_inner_height = driver.execute_script("return window.innerHeight;")
                logger.info(f"驗證尺寸: innerWidth={final_inner_width}, innerHeight={final_inner_height}")
                return driver
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        logger.info(f"設定檔讀取失敗 ({str(e)})，開始計算尺寸")
    
    service = Service(chromedriver_path)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1000,1000")
    driver = webdriver.Chrome(service=service, options=options)
    time.sleep(2)
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
    driver = webdriver.Chrome(service=service, options=options)
    time.sleep(2)
    final_inner_width = driver.execute_script("return window.innerWidth;")
    final_inner_height = driver.execute_script("return window.innerHeight;")
    if final_inner_width != target_inner_width or final_inner_height != target_inner_height:
        width_diff = target_inner_width - final_inner_width
        height_diff = target_inner_height - final_inner_height
        _final_width = base_width + width_diff
        _final_height = base_height + height_diff
        driver.quit()
        options.add_argument(f"--window-size={_final_width},{_final_height}")
        driver = webdriver.Chrome(service=service, options=options)
        time.sleep(2)
        final_inner_width = driver.execute_script("return window.innerWidth;")
        final_inner_height = driver.execute_script("return window.innerHeight;")
    else:
        _final_width = base_width
        _final_height = base_height
    
    logger.info(f"計算結果: innerWidth={final_inner_width}, innerHeight={final_inner_height}")
    config = {"final_width": _final_width, "final_height": _final_height}
    with open(config_path, "w") as config_file:
        json.dump(config, config_file, indent=4)
    logger.info(f"尺寸已儲存到設定檔: {config_path}")
    return driver

def mobile_setup_browser():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("mobileEmulation", {"deviceName": "iPhone XR"})
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    return driver