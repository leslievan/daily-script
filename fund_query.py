import requests
from bs4 import BeautifulSoup
import re
import csv
import datetime
import uuid

# 读取 code.txt 文件中的字符串列表
try:
    with open("code.txt", "r") as file:
        code_list = file.read().splitlines()
except FileNotFoundError:  # 文件不存在时
    # 创建一个空的code.txt文件
    with open("code.txt", "w") as file:
        pass
    code_list = []

pattern = r"^(.*?)\("

result_list = []

for code in code_list:
    url = f"http://fund.eastmoney.com/{code}.html?spm=001.1.swh"
    response = requests.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("title").text
    title = re.match(pattern, title).group(1)

    dataItem01 = soup.find("dl", class_="dataItem01")
    latest1month_span = dataItem01.find_all("dd")[1].find_all("span")[1]
    latest1month = latest1month_span.text if latest1month_span else ""

    latest1year_span = dataItem01.find_all("dd")[2].find_all("span")[1]
    latest1year = latest1year_span.text if latest1year_span else ""

    dataItem02 = soup.find("dl", class_="dataItem02")

    unitValue_span = dataItem02.find("dd", class_="dataNums").find("span")
    unitValue = unitValue_span.text if unitValue_span else ""
    fundDailyChange_span = dataItem02.find("dd", class_="dataNums").find_all("span")[1]
    fundDailyChange = fundDailyChange_span.text if unitValue_span else ""
    latest3month_span = dataItem02.find_all("dd")[1].find_all("span")[1]
    latest3month = latest3month_span.text if latest3month_span else ""
    latest3year_span = dataItem02.find_all("dd")[2].find_all("span")[1]
    latest3year = latest3year_span.text if latest3year_span else ""

    dataItem03 = soup.find("dl", class_="dataItem03")

    totalValue_span = dataItem03.find("dd", class_="dataNums").find("span")
    totalValue = totalValue_span.text if totalValue_span else ""
    latest6month_span = dataItem03.find_all("dd")[1].find_all("span")[1]
    latest6month = latest6month_span.text if latest6month_span else ""
    latestAll_span = dataItem03.find_all("dd")[2].find_all("span")[1]
    latestAll = latestAll_span.text if latestAll_span else ""

    result_list.append(
        [
            '="' + code + '"',
            title,
            unitValue,
            fundDailyChange,
            latest1month,
            latest3month,
            latest6month,
            latest1year,
            latestAll,
        ]
    )

# 写入结果到 CSV 文件
# 获取当前日期
current_date = datetime.datetime.now().strftime("%Y%m%d-%H%M")

# 生成4位UUID编码
uuid_code = uuid.uuid4().hex[:4]

# 拼接文件名
file_name = f"result-{current_date}-{uuid_code}.csv"

# 打开文件
with open(file_name, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(
        ["代码", "名称", "单位净值", "当日涨跌", "最近1月", "最近3月", "最近6月", "最近1年", "至今为止"]
    )
    writer.writerows(result_list)
