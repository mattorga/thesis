from PyQt5 import QtWidgets, QtCore, Qt, QtGui

class TableManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.current_filter = "all"  # Track current filter state

    def display_data_in_table(self, table_widget, motion_data, scrollable=True, joint_filter="all"):
        """
        Displays the motion data in a QTableWidget with configurable display mode.

        Args:
            table_widget (QTableWidget): The table widget to populate
            motion_data (dict): Dictionary containing time and joint data
            scrollable (bool): If True, makes table scrollable. If False, fits to available space
            joint_filter (str): Filter for table columns ("all", "hip", "knee", "ankle")
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if motion_data is None or 'time' not in motion_data:
                return False
                
            time_data = motion_data['time']
            joint_data = motion_data['joint_data']

            # Store current filter
            self.current_filter = joint_filter
                
            # Clear the table
            table_widget.clear()
            table_widget.setRowCount(len(time_data))
            
            # Determine visible columns based on the joint filter
            if joint_filter == "hip":
                # Show only hip columns
                visible_columns = ['time', 'hip_flexion_r', 'hip_flexion_l']
                headers = ['Time', 'Hip R', 'Hip L']
            elif joint_filter == "knee":
                # Show only knee columns
                visible_columns = ['time', 'knee_angle_r', 'knee_angle_l']
                headers = ['Time', 'Knee R', 'Knee L']
            elif joint_filter == "ankle":
                # Show only ankle columns
                visible_columns = ['time', 'ankle_angle_r', 'ankle_angle_l']
                headers = ['Time', 'Ankle R', 'Ankle L']
            else:
                # Default to all columns
                visible_columns = ['time', 'hip_flexion_r', 'knee_angle_r', 'ankle_angle_r', 'hip_flexion_l', 'knee_angle_l', 'ankle_angle_l']
                headers = ['Time', 'Hip R', 'Knee R', 'Ankle R', 'Hip L', 'Knee L', 'Ankle L']
            
            # Set column count based on visible columns
            table_widget.setColumnCount(len(visible_columns))
            
            # Set headers
            table_widget.setHorizontalHeaderLabels(headers)
            
            # Mapping of column names to data
            column_data_map = {
                'time': time_data,
                'hip_flexion_r': joint_data['hip_flexion_r'],
                'hip_flexion_l': joint_data['hip_flexion_l'],
                'knee_angle_r': joint_data['knee_angle_r'],
                'knee_angle_l': joint_data['knee_angle_l'],
                'ankle_angle_r': joint_data['ankle_angle_r'],
                'ankle_angle_l': joint_data['ankle_angle_l']
            }
            
            # Populate data
            for row in range(len(time_data)):
                # Create items for visible columns
                for col, column_name in enumerate(visible_columns):
                    value = column_data_map[column_name][row]
                    
                    # Format value differently for time vs. angles
                    if column_name == 'time':
                        item = QtWidgets.QTableWidgetItem(f"{value:.3f}")
                    else:
                        item = QtWidgets.QTableWidgetItem(f"{value:.2f}")
                    
                    # Make item read-only
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                    table_widget.setItem(row, col, item)
        
            
            # Configure table display mode
            header = table_widget.horizontalHeader()
            
            if scrollable:
                # Enable scrolling
                table_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
                table_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
                
                # Set equal column widths for all columns
                table_width = table_widget.width() - 20  # Subtract scrollbar width
                col_width = table_width // table_widget.columnCount()
                
                # Set fixed column widths - make all columns equal width
                for col in range(table_widget.columnCount()):
                    table_widget.setColumnWidth(col, col_width)
                    
                # Allow vertical scrolling
                table_widget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
                
            else:
                # Disable scrollbars
                table_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                table_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                
                # Make columns stretch to fill available space evenly
                for col in range(table_widget.columnCount()):
                    header.setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)
                
                # Calculate and set visible rows based on table height
                row_height = table_widget.rowHeight(0)
                header_height = header.height()
                available_height = table_widget.height() - header_height
                visible_rows = available_height // row_height
                
                # Limit visible rows
                if visible_rows < len(time_data):
                    table_widget.setRowCount(visible_rows)
            
            return True
            
        except Exception as e:
            print(f"Error displaying data in table: {str(e)}")
            return False
        
    def highlight_row(self, table_widget, row_index):
        """
        Highlights a specific row in the table and removes highlighting from other rows,
        preserving original background colors.
        
        Args:
            table_widget (QTableWidget): The table widget to highlight a row in
            row_index (int): The index of the row to highlight
        """
        # Make sure the row index is valid
        if row_index < 0 or row_index >= table_widget.rowCount():
            return
            
        # Define highlight color
        highlight_color = QtGui.QColor(255, 255, 0, 100)  # Semi-transparent yellow
        
        # Store the original background colors if not stored already
        if not hasattr(table_widget, '_original_backgrounds'):
            table_widget._original_backgrounds = {}
            for row in range(table_widget.rowCount()):
                table_widget._original_backgrounds[row] = {}
                for col in range(table_widget.columnCount()):
                    item = table_widget.item(row, col)
                    if item:
                        table_widget._original_backgrounds[row][col] = item.background()
        
        # Reset all rows to their original colors first
        for row in range(table_widget.rowCount()):
            for col in range(table_widget.columnCount()):
                item = table_widget.item(row, col)
                if item and row in table_widget._original_backgrounds and col in table_widget._original_backgrounds[row]:
                    item.setBackground(table_widget._original_backgrounds[row][col])
        
        # Highlight the selected row
        for col in range(table_widget.columnCount()):
            item = table_widget.item(row_index, col)
            if item:
                item.setBackground(highlight_color)
                
        # Ensure the highlighted row is visible
        table_widget.scrollTo(table_widget.model().index(row_index, 0), 
                            QtWidgets.QAbstractItemView.PositionAtCenter)
        
    def reapply_table_highlighting(self, table_widget, row_index):
        """
        Ensures the specified row remains highlighted.
        Call this after any operation that might refresh the table.

        Args:
            table_widget (QTableWidget): The table widget to highlight a row in
            row_index (int): The index of the row to highlight
        """
        # Make sure the table exists and has data
        if table_widget and table_widget.rowCount() > 0:
            # Ensure the row index is valid
            valid_row = min(row_index, table_widget.rowCount() - 1)
            # Apply highlight
            self.highlight_row(table_widget, valid_row)
            
            # Ensure the highlighted row is visible in the viewport
            table_widget.scrollTo(table_widget.model().index(valid_row, 0), 
                                    QtWidgets.QAbstractItemView.PositionAtCenter)