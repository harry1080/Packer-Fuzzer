# !/usr/bin/env python3
# -*- encoding: utf-8 -*-

import execjs,os,re,sqlite3
from lib.common import readConfig
from lib.Database import DatabaseType
from lib.common.CreatLog import creatLog


class InfoTest():
    
    def __init__(self, projectTag):
        self.projectTag = projectTag
        self.info_Test = readConfig.ReadConfig().getValue('infoTest', 'info')[0]
        self.log = creatLog().get_logger()

    def startInfoTest(self):
        projectPath = DatabaseType(self.projectTag).getPathfromDB()
        for parent, dirnames, filenames in os.walk(projectPath, followlinks=True):
            for filename in filenames:
                if filename != self.projectTag + ".db":
                    filePath = os.path.join(parent, filename)
                    with open(filePath, "r", encoding="utf-8") as jsPath:
                        js_str = jsPath.read()
                        for infoTest in self.info_Test.split(","):
                            info_re = infoTest.split("§§§")[0]
                            infoTest_re = info_re + r"\:\s?\"(.*?)\""
                            info_strs = re.findall(infoTest_re,js_str)
                            location_info = re.search(infoTest_re, js_str)
                            infoRe = infoTest.split("§§§")[0]
                            infoTestRe = infoRe + r"\:\s?\"(.*?)\""
                            infoLast = infoTest.split("§§§")[1]
                            infoStr = re.findall(infoTestRe, js_str)
                            locationInfo = re.search(infoTestRe, js_str)
                            if locationInfo != None:
                                startInfo = locationInfo.span()[0]
                                startInfoEnd = js_str[startInfo - 77:startInfo + 77].replace("\'", "\"")
                                projectDBPath = DatabaseType(self.projectTag).getPathfromDB() + self.projectTag + ".db"
                                connect = sqlite3.connect(os.sep.join(projectDBPath.split('/')))
                                cursor = connect.cursor()
                                connect.isolation_level = None
                                if infoStr[0]:
                                    try:
                                        jsId = DatabaseType(self.projectTag).getJsIDFromDB(filename, projectPath)
                                        sql = "insert into vuln(api_id,js_id,response_b,response_h,sure,type,des) values ('" + str(
                                            7777777) + "','" + str(jsId) + "','" + str(infoStr[0]) + "','" + str(
                                            startInfoEnd) + "','" + str(1) + "','" + "INFO" + "','" + str(infoLast) + "')"
                                        cursor.execute(sql)
                                        connect.close()
                                    except Exception as e:
                                        self.log.error("[Err] %s" % e)

                        jsPath.close()