#encoding:utf-8
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from DBCrawler.items import HeXunItem
import re
import csv
import json
import os
from scrapy.conf import settings
from collections import OrderedDict

#Two step : 
#1.Parse cate name and event id from http://mac.hexun.com
class HeXunSpider(BaseSpider):
    name = "HeXun"
    allowed_domains = ["mac.hexun.com"]
    start_urls = [
        "http://mac.hexun.com/",
    ]
    indicatort_info = {}
    area_list = ['cityname', 'FProvince'];
    time_list = ['FYear', 'FMonth', 'year', 'FDate', 'FSeason', 'FEndDate'];
    exp_list = ['FNo', 'cityname', 'FProvince', 'FYear', 'FMonth', 'year', 'FDate', 'FSeason', 'FStartDate', 'FEndDate' ]

    def parse(self, response):
        self.totalpage = 0;
        hxs = HtmlXPathSelector(response)
        ids = hxs.select('//a[contains(@href, "Default.shtml?id=")]');
        i = 0
        for id in ids:
            id_param = re.match(r'Default.shtml\?id=(.*)', id.select('@href').extract()[0])
            if id_param is not None:
                #if id_param.group(1).strip() != 'D131W':
                #    continue;
                urllink = "http://mac.hexun.com/Details/" + id_param.group(1).strip() + ".shtml?pid=1";
                self.indicatort_info[id_param.group(1).strip()] = {}
                self.indicatort_info[id_param.group(1).strip()]['indicator'] = self.get_title(id_param.group(1).strip());
                yield Request(url=urllink, callback=self.parse_firestpage)
    
    def parse_firestpage(self, response):
        Item = HeXunItem()
        hxs = HtmlXPathSelector(response)
        matches = re.search(r'(.*)/(.*).shtml(.*)', response.url);
        if matches == None:
            return;
        key = matches.groups()[1]
        self.indicatort_info[key]['key'] = matches.groups()[1];
        item_keys = [];
        matches = re.findall(r'{item.(.*?)}', response.body);
        if len(matches) == 0:
            return;
        self.indicatort_info[key]['item_keys'] = matches;
        
        #"Talbe scroll_title, scroll_title1, scroll_list, scroll_list1";
        titlerows = len(hxs.select("//table[@id='scroll_title']/tr/td"))
        rows = hxs.select("//table[@id='scroll_title1']/tr")
        ids = rows.select("//table[@id='scroll_title1']/tr/td[contains(@id,'col')]/span/text()")
        ids2 = rows.select("//table[@id='scroll_title1']/tr/td/span/text()")
        if len(rows) == 0:
            return;
        cols = 0
        if len(ids) > 0 :
            cols = len(ids)
        else:
            cols = len(ids2);
        #initalize the titles
        titles = [[] for i in range(len(rows))]
        for i in range(len(rows)):
            for j in range(cols):
                titles[i].append('')
        curRow = 0
        curCol = 0
        for row in rows:
            tds = row.select("td")
            curCol = 0
            for i in range(cols):
                if titles[len(rows)-1][i] != '' :
                    curCol += 1;
                else:
                    break;
            colspan = 0
            rowspan = 0
            for td in tds:
                if len(td.select("@colspan").extract()) > 0:
                    colspan = int(td.select("@colspan").extract()[0])
                else:
                    colspan = 1
                if len(td.select("@rowspan").extract()) > 0:
                    rowspan = int(td.select("@rowspan").extract()[0])
                else:
                    rowspan = 1
                
                span = td.select("span/text()")

                for i in range(colspan):
                    titles[curRow + rowspan - 1][curCol + i] = (span.extract()[0]).encode('gbk');
                curCol += int(colspan)
            curRow += 1

        for i in range(len(titles[len(titles)-1])):
            title = '';
            for j in range(len(titles)):
                if j == len(titles) - 1:
                    if (titles[j][i]) != '':
                        title += (titles[j][i])
                else:
                    if (titles[j][i]) != '':
                        title += (titles[j][i])  + "-";
            titles[len(titles)-1][i] = title;
        
        # add title
        title_list = ['']
        title_list.append(self.indicatort_info[key]['indicator']);
        title_list.append(self.indicatort_info[key]['indicator']);
        title_list.append('HeXun');
        title_list.append(response.url);
        writer = csv.writer(file(settings['FILE_STORE_HEXUN'] + '/' + self.indicatort_info[key]['indicator'] + '.csv', 'wb'))
        writer.writerow(title_list)
        writer.writerow([])
        title_list = titles[len(titles)-1];

        for i in range(len(matches)):
            breakall = False
            for j in range(len(self.area_list)):
                if matches[i] == self.area_list[j]:
                    title_list.insert(0, ('地区').decode('utf-8').encode('GBK'));
                    breakall = True
                    break;
            if breakall:
                break;

        for i in range(len(matches)):
            breakall = False
            for j in range(len(self.time_list)):
                if matches[i] == self.time_list[j]:
                    title_list.insert(0, ('日期').decode('utf-8').encode('GBK'));
                    break;
            if breakall:
                break;
        
        writer.writerow(title_list)
        urllink = "http://mac.hexun.com/Details/" + self.indicatort_info[key]['key'] + ".ashx?pid=1"
        print urllink
        yield Request(url=urllink, callback=self.parse_content)

    def parse_content(self, response):
        matches = re.search(r'(.*)/(.*).ashx\?pid=(.*)', response.url);
        
        if matches == None:
            return;
        key = matches.groups()[1]
        page = int(matches.groups()[2])
        str1 = response.body;
        str1 = re.sub(r",FUpdateTime(.*?)\)", r'', str1)
        str1 = re.sub(r"{\s*(\w)", r'{"\1', str1)
        str1 = re.sub(r",\s*(\w)", r',"\1', str1)
        str1 = re.sub(r"(\w):", r'\1":', str1)
        
        data = json.loads(str1,object_pairs_hook=OrderedDict)
        self.indicatort_info[key]['pages'] = (data['Pages'])
        writer = csv.writer(file(settings['FILE_STORE_HEXUN'] + '/' + self.indicatort_info[key]['indicator'] + '.csv', 'ab'))
        
        for i in range(len(data['List'])):
            line = []
            timestr = ''
            for j in range(len(self.time_list)):
                if data['List'][i].has_key(self.time_list[j]):
                    timestr = str(data['List'][i][self.time_list[j]])
                    break
            if timestr == '':
                print 'Error : unrecognize time keyword';
                return;
            if len(timestr) == 6:
                timestr = timestr[:4] + '.' + timestr[4:]
            if len(timestr) == 8:
                timestr = timestr[:4] + '.' + timestr[4:]
                timestr = timestr[:7] + '.' + timestr[7:]
            line.append(timestr);
            for j in range(len(self.area_list)):
                if data['List'][i].has_key(self.area_list[j]):
                    line.append(data['List'][i][self.area_list[j]].encode('gbk'));
            for k in range(len(self.indicatort_info[key]['item_keys'])):
                bHas = False
                keyw = self.indicatort_info[key]['item_keys'][k]
                for j in range(len(self.exp_list)):
                    if keyw == self.exp_list[j]:
                        bHas = True
                        break;
                if bHas:
                    continue;
                if type(data['List'][i][keyw]) == int or type(data['List'][i][keyw]) == float:
                    line.append(str(data['List'][i][keyw]));
            if len(line) > 0:
                writer.writerow(line)
        if page < self.indicatort_info[key]['pages'] :
            urllink = "http://mac.hexun.com/Details/" + self.indicatort_info[key]['key'] + ".ashx?pid=" + str(page+1)
            yield Request(url=urllink, callback=self.parse_content)


    def get_title(self, key):
        for i in range(len(titles)):
            if titles[i]['key'] == key:
                return titles[i]['value'].decode('utf-8').encode('GBK');
        return 'undefined'

titles = [
            { "key": "A", "value": "国民经济核算" },
            { "key": "B", "value": "价格指数" },
            { "key": "C", "value": "财政税收" },
            { "key": "D", "value": "金融保险" },
            { "key": "E", "value": "三大产业" },
            { "key": "F", "value": "人口与就业" },
            { "key": "G", "value": "行业数据" },
            { "key": "H", "value": "其它数据" },
            { "key": "I", "value": "数据查询" },
            { "key": "A101Y", "value": "年度国内生产总值 - 国民经济核算" },
            { "key": "A102M", "value": "季度国内生产总值 - 国民经济核算" },
            { "key": "A103Y", "value": "支出法国内生产总值 - 国民经济核算" },
            { "key": "A104Y", "value": "国内生产总值增长率 - 国民经济核算" },
            { "key": "GDP",   "value": "年度地区国内生产总值 - 国民经济核算" },
            { "key": "GDPMonth", "value": "季度地区国内生产总值 - 国民经济核算" },
            { "key": "A201Y", "value": "国内生产总值指数（上年=100） - 国民经济核算" },
            { "key": "A202Y", "value": "国内生产总值指数(1978=100) - 国民经济核算" },
            { "key": "A301Y", "value": "居民消费水平与指数 - 国民经济核算" },
            { "key": "A302M", "value": "社会消费品零售总额 - 国民经济核算" },
            { "key": "A303MA", "value": "地区居民消费价格指数 - 国民经济核算" },
            { "key": "A303MB", "value": "地区商品零售价格指数 - 国民经济核算" },
            { "key": "A304M", "value": "社会消费品零售分类(按行业分) - 国民经济核算" },
            { "key": "A305M", "value": "社会消费品零售分类(按销售地区分) - 国民经济核算" },
            { "key": "A401Y", "value": "全国固定资产投资划分(按经济类型分) - 国民经济核算" },
            { "key": "A402Y", "value": "全国固定资产投资划分(按资金来源分) - 国民经济核算" },
            { "key": "A403M", "value": "城镇固定资产投资 - 国民经济核算" },
            { "key": "A404M", "value": "房地产开发投资情况(按全国分) - 国民经济核算" },
            { "key": "A405M", "value": "房地产投资同比增长 - 国民经济核算" },
            { "key": "A406M", "value": "房地产开发投资情况(按各地区分) - 国民经济核算" },
            { "key": "A407M", "value": "房地产施工竣工面积 - 国民经济核算" },
            { "key": "A408M", "value": "商品住宅施工竣工面积 - 国民经济核算" },
            { "key": "A409M", "value": "施工项目及计划总投资 - 国民经济核算" },
            { "key": "A410M", "value": "分行业固定资产投资 - 国民经济核算" },
            { "key": "A411M", "value": "按三大产业分固定投资 - 国民经济核算" },
            { "key": "A412M", "value": "城镇固定资产投资 - 国民经济核算" },
            { "key": "A413M", "value": "房地产开发完成投资 - 国民经济核算 - 国民经济核算" },
            { "key": "A414Y", "value": "固定资产投资增长率 - 国民经济核算 - 国民经济核算" },
            { "key": "A501Y", "value": "进出口贸易总额 - 国民经济核算 - 国民经济核算" },
            { "key": "A502Y", "value": "全国利用外资概况 - 国民经济核算" },
            { "key": "A503M", "value": "进出口商品总值表 - 国民经济核算" },
            { "key": "A504M", "value": "月度全国外商直接投资 - 国民经济核算" },
            { "key": "A507M", "value": "出口贸易方式总值 - 国民经济核算" },
            { "key": "A508M", "value": "进口贸易方式总值 - 国民经济核算" },
            { "key": "A509M", "value": "进出口企业性质总值 - 国民经济核算" },
            { "key": "A510M", "value": "月度出口额分产品 - 国民经济核算" },
            { "key": "A511M", "value": "月度出口量分产品 - 国民经济核算" },
            { "key": "A512M", "value": "月度进口额分产品 - 国民经济核算" },
            { "key": "A513M", "value": "月度进口量分产品 - 国民经济核算" },
            { "key": "B101Y", "value": "全国各种物价指数（上年＝100） - 价格指数" },
            { "key": "B102Y", "value": "全国各种物价指数（1950＝100） - 价格指数" },
            { "key": "B103M", "value": "全国物价指数 - 价格指数" },
            { "key": "B201M", "value": "地区居民消费价格指数 - 价格指数" },
            { "key": "B202M", "value": "央行企业商品价格指数 - 价格指数" },
            { "key": "B301M", "value": "工业品出厂价格指数 - 价格指数" },
            { "key": "B302M", "value": "主要工业品出厂价格指数 - 价格指数" },
            { "key": "B303M", "value": "原材料购进价格指数 - 价格指数" },
            { "key": "B401M", "value": "城市房地产价格指数 - 价格指数" },
            { "key": "B402M", "value": "房屋销售价格指数 - 价格指数" },
            { "key": "B404M", "value": "土地交易价格指数 - 价格指数" },
            { "key": "B405M", "value": "月度国房景气指数 - 价格指数" },
            { "key": "B406M", "value": "房屋租赁价格指数 - 价格指数" },
            { "key": "C101M", "value": "国家财政预算收入 - 财政税收" },
            { "key": "C102Y", "value": "国家财政收支总额 - 财政税收" },
            { "key": "C103Y", "value": "国家财政分项目收入 - 财政税收" },
            { "key": "C104Y", "value": "国家财政预算外收入 - 财政税收" },
            { "key": "C201Y", "value": "国家财政主要支出项目 - 财政税收" },
            { "key": "C202Y", "value": "国家财政预算支出 - 财政税收" },
            { "key": "C203Y", "value": "国家财政支出(用于科学研究支出) - 财政税收" },
            { "key": "C204Y", "value": "国家财政支出(用于农业支出) - 财政税收" },
            { "key": "C205Y", "value": "国家财政支出(用于抚恤和社会福利支出) - 财政税收" },
            { "key": "C206M", "value": "月度国家财政预算支出 - 财政税收" },
            { "key": "C301Y", "value": "年度各项税收收入 - 财政税收" },
            { "key": "D101Y", "value": "金融机构信贷资金平衡表(按资金来源分) - 金融保险" },
            { "key": "D102Y", "value": "金融机构信贷资金平衡表(按资金运用分) - 金融保险" },
            { "key": "D105Y", "value": "年度现金投放回笼差额 - 金融保险" },
            { "key": "D106M", "value": "月度货币供应量 - 金融保险" },
            { "key": "D107M", "value": "金融机构信贷收支表(按本外币分) - 金融保险" },
            { "key": "D108M", "value": "金融机构信贷收支表(按人民币分) - 金融保险" },
            { "key": "D109D", "value": "人民币汇率中间价统计 - 金融保险" },
            { "key": "D111M", "value": "月度货币供应数据 - 金融保险" },
            { "key": "D112M", "value": "月度人民币新增贷款 - 金融保险" },
            { "key": "D113M", "value": "银行家信心指数 - 金融保险" },
            { "key": "D114M", "value": "季度银行业景气指数 - 金融保险" },
            { "key": "D115M", "value": "贷款需求景气指数 - 金融保险" },
            { "key": "D116M", "value": "货币政策感受指数 - 金融保险" },
            { "key": "D117M", "value": "月度市场利率水平 - 金融保险" },
            { "key": "D118M", "value": "有效名义、实际汇率 - 金融保险" },
            { "key": "D119M", "value": "存款准备金率历次调整 - 金融保险" },
            { "key": "D120M", "value": "金融机构人民币基准利率(按存款分) - 金融保险" },
            { "key": "D121M", "value": "金融机构人民币基准利率(按贷款分) - 金融保险" },
            { "key": "D122M", "value": "境内美元存款利率 - 金融保险" },
            { "key": "D123D", "value": "上海银行同业拆放利率 - 金融保险" },
            { "key": "D124M", "value": "投资者开户地区分布(按地区分) - 其它数据" },
            { "key": "D125M", "value": "投资者开户地区分布(按类别分) - 其它数据" },
            { "key": "D130W", "value": "一周股票账户情况统计 - 其它数据" },
            { "key": "D131W", "value": "一周基金账户情况统计 - 其它数据" },
            { "key": "D132M", "value": "股改限售股份解禁减持 - 其它数据" },
            { "key": "D201Y", "value": "黄金和外汇储备 - 金融保险" },
            { "key": "D202Y", "value": "国际收支概况 - 金融保险" },
            { "key": "D204M", "value": "外汇储备和外汇占款 - 金融保险" },
            { "key": "E101Y", "value": "农林牧渔业总产值及指数(按全国分) - 三大产业" },
            { "key": "E102Y", "value": "农林牧渔业总产值及指数(按省分) - 三大产业" },
            { "key": "E103Y", "value": "主要农产品产量(按全国分) - 三大产业" },
            { "key": "E104Y", "value": "主要农产品产量(按省分) - 三大产业" },
            { "key": "E105Y", "value": "农业生产条件 - 三大产业" },
            { "key": "E201Y", "value": "工业企业总产值 - 三大产业" },
            { "key": "E202Y", "value": "工业总产值指数 - 三大产业" },
            { "key": "E203Y", "value": "主要工业产品产量(按全国分) - 三大产业" },
            { "key": "E204Y", "value": "主要工业产品产量(按省分) - 三大产业" },
            { "key": "E205M", "value": "工业增加值 - 三大产业" },
            { "key": "E206M", "value": "工业总产值 - 三大产业" },
            { "key": "E207M", "value": "工业销售产值 - 三大产业" },
            { "key": "E208Y", "value": "轻重工业总产值 - 三大产业" },
            { "key": "E209M", "value": "月度工业企业利润 - 三大产业" },
            { "key": "E210M", "value": "月度主要工业产量 - 三大产业" },
            { "key": "E211M", "value": "月度主要工业增加值 - 三大产业" },
            { "key": "E212M", "value": "工业产品销售率 - 三大产业" },
            { "key": "E213M", "value": "制造业采购经理指数 - 三大产业" },
            { "key": "E214M", "value": "企业主营收帐款净额 - 三大产业" },
            { "key": "E215M", "value": "工业企业主营业务收入 - 三大产业" },
            { "key": "E216M", "value": "工业经济效益综合指数 - 三大产业" },
            { "key": "E217M", "value": "工业产成品资金 - 三大产业" },
            { "key": "E218M", "value": "工业企业净利润率 - 三大产业" },
            { "key": "E301Y", "value": "运输线路长度 - 三大产业" },
            { "key": "E302Y", "value": "客运量 - 三大产业" },
            { "key": "E303Y", "value": "旅客周转量 - 三大产业" },
            { "key": "E304Y", "value": "货运量 - 三大产业" },
            { "key": "E305Y", "value": "货物周转量 - 三大产业" },
            { "key": "E306Y", "value": "旅客运输平均运距 - 三大产业" },
            { "key": "E307Y", "value": "货物运输平均运距 - 三大产业" },
            { "key": "E308Y", "value": "铁路平均每日装车数 - 三大产业" },
            { "key": "E309Y", "value": "主要货类铁路货运量 - 三大产业" },
            { "key": "E310Y", "value": "民用汽车拥有量 - 三大产业" },
            { "key": "E311M", "value": "交通运输量 - 三大产业" },
            { "key": "F101Y", "value": "全国人口数及其构成" },
            { "key": "F102Y", "value": "全国人口出生率死亡率 - 人口与就业" },
            { "key": "F201Y", "value": "就业和职工人数 - 人口与就业" },
            { "key": "F301Y", "value": "城乡居民家庭人均收入 - 人口与就业" },
            { "key": "F302Y", "value": "居民人民币储蓄存款 - 人口与就业" },
            { "key": "F303Y", "value": "职工工资总额及指数(按全国分) - 人口与就业" },
            { "key": "F304Y", "value": "职工工资总额及指数(按省分) - 人口与就业" },
            { "key": "F305M", "value": "城镇居民家庭基本情况 - 人口与就业" },
            { "key": "F306M", "value": "城镇收入与物价扩散指数 - 人口与就业" },
            { "key": "A101M0221", "value": "木材的采运 - 行业数据" }, 
            { "key": "A101M0222", "value": "竹材的采运 - 行业数据" }, 
            { "key": "A101M0512", "value": "农业服务业 - 行业数据" },
            { "key": "A101M0610", "value": "烟煤和无烟煤的开采洗选 - 行业数据" },
            { "key": "A101M0620", "value": "褐煤的开采洗选 - 行业数据" }, 
            { "key": "A101M0690", "value": "其他煤炭采选 - 行业数据" }, 
            { "key": "A101M0710", "value": "天然原油和天然气开采 - 行业数据" }, 
            { "key": "A101M0790", "value": "与石油有关的服务活动 - 行业数据" }, 
            { "key": "A101M0810", "value": "铁矿采选 - 行业数据" }, 
            { "key": "A101M0890", "value": "其他黑色金属矿采选 - 行业数据" }, 
            { "key": "A101M0911", "value": "铜矿采选 - 行业数据" }, 
            { "key": "A101M0912", "value": "铅锌矿采选 - 行业数据" }, 
            { "key": "A101M0913", "value": "镍钴矿采选 - 行业数据" }, { "key": "A101M0914", "value": "锡矿采选 - 行业数据" }, { "key": "A101M0915", "value": "锑矿采选 - 行业数据" }, { "key": "A101M0916", "value": "铝矿采选 - 行业数据" }, { "key": "A101M0917", "value": "镁矿采选 - 行业数据" }, { "key": "A101M0919", "value": "其他常用有色金属矿采选 - 行业数据" }, { "key": "A101M0931", "value": "钨钼矿采选 - 行业数据" }, { "key": "A101M0932", "value": "稀土金属矿采选 - 行业数据" }, { "key": "A101M0933", "value": "放射性金属矿采选 - 行业数据" }, { "key": "A101M0939", "value": "其他稀有金属矿采选 - 行业数据" }, { "key": "A101M1011", "value": "石灰石、石膏开采 - 行业数据" }, { "key": "A101M1012", "value": "建筑装饰用石开采 - 行业数据" }, { "key": "A101M1013", "value": "耐火土石开采 - 行业数据" }, { "key": "A101M1019", "value": "粘土及其他土砂石开采 - 行业数据" }, { "key": "A101M1020", "value": "化学矿采选 - 行业数据" }, { "key": "A101M1030", "value": "采盐 - 行业数据" }, { "key": "A101M1091", "value": "石棉、云母矿采选 - 行业数据" }, { "key": "A101M1092", "value": "石墨、滑石采选 - 行业数据" }, { "key": "A101M1093", "value": "宝石、玉石开采 - 行业数据" }, { "key": "A101M1099", "value": "其他非金属矿采选 - 行业数据" }, { "key": "A101M1100", "value": "其他采矿业 - 行业数据" }, { "key": "A101M1310", "value": "谷物磨制 - 行业数据" }, { "key": "A101M1320", "value": "饲料加工 - 行业数据" }, { "key": "A101M1331", "value": "食用植物油加工 - 行业数据" }, { "key": "A101M1332", "value": "非食用植物油加工 - 行业数据" }, { "key": "A101M1340", "value": "制糖 - 行业数据" }, { "key": "A101M1351", "value": "畜禽屠宰 - 行业数据" }, { "key": "A101M1352", "value": "肉制品及副产品加工 - 行业数据" }, { "key": "A101M1361", "value": "水产品冷冻加工 - 行业数据" }, { "key": "A101M1362", "value": "鱼糜制品及水产品干腌制加工 - 行业数据" }, { "key": "A101M1363", "value": "水产饲料制造 - 行业数据" }, { "key": "A101M1364", "value": "鱼油提取及制品的制造 - 行业数据" }, { "key": "A101M1369", "value": "其他水产品加工 - 行业数据" }, { "key": "A101M1370", "value": "蔬菜、水果和坚果加工 - 行业数据" }, { "key": "A101M1391", "value": "淀粉及淀粉制品的制造 - 行业数据" }, { "key": "A101M1392", "value": "豆制品制造 - 行业数据" }, { "key": "A101M1393", "value": "蛋品加工 - 行业数据" }, { "key": "A101M1399", "value": "其他未列明的农副食品加工 - 行业数据" }, { "key": "A101M1411", "value": "糕点、面包制造 - 行业数据" }, { "key": "A101M1419", "value": "饼干及其他焙烤食品制造 - 行业数据" }, { "key": "A101M1421", "value": "糖果、巧克力制造 - 行业数据" }, { "key": "A101M1422", "value": "蜜饯制作 - 行业数据" }, { "key": "A101M1431", "value": "米、面制品制造 - 行业数据" }, { "key": "A101M1432", "value": "速冻食品制造 - 行业数据" }, { "key": "A101M1439", "value": "方便面及其他方便食品制造 - 行业数据" }, { "key": "A101M1440", "value": "液体乳及乳制品制造 - 行业数据" }, { "key": "A101M1451", "value": "肉、禽类罐头制造 - 行业数据" }, { "key": "A101M1452", "value": "水产品罐头制造 - 行业数据" }, { "key": "A101M1453", "value": "蔬菜、水果罐头制造 - 行业数据" }, { "key": "A101M1459", "value": "其他罐头食品制造 - 行业数据" }, { "key": "A101M1461", "value": "味精制造 - 行业数据" }, { "key": "A101M1462", "value": "酱油、食醋及类似制品的制造 - 行业数据" }, { "key": "A101M1469", "value": "其他调味品、发酵制品制造 - 行业数据" }, { "key": "A101M1491", "value": "营养、保健食品制造 - 行业数据" }, { "key": "A101M1492", "value": "冷冻饮品及食用冰制造 - 行业数据" }, { "key": "A101M1493", "value": "盐加工 - 行业数据" }, { "key": "A101M1494", "value": "食品及饲料添加剂制造 - 行业数据" }, { "key": "A101M1499", "value": "其他未列明的食品制造 - 行业数据" }, { "key": "A101M1510", "value": "酒精制造 - 行业数据" }, { "key": "A101M1521", "value": "白酒制造 - 行业数据" }, { "key": "A101M1522", "value": "啤酒制造 - 行业数据" }, { "key": "A101M1523", "value": "黄酒制造 - 行业数据" }, { "key": "A101M1524", "value": "葡萄酒制造 - 行业数据" }, { "key": "A101M1529", "value": "其他酒制造 - 行业数据" }, { "key": "A101M1531", "value": "碳酸饮料制造 - 行业数据" }, { "key": "A101M1532", "value": "瓶（罐）装饮用水制造 - 行业数据" }, { "key": "A101M1533", "value": "果菜汁及果菜汁饮料制造 - 行业数据" }, { "key": "A101M1534", "value": "含乳饮料和植物蛋白饮料制造 - 行业数据" }, { "key": "A101M1535", "value": "固体饮料制造 - 行业数据" }, { "key": "A101M1539", "value": "茶饮料及其他软饮料制造 - 行业数据" }, { "key": "A101M1540", "value": "精制茶加工 - 行业数据" }, { "key": "A101M1610", "value": "烟叶复烤 - 行业数据" }, { "key": "A101M1620", "value": "烟制造 - 行业数据" }, { "key": "A101M1690", "value": "其他烟草制品加工 - 行业数据" }, { "key": "A101M1711", "value": "棉、化纤纺织加工 - 行业数据" }, { "key": "A101M1712", "value": "棉、化纤印染精加工 - 行业数据" }, { "key": "A101M1721", "value": "毛条加工 - 行业数据" }, { "key": "A101M1722", "value": "毛纺织 - 行业数据" }, { "key": "A101M1723", "value": "毛染整精加工 - 行业数据" }, { "key": "A101M1730", "value": "麻纺织 - 行业数据" }, { "key": "A101M1741", "value": "缫丝加工 - 行业数据" }, { "key": "A101M1742", "value": "绢纺和丝织加工 - 行业数据" }, { "key": "A101M1743", "value": "丝印染精加工 - 行业数据" }, { "key": "A101M1751", "value": "棉及化纤制品制造 - 行业数据" }, { "key": "A101M1752", "value": "毛制品制造 - 行业数据" }, { "key": "A101M1753", "value": "麻制品制造 - 行业数据" }, { "key": "A101M1754", "value": "丝制品制造 - 行业数据" }, { "key": "A101M1755", "value": "绳、索、缆的制造 - 行业数据" }, { "key": "A101M1756", "value": "纺织带和帘子布制造 - 行业数据" }, { "key": "A101M1757", "value": "无纺布制造 - 行业数据" }, { "key": "A101M1759", "value": "其他纺织制成品制造 - 行业数据" }, { "key": "A101M1761", "value": "棉、化纤针织品及编织品制造 - 行业数据" }, { "key": "A101M1762", "value": "毛针织品及编织品制造 - 行业数据" }, { "key": "A101M1763", "value": "丝针织品及编织品制造 - 行业数据" }, { "key": "A101M1769", "value": "其他针织品及编织品制造 - 行业数据" }, { "key": "A101M1810", "value": "纺织服装制造 - 行业数据" }, { "key": "A101M1820", "value": "纺织面料鞋的制造 - 行业数据" }, { "key": "A101M1830", "value": "制帽 - 行业数据" }, { "key": "A101M1910", "value": "皮革鞣制加工 - 行业数据" }, { "key": "A101M1921", "value": "皮鞋制造 - 行业数据" }, { "key": "A101M1922", "value": "皮革服装制造 - 行业数据" }, { "key": "A101M1923", "value": "皮箱、包袋制造 - 行业数据" }, { "key": "A101M1924", "value": "皮手套及皮装饰制品制造 - 行业数据" }, { "key": "A101M1929", "value": "其他皮革制品制造 - 行业数据" }, { "key": "A101M1931", "value": "毛皮鞣制加工 - 行业数据" }, { "key": "A101M1932", "value": "毛皮服装加工 - 行业数据" }, { "key": "A101M1939", "value": "其他毛皮制品加工 - 行业数据" }, { "key": "A101M1941", "value": "羽毛绒加工 - 行业数据" }, { "key": "A101M1942", "value": "羽毛绒制品加工 - 行业数据" }, { "key": "A101M2011", "value": "锯材加工 - 行业数据" }, { "key": "A101M2012", "value": "木片加工 - 行业数据" }, { "key": "A101M2021", "value": "胶合板制造 - 行业数据" }, { "key": "A101M2022", "value": "纤维板制造 - 行业数据" }, { "key": "A101M2023", "value": "刨花板制造 - 行业数据" }, { "key": "A101M2029", "value": "其他人造板、材制造 - 行业数据" }, { "key": "A101M2031", "value": "建筑用木料及木材组件加工 - 行业数据" }, { "key": "A101M2032", "value": "木容器制造 - 行业数据" }, { "key": "A101M2039", "value": "软木制品及其他木制品制造 - 行业数据" }, { "key": "A101M2040", "value": "竹、藤、棕、草制品制造 - 行业数据" }, { "key": "A101M2110", "value": "木质家具制造 - 行业数据" }, { "key": "A101M2120", "value": "竹、藤家具制造 - 行业数据" }, { "key": "A101M2130", "value": "金属家具制造 - 行业数据" }, { "key": "A101M2140", "value": "塑料家具制造 - 行业数据" }, { "key": "A101M2190", "value": "其他家具制造 - 行业数据" }, { "key": "A101M2210", "value": "纸浆制造 - 行业数据" }, { "key": "A101M2221", "value": "机制纸及纸板制造 - 行业数据" }, { "key": "A101M2222", "value": "手工纸制造 - 行业数据" }, { "key": "A101M2223", "value": "加工纸制造 - 行业数据" }, { "key": "A101M2231", "value": "纸和纸板容器的制造 - 行业数据" }, { "key": "A101M2239", "value": "其他纸制品制造 - 行业数据" }, { "key": "A101M2311", "value": "书、报、刊印刷 - 行业数据" }, { "key": "A101M2312", "value": "本册印制 - 行业数据" }, { "key": "A101M2319", "value": "包装装潢及其他印刷 - 行业数据" }, { "key": "A101M2320", "value": "装订及其他印刷服务活动 - 行业数据" }, { "key": "A101M2330", "value": "记录媒介的复制 - 行业数据" }, { "key": "A101M2411", "value": "文具制造 - 行业数据" }, { "key": "A101M2412", "value": "笔的制造 - 行业数据" }, { "key": "A101M2413", "value": "教学用模型及教具制造 - 行业数据" }, { "key": "A101M2414", "value": "墨水、墨汁制造 - 行业数据" }, { "key": "A101M2419", "value": "其他文化用品制造 - 行业数据" }, { "key": "A101M2421", "value": "球类制造 - 行业数据" }, { "key": "A101M2422", "value": "体育器材及配件制造 - 行业数据" }, { "key": "A101M2423", "value": "训练健身器材制造 - 行业数据" }, { "key": "A101M2424", "value": "运动防护用具制造 - 行业数据" }, { "key": "A101M2429", "value": "其他体育用品制造 - 行业数据" }, { "key": "A101M2431", "value": "中乐器制造 - 行业数据" }, { "key": "A101M2432", "value": "西乐器制造 - 行业数据" }, { "key": "A101M2433", "value": "电子乐器制造 - 行业数据" }, { "key": "A101M2439", "value": "其他乐器及零件制造 - 行业数据" }, { "key": "A101M2440", "value": "玩具制造 - 行业数据" }, { "key": "A101M2451", "value": "露天游乐场所游乐设备制造 - 行业数据" }, { "key": "A101M2452", "value": "游艺用品及室内游艺器材制造 - 行业数据" }, { "key": "A101M2511", "value": "原油加工及石油制品制造 - 行业数据" }, { "key": "A101M2512", "value": "人造原油生产 - 行业数据" }, { "key": "A101M2520", "value": "炼焦 - 行业数据" }, { "key": "A101M2530", "value": "核燃料加工 - 行业数据" }, { "key": "A101M2611", "value": "无机酸制造 - 行业数据" }, { "key": "A101M2612", "value": "无机碱制造 - 行业数据" }, { "key": "A101M2613", "value": "无机盐制造 - 行业数据" }, { "key": "A101M2614", "value": "有机化学原料制造 - 行业数据" }, { "key": "A101M2619", "value": "其他基础化学原料制造 - 行业数据" }, { "key": "A101M2621", "value": "氮肥制造 - 行业数据" }, { "key": "A101M2622", "value": "磷肥制造 - 行业数据" }, { "key": "A101M2623", "value": "钾肥制造 - 行业数据" }, { "key": "A101M2624", "value": "复混肥料制造 - 行业数据" }, { "key": "A101M2625", "value": "有机肥料及微生物肥料制造 - 行业数据" }, { "key": "A101M2629", "value": "其他肥料制造 - 行业数据" }, { "key": "A101M2631", "value": "化学农药制造 - 行业数据" }, { "key": "A101M2632", "value": "生物化学农药及微生物农药制造 - 行业数据" }, { "key": "A101M2641", "value": "涂料制造 - 行业数据" }, { "key": "A101M2642", "value": "油墨及类似产品制造 - 行业数据" }, { "key": "A101M2643", "value": "颜料制造 - 行业数据" }, { "key": "A101M2644", "value": "染料制造 - 行业数据" }, { "key": "A101M2645", "value": "密封用填料及类似品制造 - 行业数据" }, { "key": "A101M2651", "value": "初级形态的塑料及合成树脂制造 - 行业数据" }, { "key": "A101M2652", "value": "合成橡胶制造 - 行业数据" }, { "key": "A101M2653", "value": "合成纤维单聚合体的制造 - 行业数据" }, { "key": "A101M2659", "value": "其他合成材料制造 - 行业数据" }, { "key": "A101M2661", "value": "化学试剂和助剂制造 - 行业数据" }, { "key": "A101M2662", "value": "专项化学用品制造 - 行业数据" }, { "key": "A101M2663", "value": "林产化学产品制造 - 行业数据" }, { "key": "A101M2665", "value": "信息化学品制造 - 行业数据" }, { "key": "A101M2666", "value": "环境污染处理专用药剂材料制造 - 行业数据" }, { "key": "A101M2667", "value": "动物胶制造 - 行业数据" }, { "key": "A101M2669", "value": "其他专用化学产品制造 - 行业数据" }, { "key": "A101M2671", "value": "肥皂及合成洗涤剂制造 - 行业数据" }, { "key": "A101M2672", "value": "化妆品制造 - 行业数据" }, { "key": "A101M2673", "value": "口腔清洁用品制造 - 行业数据" }, { "key": "A101M2674", "value": "香料、香精制造 - 行业数据" }, { "key": "A101M2679", "value": "其他日用化学产品制造 - 行业数据" }, { "key": "A101M2710", "value": "化学药品原药制造 - 行业数据" }, { "key": "A101M2720", "value": "化学药品制剂制造 - 行业数据" }, { "key": "A101M2730", "value": "中药饮片加工 - 行业数据" }, { "key": "A101M2740", "value": "中成药制造 - 行业数据" }, { "key": "A101M2750", "value": "兽用药品制造 - 行业数据" }, { "key": "A101M2760", "value": "生物、生化制品的制造 - 行业数据" }, { "key": "A101M2770", "value": "卫生材料及医药用品制造 - 行业数据" }, { "key": "A101M2811", "value": "化纤浆粕制造 - 行业数据" }, { "key": "A101M2812", "value": "人造纤维（纤维素纤维）制造 - 行业数据" }, { "key": "A101M2821", "value": "锦纶纤维制造 - 行业数据" }, { "key": "A101M2822", "value": "涤纶纤维制造 - 行业数据" }, { "key": "A101M2823", "value": "腈纶纤维制造 - 行业数据" }, { "key": "A101M2824", "value": "维纶纤维制造 - 行业数据" }, { "key": "A101M2829", "value": "其他合成纤维制造 - 行业数据" }, { "key": "A101M2911", "value": "车辆、飞机及工程机械轮胎制造 - 行业数据" }, { "key": "A101M2912", "value": "力车胎制造 - 行业数据" }, { "key": "A101M2913", "value": "轮胎翻新加工 - 行业数据" }, { "key": "A101M2920", "value": "橡胶板、管、带的制造 - 行业数据" }, { "key": "A101M2930", "value": "橡胶零件制造 - 行业数据" }, { "key": "A101M2940", "value": "再生橡胶制造 - 行业数据" }, { "key": "A101M2950", "value": "日用及医用橡胶制品制造 - 行业数据" }, { "key": "A101M2960", "value": "橡胶靴鞋制造 - 行业数据" }, { "key": "A101M2990", "value": "其他橡胶制品制造 - 行业数据" }, { "key": "A101M3010", "value": "塑料薄膜制造 - 行业数据" }, { "key": "A101M3020", "value": "塑料板、管、型材的制造 - 行业数据" }, { "key": "A101M3030", "value": "塑料丝、绳及编织品的制造 - 行业数据" }, { "key": "A101M3040", "value": "泡沫塑料制造 - 行业数据" }, { "key": "A101M3050", "value": "塑料人造革、合成革制造 - 行业数据" }, { "key": "A101M3060", "value": "塑料包装箱及容器制造 - 行业数据" }, { "key": "A101M3070", "value": "塑料零件制造 - 行业数据" }, { "key": "A101M3081", "value": "塑料鞋制造 - 行业数据" }, { "key": "A101M3082", "value": "日用塑料杂品制造 - 行业数据" }, { "key": "A101M3090", "value": "其他塑料制品制造 - 行业数据" }, { "key": "A101M3111", "value": "水泥制造 - 行业数据" }, { "key": "A101M3112", "value": "石灰和石膏制造 - 行业数据" }, { "key": "A101M3121", "value": "水泥制品制造 - 行业数据" }, { "key": "A101M3122", "value": "砼结构构件制造 - 行业数据" }, { "key": "A101M3123", "value": "石棉水泥制品制造 - 行业数据" }, { "key": "A101M3124", "value": "轻质建筑材料制造 - 行业数据" }, { "key": "A101M3129", "value": "其他水泥制品制造 - 行业数据" }, { "key": "A101M3131", "value": "粘土砖瓦及建筑砌块制造 - 行业数据" }, { "key": "A101M3132", "value": "建筑陶瓷制品制造 - 行业数据" }, { "key": "A101M3133", "value": "建筑用石加工 - 行业数据" }, { "key": "A101M3134", "value": "防水建筑材料制造 - 行业数据" }, { "key": "A101M3135", "value": "隔热和隔音材料制造 - 行业数据" }, { "key": "A101M3139", "value": "其他建筑材料制造 - 行业数据" }, { "key": "A101M3141", "value": "平板玻璃制造 - 行业数据" }, { "key": "A101M3142", "value": "技术玻璃制品制造 - 行业数据" }, { "key": "A101M3143", "value": "光学玻璃制造 - 行业数据" }, { "key": "A101M3144", "value": "玻璃仪器制造 - 行业数据" }, { "key": "A101M3145", "value": "日用玻璃制品及玻璃包装容器制造 - 行业数据" }, { "key": "A101M3146", "value": "玻璃保温容器制造 - 行业数据" }, { "key": "A101M3147", "value": "玻璃纤维及制品制造 - 行业数据" }, { "key": "A101M3148", "value": "玻璃纤维增强塑料制品制造 - 行业数据" }, { "key": "A101M3149", "value": "其他玻璃制品制造 - 行业数据" }, { "key": "A101M3151", "value": "卫生陶瓷制品制造 - 行业数据" }, { "key": "A101M3152", "value": "特种陶瓷制品制造 - 行业数据" }, { "key": "A101M3153", "value": "日用陶瓷制品制造 - 行业数据" }, { "key": "A101M3159", "value": "园林、陈设艺术及其他陶瓷制品制 - 行业数据" }, { "key": "A101M3161", "value": "石棉制品制造 - 行业数据" }, { "key": "A101M3162", "value": "云母制品制造 - 行业数据" }, { "key": "A101M3169", "value": "耐火陶瓷制品及其他耐火材料制造 - 行业数据" }, { "key": "A101M3191", "value": "石墨及碳素制品制造 - 行业数据" }, { "key": "A101M3199", "value": "其他非金属矿物制品制造 - 行业数据" }, { "key": "A101M3210", "value": "炼铁 - 行业数据" }, { "key": "A101M3220", "value": "炼钢 - 行业数据" }, { "key": "A101M3230", "value": "钢压延加工 - 行业数据" }, { "key": "A101M3240", "value": "铁合金冶炼 - 行业数据" }, { "key": "A101M3311", "value": "铜冶炼 - 行业数据" }, { "key": "A101M3312", "value": "铅锌冶炼 - 行业数据" }, { "key": "A101M3313", "value": "镍钴冶炼 - 行业数据" }, { "key": "A101M3314", "value": "锡冶炼 - 行业数据" }, { "key": "A101M3315", "value": "锑冶炼 - 行业数据" }, { "key": "A101M3316", "value": "铝冶炼 - 行业数据" }, { "key": "A101M3317", "value": "镁冶炼 - 行业数据" }, { "key": "A101M3319", "value": "其他常用有色金属冶炼 - 行业数据" }, { "key": "A101M3331", "value": "钨钼冶炼 - 行业数据" }, { "key": "A101M3332", "value": "稀土金属冶炼 - 行业数据" }, { "key": "A101M3339", "value": "其他稀有金属冶炼 - 行业数据" }, { "key": "A101M3340", "value": "有色金属合金制造 - 行业数据" }, { "key": "A101M3351", "value": "常用有色金属压延加工 - 行业数据" }, { "key": "A101M3352", "value": "贵金属压延加工 - 行业数据" }, { "key": "A101M3353", "value": "稀有稀土金属压延加工 - 行业数据" }, { "key": "A101M3411", "value": "金属结构制造 - 行业数据" }, { "key": "A101M3412", "value": "金属门窗制造 - 行业数据" }, { "key": "A101M3421", "value": "切削工具制造 - 行业数据" }, { "key": "A101M3422", "value": "手工具制造 - 行业数据" }, { "key": "A101M3423", "value": "农用及园林用金属工具制造 - 行业数据" }, { "key": "A101M3424", "value": "刀剪及类似日用金属工具制造 - 行业数据" }, { "key": "A101M3429", "value": "其他金属工具制造 - 行业数据" }, { "key": "A101M3431", "value": "集装箱制造 - 行业数据" }, { "key": "A101M3432", "value": "金属压力容器制造 - 行业数据" }, { "key": "A101M3433", "value": "金属包装容器制造 - 行业数据" }, { "key": "A101M3440", "value": "金属丝绳及其制品的制造 - 行业数据" }, { "key": "A101M3451", "value": "建筑、家具用金属配件制造 - 行业数据" }, { "key": "A101M3452", "value": "建筑装饰及水暖管道零件制造 - 行业数据" }, { "key": "A101M3453", "value": "安全、消防用金属制品制造 - 行业数据" }, { "key": "A101M3459", "value": "其他建筑、安全用金属制品制造 - 行业数据" }, { "key": "A101M3460", "value": "金属表面处理及热处理加工 - 行业数据" }, { "key": "A101M3471", "value": "工业生产配套用搪瓷制品制造 - 行业数据" }, { "key": "A101M3472", "value": "搪瓷卫生洁具制造 - 行业数据" }, { "key": "A101M3479", "value": "搪瓷日用品及其他搪瓷制品制造 - 行业数据" }, { "key": "A101M3481", "value": "金属制厨房调理及卫生器具制造 - 行业数据" }, { "key": "A101M3482", "value": "金属制厨用器皿及餐具制造 - 行业数据" }, { "key": "A101M3489", "value": "其他日用金属制品制造 - 行业数据" }, { "key": "A101M3491", "value": "铸币及贵金属制实验室用品制造 - 行业数据" }, { "key": "A101M3499", "value": "其他未列明的金属制品制造 - 行业数据" }, { "key": "A101M3511", "value": "锅炉及辅助设备制造 - 行业数据" }, { "key": "A101M3512", "value": "内燃机及配件制造 - 行业数据" }, { "key": "A101M3513", "value": "汽轮机及辅机制造 - 行业数据" }, { "key": "A101M3514", "value": "水轮机及辅机制造 - 行业数据" }, { "key": "A101M3519", "value": "其他原动机制造 - 行业数据" }, { "key": "A101M3521", "value": "金属切削机床制造 - 行业数据" }, { "key": "A101M3522", "value": "金属成形机床制造 - 行业数据" }, { "key": "A101M3523", "value": "铸造机械制造 - 行业数据" }, { "key": "A101M3524", "value": "金属切割及焊接设备制造 - 行业数据" }, { "key": "A101M3525", "value": "机床附件制造 - 行业数据" }, { "key": "A101M3529", "value": "其他金属加工机械制造 - 行业数据" }, { "key": "A101M3530", "value": "起重运输设备制造 - 行业数据" }, { "key": "A101M3541", "value": "泵及真空设备制造 - 行业数据" }, { "key": "A101M3542", "value": "气体压缩机械制造 - 行业数据" }, { "key": "A101M3543", "value": "阀门和旋塞的制造 - 行业数据" }, { "key": "A101M3544", "value": "液压和气压动力机械及元件制造 - 行业数据" }, { "key": "A101M3551", "value": "轴承制造 - 行业数据" }, { "key": "A101M3552", "value": "齿轮、传动和驱动部件制造 - 行业数据" }, { "key": "A101M3560", "value": "烘炉、熔炉及电炉制造 - 行业数据" }, { "key": "A101M3571", "value": "风机、风扇制造 - 行业数据" }, { "key": "A101M3572", "value": "气体、液体分离及纯净设备制造 - 行业数据" }, { "key": "A101M3573", "value": "制冷、空调设备制造 - 行业数据" }, { "key": "A101M3574", "value": "风动和电动工具制造 - 行业数据" }, { "key": "A101M3575", "value": "喷枪及类似器具制造 - 行业数据" }, { "key": "A101M3576", "value": "包装专用设备制造 - 行业数据" }, { "key": "A101M3577", "value": "衡器制造 - 行业数据" }, { "key": "A101M3579", "value": "其他通用设备制造 - 行业数据" }, { "key": "A101M3581", "value": "金属密封件制造 - 行业数据" }, { "key": "A101M3582", "value": "紧固件、弹簧制造 - 行业数据" }, { "key": "A101M3583", "value": "机械零部件加工及设备修理 - 行业数据" }, { "key": "A101M3589", "value": "其他通用零部件制造 - 行业数据" }, { "key": "A101M3591", "value": "钢铁铸件制造 - 行业数据" }, { "key": "A101M3592", "value": "锻件及粉末冶金制品制造 - 行业数据" }, { "key": "A101M3611", "value": "采矿、采石设备制造 - 行业数据" }, { "key": "A101M3612", "value": "石油钻采专用设备制造 - 行业数据" }, { "key": "A101M3613", "value": "建筑工程用机械制造 - 行业数据" }, { "key": "A101M3614", "value": "建筑材料生产专用机械制造 - 行业数据" }, { "key": "A101M3615", "value": "冶金专用设备制造 - 行业数据" }, { "key": "A101M3621", "value": "炼油、化工生产专用设备制造 - 行业数据" }, { "key": "A101M3622", "value": "橡胶加工专用设备制造 - 行业数据" }, { "key": "A101M3623", "value": "塑料加工专用设备制造 - 行业数据" }, { "key": "A101M3624", "value": "木材加工机械制造 - 行业数据" }, { "key": "A101M3625", "value": "模具制造 - 行业数据" }, { "key": "A101M3629", "value": "其他非金属加工专用设备制造 - 行业数据" }, { "key": "A101M3631", "value": "食品、饮料、烟草工业专用设备制 - 行业数据" }, { "key": "A101M3632", "value": "农副食品加工专用设备制造 - 行业数据" }, { "key": "A101M3633", "value": "饲料生产专用设备制造 - 行业数据" }, { "key": "A101M3641", "value": "制浆和造纸专用设备制造 - 行业数据" }, { "key": "A101M3642", "value": "印刷专用设备制造 - 行业数据" }, { "key": "A101M3643", "value": "日用化工专用设备制造 - 行业数据" }, { "key": "A101M3644", "value": "制药专用设备制造 - 行业数据" }, { "key": "A101M3645", "value": "照明器具生产专用设备制造 - 行业数据" }, { "key": "A101M3646", "value": "玻璃、陶瓷和搪瓷制品生产专用设 - 行业数据" }, { "key": "A101M3649", "value": "其他日用品生产专用设备制造 - 行业数据" }, { "key": "A101M3651", "value": "纺织专用设备制造 - 行业数据" }, { "key": "A101M3652", "value": "皮革、毛皮及其制品加工专用设备 - 行业数据" }, { "key": "A101M3653", "value": "缝纫机械制造 - 行业数据" }, { "key": "A101M3659", "value": "其他服装加工专用设备制造 - 行业数据" }, { "key": "A101M3661", "value": "电工机械专用设备制造 - 行业数据" }, { "key": "A101M3662", "value": "电子工业专用设备制造 - 行业数据" }, { "key": "A101M3671", "value": "拖拉机制造 - 行业数据" }, { "key": "A101M3672", "value": "机械化农业及园艺机具制造 - 行业数据" }, { "key": "A101M3673", "value": "营林及木竹采伐机械制造 - 行业数据" }, { "key": "A101M3674", "value": "畜牧机械制造 - 行业数据" }, { "key": "A101M3675", "value": "渔业机械制造 - 行业数据" }, { "key": "A101M3676", "value": "农林牧渔机械配件制造 - 行业数据" }, { "key": "A101M3679", "value": "其他农林牧渔业机械制造及机械修 - 行业数据" }, { "key": "A101M3681", "value": "医疗诊断、监护及治疗设备制造 - 行业数据" }, { "key": "A101M3682", "value": "口腔科用设备及器具制造 - 行业数据" }, { "key": "A101M3683", "value": "实验室及医用消毒设备和器具的制 - 行业数据" }, { "key": "A101M3684", "value": "医疗、外科及兽医用器械制造 - 行业数据" }, { "key": "A101M3685", "value": "机械治疗及病房护理设备制造 - 行业数据" }, { "key": "A101M3686", "value": "假肢、人工器官及植（介）入器械 - 行业数据" }, { "key": "A101M3689", "value": "其他医疗设备及器械制造 - 行业数据" }, { "key": "A101M3691", "value": "环境污染防治专用设备制造 - 行业数据" }, { "key": "A101M3692", "value": "地质勘查专用设备制造 - 行业数据" }, { "key": "A101M3693", "value": "邮政专用机械及器材制造 - 行业数据" }, { "key": "A101M3694", "value": "商业、饮食、服务业专用设备制造 - 行业数据" }, { "key": "A101M3695", "value": "社会公共安全设备及器材制造 - 行业数据" }, { "key": "A101M3696", "value": "交通安全及管制专用设备制造 - 行业数据" }, { "key": "A101M3697", "value": "水资源专用机械制造 - 行业数据" }, { "key": "A101M3699", "value": "其他专用设备制造 - 行业数据" }, { "key": "A101M3711", "value": "铁路机车车辆及动车组制造 - 行业数据" }, { "key": "A101M3712", "value": "工矿有轨专用车辆制造 - 行业数据" }, { "key": "A101M3713", "value": "铁路机车车辆配件制造 - 行业数据" }, { "key": "A101M3714", "value": "铁路专用设备及器材、配件制造 - 行业数据" }, { "key": "A101M3719", "value": "其他铁路设备制造及设备修理 - 行业数据" }, { "key": "A101M3721", "value": "汽车整车制造 - 行业数据" }, { "key": "A101M3722", "value": "改装汽车制造 - 行业数据" }, { "key": "A101M3723", "value": "电车制造 - 行业数据" }, { "key": "A101M3724", "value": "汽车车身、挂车的制造 - 行业数据" }, { "key": "A101M3725", "value": "汽车零部件及配件制造 - 行业数据" }, { "key": "A101M3726", "value": "汽车修理 - 行业数据" }, { "key": "A101M3731", "value": "摩托车整车制造 - 行业数据" }, { "key": "A101M3732", "value": "摩托车零部件及配件制造 - 行业数据" }, { "key": "A101M3741", "value": "脚踏自行车及残疾人座车制造 - 行业数据" }, { "key": "A101M3742", "value": "助动自行车制造 - 行业数据" }, { "key": "A101M3751", "value": "金属船舶制造 - 行业数据" }, { "key": "A101M3752", "value": "非金属船舶制造 - 行业数据" }, { "key": "A101M3753", "value": "娱乐船和运动船的建造和修理 - 行业数据" }, { "key": "A101M3754", "value": "船用配套设备制造 - 行业数据" }, { "key": "A101M3755", "value": "船舶修理及拆船 - 行业数据" }, { "key": "A101M3759", "value": "航标器材及其他浮动装置的制造 - 行业数据" }, { "key": "A101M3761", "value": "飞机制造及修理 - 行业数据" }, { "key": "A101M3762", "value": "航天器制造 - 行业数据" }, { "key": "A101M3769", "value": "其他飞行器制造 - 行业数据" }, { "key": "A101M3791", "value": "潜水及水下救捞装备制造 - 行业数据" }, { "key": "A101M3792", "value": "交通管理用金属标志及设施制造 - 行业数据" }, { "key": "A101M3799", "value": "其他交通运输设备制造 - 行业数据" }, { "key": "A101M3911", "value": "发电机及发电机组制造 - 行业数据" }, { "key": "A101M3912", "value": "电动机制造 - 行业数据" }, { "key": "A101M3919", "value": "微电机及其他电机制造 - 行业数据" }, { "key": "A101M3921", "value": "变压器、整流器和电感器制造 - 行业数据" }, { "key": "A101M3922", "value": "电容器及其配套设备制造 - 行业数据" }, { "key": "A101M3923", "value": "配电开关控制设备制造 - 行业数据" }, { "key": "A101M3924", "value": "电力电子元器件制造 - 行业数据" }, { "key": "A101M3929", "value": "其他输配电及控制设备制造 - 行业数据" }, { "key": "A101M3931", "value": "电线电缆制造 - 行业数据" }, { "key": "A101M3932", "value": "光纤、光缆制造 - 行业数据" }, { "key": "A101M3933", "value": "绝缘制品制造 - 行业数据" }, { "key": "A101M3939", "value": "其他电工器材制造 - 行业数据" }, { "key": "A101M3940", "value": "电池制造 - 行业数据" }, { "key": "A101M3951", "value": "家用制冷电器具制造 - 行业数据" }, { "key": "A101M3952", "value": "家用空气调节器制造 - 行业数据" }, { "key": "A101M3953", "value": "家用通风电器具制造 - 行业数据" }, { "key": "A101M3954", "value": "家用厨房电器具制造 - 行业数据" }, { "key": "A101M3955", "value": "家用清洁卫生电器具制造 - 行业数据" }, { "key": "A101M3956", "value": "家用美容、保健电器具制造 - 行业数据" }, { "key": "A101M3957", "value": "家用电力器具专用配件制造 - 行业数据" }, { "key": "A101M3959", "value": "其他家用电力器具制造 - 行业数据" }, { "key": "A101M3961", "value": "燃气、太阳能及类似能源的器具制 - 行业数据" }, { "key": "A101M3969", "value": "其他非电力家用器具制造 - 行业数据" }, { "key": "A101M3971", "value": "电光源制造 - 行业数据" }, { "key": "A101M3972", "value": "照明灯具制造 - 行业数据" }, { "key": "A101M3979", "value": "灯用电器附件及其他照明器具制造 - 行业数据" }, { "key": "A101M3991", "value": "车辆专用照明及电气信号设备装置 - 行业数据" }, { "key": "A101M3999", "value": "其他未列明的电气机械制造 - 行业数据" }, { "key": "A101M4011", "value": "通信传输设备制造 - 行业数据" }, { "key": "A101M4012", "value": "通信交换设备制造 - 行业数据" }, { "key": "A101M4013", "value": "通信终端设备制造 - 行业数据" }, { "key": "A101M4014", "value": "移动通信及终端设备制造 - 行业数据" }, { "key": "A101M4019", "value": "其他通信设备制造 - 行业数据" }, { "key": "A101M4031", "value": "广播电视节目制作及发射设备制造 - 行业数据" }, { "key": "A101M4032", "value": "广播电视接收设备及器材制造 - 行业数据" }, { "key": "A101M4039", "value": "应用电视设备及其他广播电视设备 - 行业数据" }, { "key": "A101M4041", "value": "电子计算机整机制造 - 行业数据" }, { "key": "A101M4042", "value": "计算机网络设备制造 - 行业数据" }, { "key": "A101M4043", "value": "电子计算机外部设备制造 - 行业数据" }, { "key": "A101M4051", "value": "电子真空器件制造 - 行业数据" }, { "key": "A101M4052", "value": "半导体分立器件制造 - 行业数据" }, { "key": "A101M4053", "value": "集成电路制造 - 行业数据" }, { "key": "A101M4059", "value": "光电子器件及其他电子器件制造 - 行业数据" }, { "key": "A101M4061", "value": "电子元件及组件制造 - 行业数据" }, { "key": "A101M4061", "value": "电子元件及组件制造 - 行业数据" }, { "key": "A101M4062", "value": "印制电路板制造 - 行业数据" }, { "key": "A101M4071", "value": "家用影视设备制造 - 行业数据" }, { "key": "A101M4072", "value": "家用音响设备制造 - 行业数据" }, { "key": "A101M4090", "value": "其他电子设备制造 - 行业数据" }, { "key": "A101M4111", "value": "工业自动控制系统装置制造 - 行业数据" }, { "key": "A101M4112", "value": "电工仪器仪表制造 - 行业数据" }, { "key": "A101M4113", "value": "绘图、计算及测量仪器制造 - 行业数据" }, { "key": "A101M4114", "value": "实验分析仪器制造 - 行业数据" }, { "key": "A101M4115", "value": "试验机制造 - 行业数据" }, { "key": "A101M4119", "value": "供应用仪表及其他通用仪器制造 - 行业数据" }, { "key": "A101M4121", "value": "环境监测专用仪器仪表制造 - 行业数据" }, { "key": "A101M4122", "value": "汽车及其他用计数仪表制造 - 行业数据" }, { "key": "A101M4124", "value": "农林牧渔专用仪器仪表制造 - 行业数据" }, { "key": "A101M4125", "value": "地质勘探和地震专用仪器制造 - 行业数据" }, { "key": "A101M4126", "value": "教学专用仪器制造 - 行业数据" }, { "key": "A101M4128", "value": "电子测量仪器制造 - 行业数据" }, { "key": "A101M4129", "value": "其他专用仪器制造 - 行业数据" }, { "key": "A101M4130", "value": "钟表与计时仪器制造 - 行业数据" }, { "key": "A101M4141", "value": "光学仪器制造 - 行业数据" }, { "key": "A101M4142", "value": "眼镜制造 - 行业数据" }, { "key": "A101M4151", "value": "电影机械制造 - 行业数据" }, { "key": "A101M4152", "value": "幻灯及投影设备制造 - 行业数据" }, { "key": "A101M4153", "value": "照相机及器材制造 - 行业数据" }, { "key": "A101M4154", "value": "复印和胶印设备制造 - 行业数据" }, { "key": "A101M4155", "value": "计算器及货币专用设备制造 - 行业数据" }, { "key": "A101M4159", "value": "其他文化、办公用机械制造 - 行业数据" }, { "key": "A101M4190", "value": "其他仪器仪表的制造及修理 - 行业数据" }, { "key": "A101M4211", "value": "雕塑工艺品制造 - 行业数据" }, { "key": "A101M4212", "value": "金属工艺品制造 - 行业数据" }, { "key": "A101M4213", "value": "漆器工艺品制造 - 行业数据" }, { "key": "A101M4214", "value": "花画工艺品制造 - 行业数据" }, { "key": "A101M4215", "value": "天然植物纤维编织工艺品制造 - 行业数据" }, { "key": "A101M4216", "value": "抽纱刺绣工艺品制造 - 行业数据" }, { "key": "A101M4217", "value": "地毯、挂毯制造 - 行业数据" }, { "key": "A101M4218", "value": "珠宝首饰及有关物品的制造 - 行业数据" }, { "key": "A101M4219", "value": "其他工艺美术品制造 - 行业数据" }, { "key": "A101M4221", "value": "制镜及类似品加工 - 行业数据" }, { "key": "A101M4222", "value": "鬃毛加工、制刷及清扫工具的制造 - 行业数据" }, { "key": "A101M4229", "value": "其他日用杂品制造 - 行业数据" }, { "key": "A101M4230", "value": "煤制品制造 - 行业数据" }, { "key": "A101M4240", "value": "核辐射加工 - 行业数据" }, { "key": "A101M4290", "value": "其他未列明的制造业 - 行业数据" }, { "key": "A101M4310", "value": "金属废料和碎屑的加工处理 - 行业数据" }, { "key": "A101M4320", "value": "非金属废料和碎屑的加工处理 - 行业数据" }, { "key": "A101M4411", "value": "火力发电 - 行业数据" }, { "key": "A101M4412", "value": "水力发电 - 行业数据" }, { "key": "A101M4413", "value": "核力发电 - 行业数据" }, { "key": "A101M4419", "value": "其他能源发电 - 行业数据" }, { "key": "A101M4420", "value": "电力供应 - 行业数据" }, { "key": "A101M4430", "value": "热力生产和供应 - 行业数据" }, { "key": "A101M4500", "value": "燃气生产和供应业 - 行业数据" }, { "key": "A101M4610", "value": "自来水的生产和供应 - 行业数据" }, { "key": "A101M4620", "value": "污水处理及其再生利用 - 行业数据" }, { "key": "A101M4690", "value": "其他水的处理、利用与分配 - 行业数据" }
        ];