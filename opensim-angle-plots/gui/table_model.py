from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt5.QtGui import QColor

class CustomTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        QAbstractTableModel.__init__(self)
        self.load_data(data)
    
    def load_data(self, data):
        self.input_time = data[0].values
        self.input_joint_r = data[1].values
        self.input_joint_l = data[2].values

        self.column_count = 3
        self.row_count = len(self.input_time)

    # What does QModelIndex do?
    def rowCount(self, parent=QModelIndex()):
        return self.row_count
    
    def columnCount(self, parent=QModelIndex()):
        return self.column_count
    
    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return ("Time", "Joint 1", "Joint 2")[section]
        else:
            return f"{section}"
    
    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            if column == 0:
                time = self.input_time[row]
                return str(time)
            elif column == 1:
                joint_angle_r = self.input_joint_r[row]
                return f"{joint_angle_r:.2f}"
            elif column == 2:
                joint_angle_l = self.input_joint_l[row]
                return f"{joint_angle_l:.2f}"
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight
        
        return None