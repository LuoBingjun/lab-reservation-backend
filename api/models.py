from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.db.models import signals
from django.dispatch import receiver

# Create your models here.
# class Config(models.Model):
#     open_num = models.PositiveIntegerField()

class User(AbstractUser):
    phone = models.DecimalField(max_digits=11, decimal_places=0, null=True,verbose_name='电话号码')

class UserGroup(Group):
    max_reserve = models.PositiveIntegerField(verbose_name='最大预约量')
    class Meta:
        verbose_name = '用户组'
        verbose_name_plural = '用户组'


class Machine(models.Model):
    id = models.PositiveIntegerField(primary_key=True, verbose_name='编号')
    available = models.BooleanField(default=True, verbose_name='当前可用')  # 当前是否可用
    note = models.CharField(
        blank=True,
        null=True,
        max_length=128,
        verbose_name='备注'
    )

    def __str__(self):
        return '{0}号机器'.format(self.id)

    class Meta:
        verbose_name = '机器'
        verbose_name_plural = '机器'

class Operator(models.Model):
    id = models.DecimalField(primary_key=True, max_digits=11, decimal_places=0, verbose_name='学生/工作证号')
    name = models.CharField(max_length=32, verbose_name='姓名')

    def __str__(self):
        return '{0}({1})'.format(self.name, self.id)

    class Meta:
        verbose_name = '操作者'
        verbose_name_plural = '操作者'

class ReserveRecord(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE, verbose_name='用户')
    operator = models.ForeignKey(
        'Operator',
        on_delete=models.CASCADE,
        verbose_name='操作者'
    )
    date = models.DateField(verbose_name='日期')
    time = models.CharField(
        max_length=2,
        choices=[('AM', '上午'), ('PM', '下午'), ('OT', '其他')],
        verbose_name='时间'
    )
    special_time = models.TimeField(null=True, verbose_name='特殊预约时间')
    note = models.CharField(max_length=128, verbose_name='备注')
    submit_time = models.DateTimeField(auto_now=True, verbose_name='提交时间')
    checked = models.BooleanField(default=False, verbose_name='通过审核')

    def __str__(self):
        return '预约记录({0})'.format(self.id)

    class Meta:
        verbose_name = '预约记录'
        verbose_name_plural = '预约记录'

class BreachRecord(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE, verbose_name='用户')
    operator = models.ForeignKey(
        'Operator',
        on_delete=models.CASCADE,
        verbose_name='操作者'
    )
    date = models.DateField(verbose_name='日期')
    time = models.CharField(
        max_length=2,
        choices=[('AM', '上午'), ('PM', '下午'), ('OT', '其它')],
        verbose_name='时间'
    )
    note = models.CharField(max_length=128, verbose_name='备注')
    submit_time = models.DateTimeField(auto_now=True, verbose_name='提交时间')

    def __str__(self):
        return '违约记录({0})'.format(self.id)

    class Meta:
        verbose_name = '违约记录'
        verbose_name_plural = '违约记录'


class UseRecord(models.Model):
    machine = models.ForeignKey(
        'Machine',
        on_delete=models.CASCADE,
        verbose_name='机器'
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name='用户'
    )
    operator = models.ForeignKey(
        'Operator',
        on_delete=models.CASCADE,
        verbose_name='操作者'
    )
    start_time = models.DateTimeField(verbose_name='签到时间')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    note = models.CharField(max_length=128, verbose_name='备注')

    def __str__(self):
        return '使用记录({0})'.format(self.id)

    class Meta:
        verbose_name = '使用记录'
        verbose_name_plural = '使用记录'

@receiver(signals.post_save, sender=UseRecord)
def UseRecord_save(instance, **kwargs):
    instance.machine.available = False
    instance.machine.save()