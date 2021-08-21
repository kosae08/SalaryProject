from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import load_workbook
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
import datetime
import time


# 로그인
def fall_login():
    driver.get("https://fall-mvp.com/")
    driver.find_element_by_name('userid').send_keys("kosae08")
    driver.find_element_by_name('userpass').send_keys("Joker0422")
    driver.find_element_by_xpath('//*[@id="loginForm1"]/button').click()
    time.sleep(1)

    if driver.current_url == "https://fall-mvp.com/main":
        return True
    else:
        return False


# 할당량 확인 시 return True, 아니면 False
def today_quota_check():
    sheet_wb = load_workbook("September.xlsx", data_only=True)
    sheet_ws = sheet_wb['달력']
    date = datetime.datetime.now()
    now = date.strftime("%Y-%m-%d")

    for row_count in range(5, 13, 1):
        for col_count in range(1, 7):
            if str(now) in str(sheet_ws.cell(row_count, col_count).value):
                today_row_count, today_col_count = row_count, col_count

    if sheet_ws.cell(today_row_count+1, today_col_count).value is None:
        return False
    else:
        return True


# 1.2 ~ 1.4 배당 확인
def fall_filtering():
    id_list = []
    team_list, odds_list, match_list = [], [], []
    driver.get("https://fall-mvp.com/main/cross.html")
    r = driver.page_source
    soup = BeautifulSoup(r, 'html.parser')

    for top in soup.find_all('ul', class_='g_item'):
        for mid in top.find_all('li'):
            for bot in mid.find_all('span', class_='g_home_odd_n'):
                if "," in str(bot.get_text().strip()):
                    if 1.2 < float(str(bot.get_text().strip()).replace(",", "")) < 1.4:
                        odds_list.append(str(bot.get_text().strip()).replace(",", ""))
                        id_list.append(mid.get('id'))
                        for team in mid.find_all('span', class_='g_away_n'):
                            team_list.append(team.get_text().strip())
                        for match in top.find_all('li', class_='g_day'):
                            match_list.append("2021-" + str(match.get_text().strip()))
                else:
                    if 1.2 < float(str(bot.get_text().strip()).replace(",", "")) < 1.4:
                        odds_list.append(str(bot.get_text().strip()).replace(",", ""))
                        id_list.append(mid.get('id'))
                        for team in mid.find_all('span', class_='g_home_n'):
                            team_list.append(team.get_text().strip())
                        for match in top.find_all('li', class_='g_day'):
                            match_list.append("2021-" + str(match.get_text().strip()))
            for bot in mid.find_all('span', class_='g_away_odd_n'):
                if "," in str(bot.get_text().strip()):
                    if 1.2 < float(str(bot.get_text().strip()).replace(",", "")) < 1.4:
                        odds_list.append(str(bot.get_text().strip()).replace(",", ""))
                        id_list.append(mid.get('id'))
                        for team in mid.find_all('span', class_='g_away_n'):
                            team_list.append(team.get_text().strip())
                        for match in top.find_all('li', class_='g_day'):
                            match_list.append("2021-" + str(match.get_text().strip()))
                else:
                    if 1.2 < float(str(bot.get_text().strip()).replace(",", "")) < 1.4:
                        odds_list.append(str(bot.get_text().strip()).replace(",", ""))
                        id_list.append(mid.get('id'))
                        for team in mid.find_all('span', class_='g_away_n'):
                            team_list.append(team.get_text().strip())
                        for match in top.find_all('li', class_='g_day'):
                            match_list.append("2021-" + str(match.get_text().strip()))

    match_list_input(id_list, team_list, odds_list, match_list)


# 엑셀 파일에 저장
# user_data1 = 아이디, user_data2 = 팀 이름, user_data3 = 팀 배당, user_data4 = 경기 시간
def match_list_input(user_data1, user_data2, user_data3, user_data4):
    user_list_1 = []
    sheet_wb = load_workbook("September.xlsx", data_only=True)
    sheet_ws = sheet_wb['경기리스트']

    row_count = 1

    while sheet_ws.cell(row_count, 3).value is not None:
        user_list_1.append(sheet_ws.cell(row_count, 3).value)
        row_count += 1
    start_row = sheet_ws.max_row

    for match, source_id, team, odds in zip(user_data4, user_data1, user_data2, user_data3):
        if team not in user_list_1:
            sheet_ws.cell(start_row, 1).value = match
            sheet_ws.cell(start_row, 2).value = source_id
            sheet_ws.cell(start_row, 3).value = team
            sheet_ws.cell(start_row, 4).value = odds
        start_row += 1
    sheet_wb.save("September.xlsx")


# 경기 목록 리스트업 후 사용자의 입력을 받아 베팅 진행
def betting_system():
    sheet_wb = load_workbook("September.xlsx")
    sheet_ws = sheet_wb['경기리스트']

    row_count = 1

    while sheet_ws.cell(row_count, 2).value is not None:
        # now_filtering = datetime.datetime.now() - datetime.datetime.strptime(sheet_ws.cell(row_count, 1).value, "%y-%M-%d %H:%M")
        match = sheet_ws.cell(row_count, 1).value
        match_datetime = datetime.datetime.strptime(match, "%Y-%m-%d %H:%M")
        difference = match_datetime - datetime.datetime.now()
        if int(difference.days) == 0:
            print(str(row_count) + "       " + sheet_ws.cell(row_count, 1).value + sheet_ws.cell(row_count, 2).value
                  + sheet_ws.cell(row_count, 3).value + sheet_ws.cell(row_count, 4).value)
        row_count += 1

    input_match_no = int(input("경기를 골라주세요: "))
    input_account = input("금액을 입력해주세요: ")

    # if driver.find_element_by_id(sheet_ws.cell(input_match_no, 2).value):
    #     driver.find_element_by_id(sheet_ws.cell(input_match_no, 2).value).click()
    # else:
    #     pass
    #
    # driver.find_element_by_id('nAmt').send_keys(input_account)
    # driver.find_element_by_xpath('//*[@id="cart"]/div[3]/button').send_keys(Keys.ENTER)
    # time.sleep(1)
    # alert = Alert(driver)
    # alert.accept()


def results_check():
    home_win_list, draw_win_list, away_win_list = [], [], []
    team_list, match_list = [], []

    page_count = 0

    url = "https://fall-mvp.com/main/result/D/"
    url_a = ".html"

    while page_count < 101:
        com_url = url + str(page_count) + url_a

        driver.get(com_url)
        r = driver.page_source
        soup = BeautifulSoup(r, 'html.parser')

        for top in soup.find_all('li', class_='g_home_ed g_gr_o'):
            for mid in top.find_all('span', class_='g_home_o'):
                home_win_list.append(mid.get_text().strip())
        for top in soup.find_all('li', class_='g_away_ed g_gr_o'):
            for mid in top.find_all('span', class_='g_away_o'):
                away_win_list.append(mid.get_text().strip())
        page_count += 25

    sheet_wb = load_workbook("September.xlsx")
    sheet_ws = sheet_wb['경기리스트']

    row_count = 1

    while sheet_ws.cell(row_count, 1).value is not None:
        if sheet_ws.cell(row_count, 3).value in home_win_list or sheet_ws.cell(row_count, 3).value in away_win_list:
            sheet_ws.cell(row_count, 5).value = "적중"
        row_count += 1

    sheet_wb.save("September.xlsx")


if __name__ == '__main__':
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    # if fall_login():
    betting_system()
    #     fall_filtering()
    #     results_check()


# 베팅 전 목록 리스트업 과정에서 현재 시간보다 지난 경기 제외
