
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import QSize
from time import sleep as sleep
import os
import pandas as pd
import numpy as np
from math import ceil
import matplotlib.pyplot as plt
import pyarrow as pa
import pyarrow.parquet as pq


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        QMainWindow.__init__(self)
        self.ui = loadUi('./ui/main/mainwindow.ui', self)

        self.filepath = './data'
        self.files = []
        # self.pb_loadmsrfiles.clicked.connect(self.load_msr_files)
        self.pb_exit.clicked.connect(self.close)
        self.pb_exit.setStyleSheet('color: red')
        self.pb_test.clicked.connect(self.file_list)
        self.pb_convert.clicked.connect(self.convert_msr)

        self.csv_list = []
        self.par_list = []
        self.mod_list = []
        self.file_list()

        self.head = ['cnt', 'ZDA_s', 'Lat_deg', 'Lon_deg', 'HDT_deg', 'COG_deg', 'SOG_kt', 'ROT_deg_min',
                     'VelocLin_gr_u_kt', 'VelocLin_gr_v_kt', 'VelocLin_tw_u_kt', 'VelocLin_tw_v_kt',
                     'AP_Drivemotor_Load1_perc', 'AP_RPM_Cmd1_perc', 'AP_RPM_Act1_perc', 'AP_Drivemotor_Load2_perc',
                     'AP_RPM_Cmd2_perc', 'AP_RPM_Act2_perc', 'CP_RPM_Cmd_perc', 'CP_RPM_Act_perc', 'CP_RPM_Act_1/min',
                     'CP_Pitch_Cmd_perc', 'CP_Pitch_Act_perc', 'AP_Azim_Cmd1_deg', 'AP_Azim__Act1_deg',
                     'AP_Azim_Cmd2_deg', 'AP_Azim__Act2_deg', 'CP_Rudder_Cmd', 'CP_Rudder_Act', 'BT_Cmd1_perc',
                     'BT_Act1_perc', 'BT_Cmd2_perc', 'BT_Act2_perc', 'Wind_Dir_Abs_deg', 'Wind_Val_Abs_kt',
                     'Wind_Dir_Rel_deg', 'Wind_Val_Rel_kt', 'DPT_m', 'StMnEng_hm1_sbI', 'StMnEng_hm2_psI',
                     'StMnEng_hm3_sbII', 'StMnEng_hm4_psII', 'StRudPump1', 'StRudPump2', 'StRudPump3', 'StRudPump4',
                     'EngineMode', 'burdlim_ps', 'burdlim_sb', 'ID_VBW', 'ID_ZDA', 'ID_VTG', 'AP_prt_Backup_On',
                     'AP_prt_Thruster_Running', 'AP_prt_Tandem_Stbd', 'AP_prt_Tandem_Port', 'AP_prt_Cruise_Mode',
                     'AP_prt_AP_in_Control', 'AP_prt_Rpm_Order_perc', 'AP_prt_Rpm_Feedback_perc',
                     'AP_prt_Rpm_Feedback_rpm', 'AP_prt_Direction_Order_deg', 'AP_prt_Direction_Feedback_deg',
                     'AP_prt_Main_Bridge_in_Cmd', 'AP_prt_Port_Wing_in_Cmd', 'AP_prt_Stbd_Wing_in_Cmd',
                     'AP_stb_Backup_On', 'AP_stb_Thruster_Running', 'AP_stb_Tandem_Stbd', 'AP_stb_Tandem_Port',
                     'AP_stb_Cruise_Mode', 'AP_stb_AP_in_Control', 'AP_stb_Rpm_Order_perc', 'AP_stb_Rpm_Feedback_perc',
                     'AP_stb_Rpm_Feedback_rpm', 'AP_stb_Direction_Order_deg', 'AP_stb_Direction_Feedback_deg',
                     'AP_stb_Main_Bridge_in_Cmd', 'AP_stb_Port_Wing_in_Cmd', 'AP_stb_Stbd_Wing_in_Cmd',
                     'CP_NC_Backup_On', 'CP_NC_Sailing_Pos', 'CP_NC_Speed_Pilot_in_Control', 'CP_NC_AP_in_Control',
                     'CP_NC_Clutch_1_Status', 'CP_NC_Clutch_2_Status', 'CP_NC_Clutch_3_Status',
                     'CP_NC_Pitch_Order_perc', 'CP_NC_Pitch_Feedback_perc', 'CP_NC_Rpm_Order_perc',
                     'CP_NC_Rpm_Feedback_perc', 'CP_NC_Rpm_Feedback_rpm', 'CP_NC_Rudder_Order_deg',
                     'CP_NC_Ruddr_Feedback_deg', 'CP_NC_Main_Bridge_in_Cmd', 'CP_NC_Port_Wing_in_Cmd',
                     'CP_NC_Stbd_Wing_in_Cmd', 'CP_NC_Auto_start_pump_1', 'CP_NC_Auto_start_pump_2',
                     'CP_NC_Pump_1_Run', 'CP_NC_Pump_2_Run', 'DDM_draught_FWD', 'DDM_draught_MID_PT',
                     'DDM_draught_MID_MID', 'DDM_draught_MID_SB', 'DDM_draught_AFT', 'Trim_m', 'Trim_deg',
                     'List_m', 'List_deg']
        self.drop = ['cnt', 'ZDA_s', 'Lat_deg', 'Lon_deg', 'HDT_deg', 'COG_deg', 'SOG_kt', 'ROT_deg_min',
                     'VelocLin_gr_u_kt', 'VelocLin_gr_v_kt', 'VelocLin_tw_u_kt', 'VelocLin_tw_v_kt',
                     'AP_Drivemotor_Load1_perc', 'AP_RPM_Cmd1_perc', 'AP_RPM_Act1_perc', 'AP_Drivemotor_Load2_perc',
                     'AP_RPM_Cmd2_perc', 'AP_RPM_Act2_perc', 'CP_RPM_Cmd_perc', 'CP_RPM_Act_perc', 'CP_RPM_Act_1/min',
                     'CP_Pitch_Cmd_perc', 'CP_Pitch_Act_perc', 'AP_Azim_Cmd1_deg', 'AP_Azim__Act1_deg',
                     'AP_Azim_Cmd2_deg', 'AP_Azim__Act2_deg', 'CP_Rudder_Cmd', 'CP_Rudder_Act', 'BT_Cmd1_perc',
                     'BT_Act1_perc', 'BT_Cmd2_perc', 'BT_Act2_perc', 'Wind_Dir_Abs_deg', 'Wind_Val_Abs_kt',
                     'Wind_Dir_Rel_deg', 'Wind_Val_Rel_kt', 'DPT_m', 'StMnEng_hm1_sbI', 'StMnEng_hm2_psI',
                     'StMnEng_hm3_sbII', 'StMnEng_hm4_psII', 'StRudPump1', 'StRudPump2', 'StRudPump3', 'StRudPump4',
                     'EngineMode', 'burdlim_ps', 'burdlim_sb', 'ID_VBW', 'ID_ZDA', 'ID_VTG', 'AP_prt_Backup_On',
                     'AP_prt_Thruster_Running', 'AP_prt_Tandem_Stbd', 'AP_prt_Tandem_Port', 'AP_prt_Cruise_Mode',
                     'AP_prt_AP_in_Control', 'AP_prt_Rpm_Order_perc', 'AP_prt_Rpm_Feedback_perc',
                     'AP_prt_Rpm_Feedback_rpm', 'AP_prt_Direction_Order_deg', 'AP_prt_Direction_Feedback_deg',
                     'AP_prt_Main_Bridge_in_Cmd', 'AP_prt_Port_Wing_in_Cmd', 'AP_prt_Stbd_Wing_in_Cmd',
                     'AP_stb_Backup_On', 'AP_stb_Thruster_Running', 'AP_stb_Tandem_Stbd', 'AP_stb_Tandem_Port',
                     'AP_stb_Cruise_Mode', 'AP_stb_AP_in_Control', 'AP_stb_Rpm_Order_perc', 'AP_stb_Rpm_Feedback_perc',
                     'AP_stb_Rpm_Feedback_rpm', 'AP_stb_Direction_Order_deg', 'AP_stb_Direction_Feedback_deg',
                     'AP_stb_Main_Bridge_in_Cmd', 'AP_stb_Port_Wing_in_Cmd', 'AP_stb_Stbd_Wing_in_Cmd',
                     'CP_NC_Backup_On', 'CP_NC_Sailing_Pos', 'CP_NC_Speed_Pilot_in_Control', 'CP_NC_AP_in_Control',
                     'CP_NC_Clutch_1_Status', 'CP_NC_Clutch_2_Status', 'CP_NC_Clutch_3_Status',
                     'CP_NC_Pitch_Order_perc', 'CP_NC_Pitch_Feedback_perc', 'CP_NC_Rpm_Order_perc',
                     'CP_NC_Rpm_Feedback_perc', 'CP_NC_Rpm_Feedback_rpm', 'CP_NC_Rudder_Order_deg',
                     'CP_NC_Ruddr_Feedback_deg', 'CP_NC_Main_Bridge_in_Cmd', 'CP_NC_Port_Wing_in_Cmd',
                     'CP_NC_Stbd_Wing_in_Cmd', 'CP_NC_Auto_start_pump_1', 'CP_NC_Auto_start_pump_2',
                     'CP_NC_Pump_1_Run', 'CP_NC_Pump_2_Run', 'DDM_draught_FWD', 'DDM_draught_MID_PT',
                     'DDM_draught_MID_MID', 'DDM_draught_MID_SB', 'DDM_draught_AFT', 'Trim_m', 'Trim_deg',
                     'List_m', 'List_deg']

    def convert_msr(self):
        '''
        :return: None

        konvertiert alle noch nicht umgewandelten txt-Dateien

        '''
        self.file_list()
        cnt = 0
        for name in self.csv_list:
            cnt += 1
            if (name[0:-3] + 'par') not in self.par_list:
                # load data
                data = pd.read_csv(os.path.join('./data', name), skiprows=2, sep='\t', decimal=',').astype('float32')
                table = pa.Table.from_pandas(data)
                pq.write_table(table, os.path.join('./data', name[0:-3] + 'par'))
                i = int(ceil((100/len(self.csv_list))*cnt))
                self.progressBar.setValue(i)
                QApplication.processEvents()
        self.file_list()

        # data = pd.read_parquet('./data/msr_180828_235959_180830_000000.par')
        # fig, axs = plt.subplots(2, 2)
        # axs[0, 0].plot(data['CP_NC_Backup_On'])
        # axs[0, 0].set_title('CP_NC_Backup_On')
        # axs[0, 1].plot(data['CP_NC_Sailing_Pos'])
        # axs[0, 1].set_title('CP_NC_Sailing_Pos')
        # axs[1, 0].plot(data['CP_NC_Speed_Pilot_in_Control'])
        # axs[1, 0].set_title('CP_NC_Speed_Pilot_in_Control')
        # axs[1, 1].plot(data['CP_NC_AP_in_Control'])
        # axs[1, 1].set_title('CP_NC_AP_in_Control')
        # plt.show()

    def load_msr_files(self):
        pass

    def file_list(self):
        while not os.path.isdir(self.filepath):
            self.filepath = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.files = os.listdir(self.filepath)
        self.csv_list = []
        self.par_list = []
        self.mod_list = []

        for file in self.files:
            if file[0:3] == 'msr' and file[-3:] == 'txt':
                self.csv_list.append(file)
            elif file[0:3] == 'msr' and file[-3:] == 'par':
                self.par_list.append(file)
            elif file[-5:] == '.hdf5':
                self.mod_list.append(file)

        self.lw_txt.clear()
        self.lw_par.clear()
        self.lw_mod.clear()
        self.lw_txt.addItems(self.csv_list)
        self.lw_par.addItems(self.par_list)
        self.lw_mod.addItems(self.mod_list)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
