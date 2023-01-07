from selenium import webdriver
from selenium.webdriver.common.by import By
from time import process_time
from rich import print
from rich.console import Console
import os
import pwinput

print("[bold violet]    Auto Itemcode ")
print("[bold] Made with 💜 Eryxiz")
print("\n[Step 1] Input your username and password")
userid = input("Username: ")
userpwd = pwinput.pwinput(prompt='Password: ', mask='*')
os.system('cls')
print("[bold violet]    Auto Itemcode ")
print("[bold] Made with 💜 Eryxiz")
print("\n[Step 2] Input your itemcode (When fill out type 'done') ")
itemcode = list()
count = 0
success_count = 0
failed_count = 0

while True:
    addtolist = input()
    if addtolist == "done":
        break
    else:
        itemcode.append(addtolist)

print(itemcode)

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument(f'user-agent={user_agent}')
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--disable-crash-reporter")
options.add_argument("--disable-extensions")
options.add_argument("--disable-in-process-stack-traces")
options.add_argument("--disable-logging")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--log-level=3")
options.add_argument("--output=/dev/null")
driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options, service_log_path='NUL')
driver.get("https://secure3.playpark.com/itemcode/AUItemCode/AuLogin.aspx")

#init rich console
console = Console(log_path=False)

t1_start = process_time()
os.system('cls')
with console.status("[bold green] ระบบกำลังทำการเติมโค้ดไอเท็ม ..") as status:
    for code_round in range(len(itemcode)):
        driver.implicitly_wait(1)
        ## Step 1 :: กดปุ่ม PlayID Login
        playid_btn = driver.find_element(By.ID, "ContentPlaceHolder1_imbPlayID")
        playid_btn.click()
        ## Step 2 :: ส่งค่า id password แล้วล็อคอิน
        playid_id = driver.find_element(By.ID, "ContentPlaceHolder1_txtUserLogin")
        playid_id.send_keys(userid)
        playid_pwd = driver.find_element(By.ID, "ContentPlaceHolder1_txtUserPwd")
        playid_pwd.send_keys(userpwd)
        playid_login_btn = driver.find_element(By.ID, "ContentPlaceHolder1_btnSubmit")
        playid_login_btn.click()
        ## Step 3 :: กรอกไอเท็มโค้ด และ logout ออก
        driver.implicitly_wait(1)
        code_box = driver.find_element(By.ID, "ContentPlaceHolder1_tbvalidatecode")
        code_box.send_keys(itemcode[count])
        count = count + 1
        submit_code = driver.find_element(By.ID, "ContentPlaceHolder1_IMBTEvent")
        submit_code.click()
        error_check = driver.find_elements(By.ID, "ContentPlaceHolder1_divError")
        task_round, task_itemcode = code_round+1, itemcode[count-1]
        if(error_check):
            msg_show = driver.find_element(By.ID, "ContentPlaceHolder1_msgShow").text
            logout_btn = driver.find_element(By.ID, "ContentPlaceHolder1_imbntBack")
            logout_btn.click()
            console.log(f"{task_round} เติมโค้ด [red]{task_itemcode}[/red] ล้มเหลว ❌ ({str(msg_show)})")
            failed_count = failed_count + 1
        else:
            item_name = driver.find_element(By.ID, "ContentPlaceHolder1_lbitemvale").text
            console.log(f"{task_round} เติมโค้ด [green]{task_itemcode}[/green] เสร็จสิ้นแล้ว ✔️ ได้รับไอเท็ม [yellow]{item_name}[/yellow]")
            success_count = success_count + 1
            driver.implicitly_wait(1)
            logout_btn = driver.find_element(By.ID, "ContentPlaceHolder1_ImBTClick")
            logout_btn.click()

t1_stop = process_time()
print("\n⌛️ Elapsed time :", t1_stop-t1_start)
print("✔️  Success : %d | ❌ Failled : %d " % (success_count, failed_count))
driver.close()