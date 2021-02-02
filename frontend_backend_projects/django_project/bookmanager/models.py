from django.db import models


# Create your models here.
class Author(models.Model):
    """
    作者模型类
    """
    name = models.CharField(verbose_name='姓名', max_length=32)


class Publisher(models.Model):
    """
    出版社模型类
    """
    name = models.CharField(verbose_name='名称', max_length=32)


class Book(models.Model):
    """
    书籍模型类
    """
    title = models.CharField(verbose_name='书名', max_length=32)
    price = models.DecimalField(verbose_name='价格', max_digits=6, 
                                decimal_places=2)
    authors = models.ManyToManyField(verbose_name='作者', to='Author')
    pub_date = models.DateTimeField(verbose_name='出版时间', 
                                    default='2020-10-10 10:10:10')
    pub = models.ForeignKey(verbose_name='出版社', to='Publisher', 
                            on_delete=models.CASCADE)
