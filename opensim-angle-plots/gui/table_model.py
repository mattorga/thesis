from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt5.QtGui import QColor

class CustomTableModel(QAbstractTableModel):
    def __init__(self, time, data_right, data_left, joint_name):
        QAbstractTableModel.__init__(self)
        self.load_data(time, data_right, data_left, joint_name)
    
    def load_data(self, time, data_right, data_left, joint_name):
        self.input_time = time
        self.input_data_right = data_right
        self.input_data_left = data_left
        self.joint_name = joint_name
        self.column_count = 3
        self.row_count = len(self.input_time)
        self.total_time = self.input_time.iloc[-1] - self.input_time.iloc[0]

    def rowCount(self, parent=QModelIndex()):
        return self.row_count
    
    def columnCount(self, parent=QModelIndex()):
        return self.column_count
    
    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            headers = ["GC(%)", f"{self.joint_name} R", f"{self.joint_name} L"]
            return headers[section]
        else:
            return f"{section}"
    
    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            if column == 0:
                percentage = (self.input_time.iloc[row] - self.input_time.iloc[0]) / self.total_time * 100
                return f"{percentage:.2f}"
            elif column == 1:
                return f"{self.input_data_right.iloc[row]:.2f}"
            elif column == 2:
                return f"{self.input_data_left.iloc[row]:.2f}"
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight
        
        return None
    
    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable