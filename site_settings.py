import datetime
# 网站设置，请谨慎修改，修改后需重启服务器

# 可预约机器数量，请保持大于管理平台中的实际机器数量
OPEN_NUM = 8

# 不开放日期列表，请持续更新，除此以外的日期将全部开放
CLOSE_DATE_STR = ['2019-09-29', '2019-10-01']

# 管理员姓名和邮箱
ADMINS = [('Bingjun Luo', 'luobingjun@aliyun.com')]

# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True
EMAIL_HOST = ''
EMAIL_PORT = 465
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = '3D Printer Lab'
EMAIL_SUBJECT_PREFIX = '[预约平台]'
SERVER_EMAIL = '3D Printer Lab'
