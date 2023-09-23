# 准备所有翻译任务的前置信息；包括数据库读取等构建参数
import os
from apikeys import DB_PORT, DB_USERNAME, DB_PASSWORD, DB_HOST, DB_DATABASE, ACCESS_ID, ACCESS_KEY
import pymysql

import pandas as pd
import numpy as np

# mysql database
# conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USERNAME,
#                        db=DB_DATABASE, password=DB_PASSWORD, charset='utf8')

from odps import ODPS
from odps import options

DEFAULT_PROJECT = 'cda'
END_POINT = 'http://service.cn-shenzhen.maxcompute.aliyun.com/api'
o = ODPS(ACCESS_ID, ACCESS_KEY, DEFAULT_PROJECT, endpoint=END_POINT)
options.tunnel.use_instance_tunnel = True
options.tunnel.limit_instance_tunnel = False  # 关闭limit限制，读取全部数据。

# import time
# import datetime
# now = datetime.datetime.now()
# # 上周一时间是
# lastMonday = datetime.datetime.strftime(
#     now - datetime.timedelta(now.weekday()) - datetime.timedelta(days=7), "%Y-%m-%d")
# 上周日时间是
# lastSunday = datetime.datetime.strftime(
#     now - datetime.timedelta(now.weekday()) - datetime.timedelta(days=1), "%Y-%m-%d").replace('-', '')


lang2line_name = {
    "JP": ["Japanese", "Japan"],
    "KR": ["Korean", "South Korea"],  # 韩国语
    "MY": ["Bahasa Malay", "Malaysia"],  # 马来语
    "CN": ["Chinese", "Taiwan"],  # 繁体中文； 这个不需要走翻译接口
    "TH": ["Thai", "Thailand"],  # 泰语
    "EN": ["English", "American"],
    "PH": ["wika ng Pilipino", "ang Pilipinas"],  # 菲律宾语
    "AR": ["بالعربية", "الشرق الأوسط"],  # 阿拉伯语
    "PL": ["Język polski", "Polska"]  # 波兰语
}

basePath = '../标准OCR文本数据已修正/difficultpicturedemo1/ocr_results'
files = os.listdir(basePath)
allTextList = []
for file in files:
    with open(os.path.join(basePath, file), 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if not line.strip():
                continue
            allTextList.append(line.strip())


def selectMaterialTable(dburl, port, un, psw, product_id, sale_id, line_code):
    # 查素材表： 获取完整的信息，包括广告语信息
    db = 'workflow_mc'
    conn = pymysql.connect(host=dburl, port=port, user=un, db=db, password=psw, charset='utf8')
    product_name, sale_name, ad_slogans, line_name = '', '', '', ''

    sqlmaterial = ''
    if product_id and sale_id:
        sqlmaterial = f"""
        select line_name, product_name, sale_name, ad_slogans, product_id, sale_id from tb_rp_mar_ad_material_df 
        where product_id = {product_id} and line_code = '{line_code}' limit 1
        """
    if product_id and not sale_id:
        sqlmaterial = f"""
        select line_name, product_name, sale_name, ad_slogans, product_id, sale_id from tb_rp_mar_ad_material_df 
        where product_id = {product_id} and line_code = '{line_code}' limit 1
        """
    if sale_id and not product_id:
        sqlmaterial = f"""
        select line_name, product_name, sale_name, ad_slogans, product_id, sale_id from tb_rp_mar_ad_material_df  
        where sale_id = '{sale_id}' and line_code = '{line_code}' limit 1
        """
        # sqlmaterial = f"""
        # select line_name, product_name, sale_name, ad_slogans, product_id, sale_id from tb_rp_mar_ad_material_df
        # where sale_id = '{sale_id}'
        # """
    targetData = pd.read_sql(sqlmaterial, conn)  # todo 从素材标中获取最全的信息
    if len(targetData) != 0:
        for index, row in enumerate(targetData.itertuples()):
            product_name = getattr(row, 'product_name')
            sale_name = getattr(row, 'sale_name')
            ad_slogans = getattr(row, 'ad_slogans')
            line_name = getattr(row, 'line_name')
            product_id = getattr(row, 'product_id')
            sale_id = getattr(row, 'sale_id')
            break
        return product_name, sale_name, ad_slogans, line_name, product_id, sale_id
    else:
        return '', '', '', '', product_id, sale_id


def selectMaxcomputeTable(dburl, port, un, psw, product_id, sale_id, line_code):
    # 没有广告语素材，只查询商品名
    db = 'maxcompute'
    conn = pymysql.connect(host=dburl, port=port, user=un, db=db, password=psw, charset='utf8')
    product_name, sale_name = '', ''

    sqlwithoutadslogan = ''
    if product_id and sale_id:
        sqlwithoutadslogan = f"""
            select sale_name, product_name,product_id, sale_id from tb_dim_pro_gk_sale_df a
        left join tb_dim_pub_gk_sys_country_df b on a.currency_id = b.currency_id 
        where a.product_id = {product_id} and b.code = '{line_code}' limit 1
        """
    if product_id and not sale_id:
        sqlwithoutadslogan = f"""
         select sale_name, product_name,product_id, sale_id from tb_dim_pro_gk_sale_df a
        left join tb_dim_pub_gk_sys_country_df b on a.currency_id = b.currency_id 
        where a.product_id = {product_id} and b.code = '{line_code}' limit 1
        """
    if sale_id and not product_id:
        sqlwithoutadslogan = f"""
        select sale_name, product_name,product_id, sale_id from tb_dim_pro_gk_sale_df a
        left join tb_dim_pub_gk_sys_country_df b on a.currency_id = b.currency_id 
        where a.sale_id = '{sale_id}'
        """
    targetData = pd.read_sql(sqlwithoutadslogan, conn)  # todo 从素材标中获取最全的信息

    for index, row in enumerate(targetData.itertuples()):
        product_name = getattr(row, 'product_name')
        sale_name = getattr(row, 'sale_name')
        product_id = getattr(row, 'product_id')
        sale_id = getattr(row, 'sale_id')
        break
    return product_name, sale_name, product_id, sale_id


def giilinProAliPor(product_id):
    sql = f""" select product_name from giikin_aliyun.tb_dim_pro_gk_ali_tags_df where product_id = '{product_id}' """
    product_name_ali = ''
    with o.execute_sql(sql).open_reader(tunnel=True) as reader:
        df = reader.to_pandas()
    for index, row in enumerate(df.itertuples()):
        product_name_ali = getattr(row, 'product_name')
    return product_name_ali


# todo 根据前端传入的参数查表构造参数
def part1toparams(product_id='', sale_id='', line_code=''):
    dburl = '192.168.4.51'
    port = 4000
    un = 'fanzhimin'
    psw = 'tit3hSCVwp82'
    product_name, sale_name, ad_slogans, line_name, product_id, sale_id = \
        selectMaterialTable(dburl, port, un, psw, product_id, sale_id, line_code)
    if not ad_slogans:
        _product_name_, _sale_name_, product_id, sale_id = \
            selectMaxcomputeTable(dburl, port, un, psw, product_id, sale_id, line_code)
        product_name_ali = giilinProAliPor(product_id)
        return (_product_name_, _sale_name_, product_id, sale_id, product_name_ali)
    else:
        product_name_ali = giilinProAliPor(product_id)
        return (product_name, sale_name, ad_slogans, line_name, product_id, sale_id, product_name_ali)
