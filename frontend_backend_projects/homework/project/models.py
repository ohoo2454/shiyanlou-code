from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Role(models.Model):
    '''
    用户角色的模型类
    '''
    ROLE_CHOICES = (
        (0, '学生'),
        (1, '教师')
    )
    user = models.OneToOneField(User, related_name='role', 
            on_delete=models.CASCADE)
    role = models.SmallIntegerField(choices=ROLE_CHOICES, 
            default=0, verbose_name='角色')
    
    def __str__(self):
        return str(self.role)


class UserAbstractModel(models.Model):
    '''
    教师角色与学生角色的抽象类
    '''
    GENDER_CHOICES = (
        (0, '男'),
        (1, '女')
    )
    name = models.CharField('姓名', default='', max_length=50)
    gender = models.SmallIntegerField('性别', choices=GENDER_CHOICES, 
            default=0)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    modified = models.DateTimeField('最后更改时间', auto_now=True)
    description = models.TextField('个人描述', null=True)

    class Meta:
        abstract = True


class Teacher(UserAbstractModel):
    '''
    教师角色的模型类
    '''
    user = models.OneToOneField(Role, related_name='teacher', 
            on_delete=models.CASCADE)
    ranks = models.CharField('职称', default='无', max_length=50)

    def __str__(self):
        return self.name


class Student(UserAbstractModel):
    '''
    学生角色的模型类
    '''
    user = models.OneToOneField(Role, related_name='student', 
            on_delete=models.CASCADE)
    classes = models.CharField('班级', default='', max_length=50)

    def __str__(self):
        return self.user.user.username
    