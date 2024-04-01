from faker import Faker
import datetime
import time

fake = Faker(locale='zh_CN')


# 基本变量
def pystring(Min: int = 5, Max: int = 5):
    """指定长度范围随机字母字符串"""
    return fake.pystr(min_chars=Min, max_chars=Max)


def pyfloat(left: int = 2, right: int = 2, positive: bool = True):
    """随机浮点数"""
    return fake.pyfloat(left, right, positive)


def number(Min: int = 0, Max: int = 100):
    """随机整数"""
    return fake.random_int(Min, Max)


# 日期时间
def date(ftime: str = '%Y-%m-%d'):
    """随机日期"""
    return fake.date(ftime)


def date_time(ftime: str = '%Y-%m-%d %H:%M:%S'):
    """随机日期"""
    return fake.date(ftime)


def calc_datetime(ftime="%Y-%m-%d %H:%M:%S", days=0, hours=0, minutes=0, seconds=0):
    """从当前时间获取前后时间"""
    now_time = datetime.datetime.now()
    if days or hours or minutes or seconds:
        return (now_time + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)).strftime(
            ftime)
    else:
        return now_time.strftime(ftime)


def month_start_day(ftime="%Y-%m-%d", months: int = 0, years: int = 0):
    """返回当前月份计算月份的第一天"""
    now = datetime.datetime.now()
    month = now.month - 1 + months
    year = now.year + month // 12 + years
    month = month % 12 + 1
    day = datetime.datetime(year, month, 1)
    return day.strftime(ftime)


def month_end_day(ftime="%Y-%m-%d", months: int = 0, years: int = 0):
    """返回当前月份计算月份的最后一天"""
    now = datetime.datetime.now()
    import calendar
    month = now.month - 1 + months
    year = now.year + month // 12 + years
    month = month % 12 + 1
    day = datetime.datetime(year, month, calendar.monthrange(year, month)[1])
    return day.strftime(ftime)


def timestamp():
    """返回当前时间时间戳（13位数）"""
    return int(time.time() * 1000)


# 个人信息
def phone():
    """随机手机号码"""
    return fake.phone_number()


def email():
    """随机邮箱"""
    return fake.email()


def name():
    """随机中文名带三个字符串，避免重名"""
    return fake.name() + pystring(3, 3)


def idcard():
    """随机身份证"""
    return fake.ssn()


# 地址变量
def address():
    """随机地址"""
    return fake.address()


def city():
    """随机城市"""
    return fake.city()


def province():
    """随机省份"""
    return fake.province()


def postcode():
    """随机邮编"""
    return fake.postcode()


# 文本信息
def paragraph(Max: int = 200):
    """随机一段中文文本"""
    text = fake.paragraph()
    return text if len(text) < Max else text[:Max]
