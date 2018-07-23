import os
import time
import pprint
import socket
import xml.etree.ElementTree as ET
from yattag import Doc
from yattag import indent
from src.resource.style import css
from src.Tools.IO.Output.ConfigWriter import write_options_dict_to_config
from src.Tools.IO.Input.ConfigReader import read_options_as_dict_from_config


class Report(object):

    meta_dic = {}
    result_root = None
    start_time_stamp = 0
    host = "localhost"

    def __init__(self, Krakken, path="Output/report.html"):
        
        self.start_time_stamp = time.time()
        if not os.path.isfile(path):
            with open(path, 'a'):
                pass 
        self.krakken = Krakken
        self.html_file = path
    
    def record_metadata(self, metadata_ini="Output/metadata.ini"):
        pass 

    def create_report(self, report_file="Output/report.html"):
        
        doc, tag, text = Doc().tagtext()
        doc.asis('<!DOCTYPE html>')
        from src.resource.style import css
        with tag('html'):
            with tag('head'):
                with tag('title'):
                    text("Automation Test Result")
                with tag('meta', charset="utf-8"):
                    pass 
                with tag('meta', name="viewport", content="width=device-width, initial-scale=1"):
                    pass 
                with tag('style'):
                    text(css)
            with tag('body'):
                with tag('div', klass='container'):
                    pass 
                with tag('div', klass='panel'): 
                    pass 
                with tag('div', klass='panel-footer'):
                    for meta in self.meta_dic:
                        with tag('p'):
                            with tag('b'):
                                text(meta + ": ")
                            if meta == "HOST":
                                with tag('a', href='https://'+self.meta_dic.get(meta)+"/"):
                                    text(self.krakken.master)
                            else:
                                text(str(self.meta_dic.get(meta)))
                with tag('div', klass="panel-body"):
                    with tag('table'):
                        with tag('tr'):
                            with tag('th'):
                                text("TEST #")
                            with tag('th'):
                                text("TEST NAME")
                            with tag('th'):
                                text("START TIME")
                            with tag('th'):
                                text("DURATION")
                            with tag('th'):
                                text("RESULT")
                            with tag('th'):
                                text("LOG")
                        root = self.result_root
                        cnt = 0
                        for result in root.iter('testcase'):
                            if result.find("failure") is not None:
                                res = "FAIL"
                                with open("Output/failure", "a+") as r: 
                                    r.write("failed\n")
                            elif result.find("skipped") is not None:
                                res = "SKIP"
                            else:
                                res = "PASS"
                            print result.attrib.get('name') + " -> " + res
                            properties = result.find('properties')
                            st_time = ""
                            for property in properties:
                                if property.attrib.get('name') == 'case_start_time':
                                    st_time = property.attrib.get('value')
                                    break
                            with tag('tr'):
                                with tag('td'):
                                    text("TC" + str(cnt))
                                with tag('td'):
                                    text(result.attrib.get('name'))
                                with tag('td'):
                                    if st_time:
                                        time_string = time.strftime('%H:%M:%S', time.localtime(float(st_time)))
                                    else:
                                        time_string = '-'
                                    text(time_string)
                                with tag('td'):
                                    try:
                                        t = float(result.attrib.get('time'))
                                        time_elapsed = ("{:0>2}h:".format(int(t//3600)) if int(t//3600) > 0 else "") + ("{:0>2}m:".format(int(t - 3600 * (t//3600))//60) if (t - 3600 * (t//3600))//60 > 0 or t//3600>0 else "") + "{:05.2f}s".format(t%60)
                                    except:
                                        time_elapsed = "-"
                                    text(time_elapsed)
                                with tag('td'):
                                    with tag('span', klass=res.lower(), style="font-family:'Monaco', monospace"):
                                        text(res)
                                with tag('td'):
                                    # misc = read_options_as_dict_from_config("misc.ini", "TEST")
                                    if "JOB_NAME" in self.meta_dic and "BUILD_URL" in self.meta_dic:
                                        BUILD_ID = filter(None, self.meta_dic.get('BUILD_URL').split("/"))[-1]
                                        with tag('a', klass=res.lower(), href="http://"+socket.gethostname()+"/jenkins/"+self.meta_dic.get("JOB_NAME")+"/"+BUILD_ID+"/Output/"+str(cnt)):
                                            with tag('span', style="font-family: monospace;"):
                                                text(">")
                                    else:
                                        with tag('a', klass=res.lower(), href="./"+str(cnt)+"/"):
                                            with tag('span', style="font-family: monospace;"):
                                                text(">")
                            cnt += 1
                with tag('div', klass="panel-footer"):
                    with tag('p'):
                        with tag('b'):
                            text('Total Processing Time: ')
                        end_time = time.time()
                        elapse = end_time - self.start_time_stamp
                        h, r = divmod(elapse, 3600)
                        m, s = divmod(r, 60)
                        text("{:0>2}h:{:0>2}m:{:05.2f}s".format(int(h), int(m), s))



        with open(report_file, 'w+') as f:
            f.write(indent(
                doc.getvalue(), 
                indentation="   ",
                newline="\r\n",
                indent_text=True))

    def finalized_report(self, start_time):
        
        pass

    def log_meta_data(self, request, metadata_ini="Output/metadata.ini"):
        self.meta_dic = request.config._metadata
        dic = {}
        write_options_dict_to_config(metadata_ini, "TEST", request.config._metadata)

    def record_results(self, report="Output/result.xml"):
        tree = ET.parse(report)
        root = tree.getroot()
        self.result_root = root 
        # print root.tag
        """print root.attrib
        for result in root.iter('testcase'):
            #pprint.pprint(result.find("failure"))
            print result.attrib.get('name') + " -> " + ("PASS" if result.find("failure") is None else "FAIL")
        """
