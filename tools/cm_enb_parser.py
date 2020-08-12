import xml.etree.ElementTree as ET
import pandas as pd
# from jt_parser import jt_parser

class cm_enb_parser():
    def __init__(self, fileobj):

        # super().__init__(fileobj)
        self.TimeStamp = ''
        self.VendorName = ''
        self.CmVersion = ''
        self.header = list()
        self.value = list()
        self.values = list()
        self.rmUID = list()
        self.Dn = list()
        self.UserLabel = list()
        self.fileobj = fileobj

    def parse(self):
        df = pd.DataFrame()
        for event, elem in ET.iterparse(self.fileobj, events=('start', 'end')):
            if event == 'start':
                print(elem.tag)
                if elem.tag == 'TimeStamp':
                    self.TimeStamp = elem.text
                elif elem.tag == 'VendorName':
                    self.VendorName = elem.text
                elif elem.tag == 'CmVersion':
                    self.CmVersion = elem.text
                elif elem.tag == 'N':
                    self.header.append(elem.text)
                elif elem.tag == 'V':
                    self.value.append(elem.text)
                elif elem.tag == 'Object':
                    self.rmUID.append(elem.attrib['rmUID'])
                    self.Dn.append(elem.attrib['Dn'])
                    self.UserLabel.append(elem.attrib['UserLabel'])

            elif event == 'end':
                print(elem.tag)
                if elem.tag == 'Object':
                    self.values.append(self.value)
                    self.value = list()
                elif elem.tag == 'Objects':
                    df = pd.DataFrame(self.values)
                    df.columns = self.header
                    df['rmUID'] = self.rmUID
                    df['Dn'] = self.Dn
                    df['UserLabel'] = self.UserLabel
                    df['VendorName'] = self.VendorName
                    df['InfoModelReferenced'] = self.CmVersion
                    df['BeginTime'] = self.TimeStamp
                    # df = self.fill_value(df)
                    df.to_csv('./res.csv', index=False,)
                    print(df.head())
        return df


if __name__ == '__main__':
    path = 'e:/aaa.xml'
    p = cm_enb_parser(path)
    p.parse()
