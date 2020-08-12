import os
import re
from abc import abstractmethod

import pandas as pd
import yaml

from .base_parser import BaseParser

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class jt_parser(BaseParser):

    conf = yaml.safe_load(open(os.path.join(CURRENT_DIR, 'jt_parser.yml'), 'rt'))
    cm_mapping = conf['cm_mapping']
    pm_mapping = conf['pm_mapping']
    object_structs = conf['object_structs']


    @property
    def object_type(self) -> str:
        event = re.search(r'[PC]{1}M-ENB-.+?-', self.filename).group().split('-')[-2]
        if self.filename.startswith("PM-"):
            return self.pm_mapping[event]
        elif self.filename.startswith("CM-"):
            return self.cm_mapping[event]

    @property
    def object_struct(self) -> list:
        return self.object_structs[self.object_type]

    @abstractmethod
    def parse(self) -> pd.DataFrame:
        pass

    def qci_mapping(self, cols):
        qci_keys = [key for key in self.object_struct if key.find('_Qci') > 0]
        qci_dict = dict()
        for qci in qci_keys:
            prefix, suffix = qci.split('_Qci')
            exp = '^%s_[0-9]{1,2}%s$' % (prefix, suffix)
            pattern = re.compile(exp)
            qci_dict[qci] = [col for col in cols if pattern.match(col)]
        return qci_dict

    def mutilvalue_merge(self, qci_dict, df):
        for qci, values in qci_dict.items():
            ser = pd.Series()
            for value in values:
                if ser.empty:
                    ser = df[value]
                else:
                    ser = ser + ',' + df[value]
            df[qci] = ser
            df.drop(columns=values, inplace=True)
        return df

    def prb_mapping(self, cols):
        prb_keys = [key for key in self.object_struct if key.find("_PRB") > 0]
        prb_dict = dict()
        for prb in prb_keys:
            prefix = prb.split('_PRB')[0]
            exp = '^%s_PRB[0-9]{1,3}$' % prefix
            pattern = re.compile(exp)
            prb_dict[prb] = [col for col in cols if pattern.match(col)]
        return prb_dict

    def fill_value(self, df):
        dn_df_cols = ['DnPrefix'] + [ele.split('=')[0] for ele in df['Dn'][0].split(',')[1:]]
        dn_df = df['Dn'].str.split(',', expand=True).apply(
            lambda ser: (ser.str.split('=', expand=True))[1] if ser.str.contains('=', regex=False).all() else ser)
        df['SenderName'] = df['Dn'].str.split(',', 1, expand=True)[1]
        dn_df.columns = dn_df_cols
        duplicated_cols = set(dn_df.columns) & set(df.columns)
        for col in duplicated_cols:
            dn_df.drop(columns=col, inplace=True)
        df = pd.concat((df, dn_df), axis=1)
        df['OMC_ID'] = self.attrs['omc_id']
        df['ProvinceName'] = self.attrs['province']
        df['FileName'] = self.fileobj.filename
        return df

