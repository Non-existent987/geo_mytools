import xml.etree.ElementTree as ET
import pandas as pd

class my_xml_to_csv():
    def __init__(self,file_name):
        self.TimeStamp = ''
        self.VendorName = ''
        self.ElementType = ''
        self.ObjectType = ''
        self.CmVersion = ''
        self.value = list()
        self.values = list()
        self.file_name = file_name
        self.columns = list()
        self.rmUID = list()
        self.Dn = list()
        self.UserLabel = list()


    def go(self):

        for start_end , elem in ET.iterparse(self.file_name , events=('start','end')):

            if start_end == 'start':
                if elem.tag == 'N':
                    self.columns.append(elem.text)
                elif elem.tag == 'V':
                    self.value.append(elem.text)
                elif elem.tag == 'TimeStamp':
                    self.TimeStamp = elem.text
                elif elem.tag == 'VendorName':
                    self.VendorName = elem.text
                elif elem.tag == 'ElementType':
                    self.ElementType = elem.text
                elif elem.tag == 'CmVersion':
                    self.CmVersion = elem.text

                elif elem.tag == 'Object':
                    self.rmUID.append(elem.attrib['rmUID']) 
                    self.Dn.append(elem.attrib['Dn']) 
                    self.UserLabel.append(elem.attrib['UserLabel']) 


            elif start_end == 'end':
                if elem.tag == 'Object':
                    self.values.append(self.value)
                    self.value = list()
                elif elem.tag == 'Objects':
                    df = pd.DataFrame(self.values)
                    df.columns = self.columns
                    df['rmUID']=self.rmUID
                    df['Dn']=self.Dn
                    df['UserLabel']=self.UserLabel

                    df['TimeStamp']=self.TimeStamp
                    df['VendorName']=self.VendorName
                    df['ElementType']=self.ElementType
                    df['ObjectType']=self.ObjectType
                    df['CmVersion']=self.CmVersion
                  

                    df.to_csv('res2.csv',index=False)

if __name__ == '__main__':
    path = 'e:/aaa.xml'
    p = my_xml_to_csv(path)
    p.go()






