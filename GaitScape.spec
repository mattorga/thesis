# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Read Pose2Sim path from the temporary file
from PyInstaller.utils.hooks import collect_all


pose2sim_path = None
try:
    with open("pose2sim_path.txt", "r") as f:
        pose2sim_path = f.read().strip()
    print(f"Using Pose2Sim path from file: {pose2sim_path}")
except FileNotFoundError:
    import Pose2Sim
    pose2sim_path = os.path.dirname(Pose2Sim.__file__)
    print(f"Pose2Sim path file not found, using imported path: {pose2sim_path}")

# Add data files that need to be included
data_files = [
    ('blender_viz_orig', 'blender_viz_orig'),
    ('misc', 'misc'),
    ('utils', 'utils'),
    ('web', 'web'),
    ('resources', 'resources'),
    ('resources/icons', 'resources/icons'),
    ('resources/fonts/poppins', 'resources/fonts/poppins'),
    ('analyticsParams.py', '.'),
    ('analyticsParams.ui', '.'),
    ('comparative_params_manager.py', '.'),
    ('comparativeParams.py', '.'),
    ('comparativeParams.ui', '.'),
    ('params_manager.py', '.'),
    ('patient_form.py', '.'),
    ('trial_form.py', '.'),
    ('trial_form.ui', '.'),
    ('camera_manager.py', '.'),
    ('directory_manager.py', '.'),
    ('table_manager.py', '.'),
    ('data_manager.py', '.'),
    ('process_manager.py', '.'),
    ('chart_manager.py', '.'),
    ('viewer_manager.py', '.'),
    ('poseConfiguration.py', '.'),
    ('poseConfiguration.ui', '.'),
    ('styles.qss', '.'),
    ('resources.qrc', '.'),
    ('resources_rc.py', '.'),
    ('final_widget.py', '.'),
    ('final_widget.ui', '.'),
    ('final_orig.ui', '.'),
]

# Add Pose2Sim directory to data_files
data_files.append((pose2sim_path, 'Pose2Sim'))

# Add hidden imports that might be needed
hidden_imports = [
    # PyQt5 components
    'PyQt5',
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'PyQt5.QtWidgets',
    'PyQt5.QtChart',
    'PyQt5.QtWebEngineWidgets',
    'PyQt5.QtWebChannel',
    'PyQt5.QtWebEngineCore',  # Important for web engine
    
    # Standard library and common imports
    'os',
    'sys',
    'pathlib',
    'datetime',
    're',
    'zipfile',
    'argparse',
    'threading',
    'http.server',
    'socketserver',
    'configparser',
    'signal',
    'glob',
    'json',
    'time',
    'types',
    
    # Data processing libraries
    'numpy',
    'pandas',
    'csv',
    'toml',
    
    # Scientific computing
    'scipy',
    'scipy.signal',
    'scipy.stats',
    'scipy.spatial',
    'scipy.spatial.distance',
    'fastdtw',
    
    # Computer vision
    'cv2',
    'matplotlib',
    'matplotlib.pyplot',
    
    # Your custom modules
    'Pose2Sim',
    'Pose2Sim.Utilities',
    'Pose2Sim.Utilities.bodykin_from_mot_osim',
    'params_manager',
    'camera_manager',
    'directory_manager',
    'table_manager',
    'data_manager',
    'process_manager',
    'chart_manager',
    'viewer_manager',
    'comparative_params_manager',
    'patient_form',
    'trial_form',
    'final',
    'poseConfiguration',
    'comparativeParams',
    
    # Your utility modules and submodules
    'utils',
    'utils.gait_classification',
    'utils.statistics',
    'utils.statistics.Calc_ST_params',
    'utils.statistics.Angles_Analysis',
    'utils.statistics.paired_t_test_gait',
]

from PyInstaller.utils.hooks import collect_data_files

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=data_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

import os
from PyQt5.QtCore import QLibraryInfo

# Get the plugins directory from PyQt5
qt_plugins_dir = QLibraryInfo.location(QLibraryInfo.PluginsPath)

# Add each plugin subdirectory
for plugin_type in ['platforms', 'imageformats', 'styles', 'iconengines', 'webengine']:
    plugin_dir = os.path.join(qt_plugins_dir, plugin_type)
    if os.path.exists(plugin_dir):
        for file in os.listdir(plugin_dir):
            if file.endswith('.dll') or file.endswith('.so'):
                source = os.path.join(plugin_dir, file)
                target = os.path.join(plugin_type, file)
                a.datas.append((target, source, 'DATA'))

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GaitScape',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to True if you want a console window for debugging
)