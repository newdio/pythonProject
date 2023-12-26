#coding=utf8
import arcpy
import os
import sys

import ylpy
import string
def add_error(id, s=None):
    """ Return errors """

    arcpy.AddIDMessage("ERROR", id, s if s else None)
    if __name__ == '__main__':
        sys.exit(1)
    else:
        raise arcpy.ExecuteError, arcpy.GetIDMessage(id)

#获得一个字段类型
def getFieldType(TableName,FieldName):
    desc = arcpy.Describe(TableName)
    FieldName=FieldName.upper()
    for field in desc.fields:
        if field.Name.upper() ==FieldName:
            return field.type
            break
    return ""
def getFieldlen(TableName,FieldName):
    desc = arcpy.Describe(TableName)
    FieldName=FieldName.upper()
    for field in desc.fields:
        if field.Name.upper() ==FieldName:
            return field.length
            break
    return -1

def main():
    #arcpy.AddMessage("==================")
    wfiles = open(txtFile,'w')



    try:
        myField=FieldNames.replace(";",",")
        wfiles.write(myField+"\n")

        num=len(fields)
        #arcpy.AddMessage("num===="+str(num))
        FieldTypeList=[] #字段类型列表
        for  field in fields:
            FieldType=getFieldType(inFeature,field)
            FieldTypeList.append(FieldType)


        # Loop through input records
        n=ylpy.getCount(inFeature)
        ylpy.initProgress(u"导出数据",n)
        mystr='' #字符串
        with arcpy.da.SearchCursor(inFeature, fields) as cursor:

            for row in cursor:
                ylpy.step()
                myValue=""
                for  i in range(0,num):
                    value=row[i]
                    if FieldTypeList[i]=="String":
                        if value==None:
                            value=mystr+mystr
                        else:
                            value=mystr+value+mystr
                        myValue=myValue+value
                    else:
                        if value==None:
                            myValue=myValue
                        else:
                            myValue=myValue+str(value)
                    if i<num-1:
                        myValue=myValue+","
                wfiles.write(myValue+"\n")



    finally:
        wfiles.close()
        ylpy.freeProgress()
    #arcpy.AddMessage("aaaaaaaaaaaaaa")
inFeature = arcpy.GetParameterAsText(0) #
FieldNames=arcpy.GetParameterAsText(1)
txtFile=arcpy.GetParameterAsText(2) #是字符串的，一定要写成字符串

fields=string.split(FieldNames,";")
##if os.path.exists(outxls):
##    if arcpy.env.overwriteOutput == False:
##        add_error(258, outxls)
##    else:
##        os.remove(outxls)
num=ylpy.getCount(inFeature)
#arcpy.AddMessage(str(num))
##if  num> 65535:
##        # Input table exceeds the 256 columns limit of the .xls file format.
##        add_error(1531)
##elif len(fields) > 255:
##        # Input table exceeds the 65535 rows limit of the .xls file format.
##        add_error(1530)

try:
    main()
    #arcpy.SetParameterAsText(3, inFeature)  # Is polygon
except Exception, ErrorDesc:
    arcpy.AddError(u"错误："+str(ErrorDesc))

