#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# 分页组件
class Pagination(object):
    """
    分页组件
    """

    def __init__(self, current_page, all_count, base_url, 
                 query_params, per_page=20, pager_page_count=11):
        """
        分页初始化
        :param current_page: 当前页码
        :param per_page: 每页显示数据条数
        :param all_count: 数据库中总条数
        :param base_url: 基础URL
        :param query_params: QueryDict对象，内部含所有当前URL的原条件
        :param pager_page_count: 页面上最多显示的页码数量
        """
        self.base_url = base_url
        try:
            self.current_page = int(current_page)
            if self.current_page <= 0:
                raise Exception()
        except Exception as e:
            self.current_page = 1
        self.per_page = per_page
        self.all_count = all_count
        self.query_params = query_params
        self.pager_page_count = pager_page_count
        self.half_pager_page_count = int(self.pager_page_count / 2)
        pager_count, b = divmod(self.all_count, self.per_page)
        if b != 0:
            pager_count += 1
        self.pager_count = pager_count
    
    # 获取数据值起始索引
    @property
    def start(self):
        """
        获取数据值起始索引
        :return:
        """
        return (self.current_page - 1) * self.per_page

    # 获取数据值结束索引
    @property
    def end(self):
        """
        获取数据值结束索引
        :return:
        """
        return self.current_page * self.per_page

    # 生成HTML页码
    def page_html(self):
        """
        生成html页码
        :return:
        """
        # 如果总页码数量小于页面允许显示最大页码数量
        if self.pager_count < self.pager_page_count:
            pager_start = 1
            pager_end = self.pager_count
        # 如果总页码数量大于等于页面允许显示最大页码数量
        else:
            # 如果当前页小于等于页面允许显示最大页码数量一半
            if self.current_page <= self.half_pager_page_count:
                pager_start = 1
                pager_end = self.pager_page_count
            # 如果当前页大于页面允许显示最大页码数量一半
            else:
                # 如果当前页+页面允许显示最大页码数量一半超出总页码数量
                if (self.current_page + self.half_pager_page_count) \
                        > self.pager_count:
                    pager_start = self.pager_count - self.pager_page_count + 1
                    pager_end = self.pager_count
                # 如果当前页+页面允许显示最大页码数量一半未超出总页码数量
                else:
                    pager_start = self.current_page - \
                            self.half_pager_page_count
                    pager_end = self.current_page + self.half_pager_page_count
        page_list = []
        if self.current_page <= 1:
            prev = '<li><a href="#">上一页</a></li>'
        else:
            self.query_params['page'] = self.current_page - 1
            prev = '<li><a href="%s?%s">上一页</a></li>' % (self.base_url, 
                    self.query_params.urlencode())
        page_list.append(prev)
        for i in range(pager_start, pager_end + 1):
            self.query_params['page'] = i
            if self.current_page == i:
                tpl = '<li class="active"><a href="%s?%s">%s</a></li>' % (
                        self.base_url, self.query_params.urlencode(), i)
            else:
                tpl = '<li><a href="%s?%s">%s</a></li>' % (self.base_url, 
                        self.query_params.urlencode(), i)
            page_list.append(tpl)
        if self.current_page >= self.pager_count:
            nex = '<li><a href="#">下一页</a></li>'
        else:
            self.query_params['page'] = self.current_page + 1
            nex = '<li><a href="%s?%s">下一页</a></li>' % (self.base_url, 
                    self.query_params.urlencode())
        page_list.append(nex)
        page_str = ''.join(page_list)
        return page_str
