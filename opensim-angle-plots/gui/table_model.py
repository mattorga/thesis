from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt5.QtGui import QColor

class CustomTableModel(QAbstractTableModel):
    def __init__(self, time, *args):
        QAbstractTableModel.__init__(self)
        self.load_data(time, *args)
    
    def load_data(self, time, *args):
        self.input_time = time
        self.input_data = args
        self.column_count = len(args) + 1
        self.row_count = len(self.input_time)

    def rowCount(self, parent=QModelIndex()):
        return self.row_count
    
    def columnCount(self, parent=QModelIndex()):
        return self.column_count
    
    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if section == 0:
                return "Time"
            else:
                joint_names = ["Hip R", "Hip L", "Knee R", "Knee L", "Ankle R", "Ankle L"]
                return joint_names[section - 1] if section <= len(joint_names) else f"Column {section}"
        else:
            return f"{section}"
    
    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            if column == 0:
                return f"{self.input_time[row]:.2f}"
            else:
                return f"{self.input_data[column - 1][row]:.2f}"
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight
        
        return None
    
    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable