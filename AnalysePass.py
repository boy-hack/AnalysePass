#!/usr/bin/env python
# coding=utf-8

"""
Descript your program
"""
import re
import json
import os
import sys
import collections
import argparse

reload(sys)
sys.setdefaultencoding('utf-8')


def load_apps(filename='apps.json.py'):
    filename = os.path.join(os.getcwd(), os.path.dirname(__file__), filename)
    return json.load(open(filename))
data = load_apps()
data["data"]["specialstr"]["parrten"] = r'[,./\\\+\-!@#$%^&*\(\)]+'
dict = sorted(data["data"].iteritems(),key=lambda d:d[1])
data["data"] = dict

def recontain(s,reg):
    return re.compile(reg,flags=re.IGNORECASE).search(s)

def get_categories(item):
    return data["categories"][str(item)]

def analypassword(s):
    n_data = list()
    error = 0
    while s!=" "*len(s):
        for item in data['data']:
            x_ = recontain(s,item[1]["parrten"])
            if x_:
                str_ = x_.group()
                ls_data = {}
                ls_data["index"] = s.find(str_)
                cid = item[1]["cat"]
                try:
		    if cid == 6:
                        if len(str_)==4:
                            if (int(str_[0:2])>=1 and int(str_[0:2])<=12) or (int(str_[2:4])<=32 and int(str_[2:4])>=1):
                                cid = 1
                    elif cid==1:
			if int(str_[-2:])>31:
                            cid = 6

		    ls_data["categories"] = get_categories(cid)
		except:
                    ls_data["categories"] = "无法识别"
                s = s.replace(str_," "*len(str_),1)
                n_data.append(ls_data)
                break
        error = error+1
        if error>20:
            ls_data["index"]="99"
            ls_data["categories"] = "无法识别"
            n_data.append(ls_data)
            break
    dict = sorted(n_data,key=lambda d:d["index"])
    str_return = list()
    for a in dict:
        str_return.append(a["categories"])
    return "+".join(str_return)
def filewrites(filename,content):
    f = open(filename,'a')
    f.write(content+'\n')
    f.close()
    
if __name__ == '__main__':
    # a = "zxc5201314abc"
    # print a
    # print analypassword(a)
	parser = argparse.ArgumentParser()
	parser.add_argument("-p", help=u"分析单个密码")
	parser.add_argument("-f", help="读入文件路径")
	parser.add_argument("-s","--split", help="读入文件分割符号")
	parser.add_argument("-sn","--split_num", type=int,help="取分割符号第几个用作密码分析")
	parser.add_argument("-c","--count", action="store_true",help="输出密码类型的数量")
	parser.add_argument("-d","--detail",action="store_true", help="输出每个密码的分析结果")
	parser.add_argument("-w","--write", help="写到文件")
	args = parser.parse_args()
	
	if args.p:
		print args.p
		print analypassword(args.p)
	
	if args.f:
		result = {}
		r_detail = {}
		f = open(args.f)
		for line in f:
			if args.split:
				content = line.split(args.split)[args.split_num]
			else:
				content = line
			content = content.strip()
			analyise = analypassword(content)
			if args.detail:
				r_detail[content] = analyise
			#print content,analypassword(content)
			if args.count:
				if analyise not in result:
					result[analyise] = 0
				result[analyise]+=1
		if args.count:		
			result = collections.OrderedDict(sorted(result.items(), key = lambda t: -t[1]))
			for key,value in result.items():
				print "%s--%s"%(key,value)
				if args.write:
                                    filewrites(args.write,"%s--%s"%(key,value))
		if args.detail:
			for key,value in r_detail.items():
				print "%s--%s"%(key,value)
				if args.write:
                                    filewrites(args.write,"%s--%s"%(key,value))
