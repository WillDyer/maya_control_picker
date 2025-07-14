<h1 align="center">Maya-Control-Picker aka MCP</h1>
<p align="center">
    <img src="https://img.shields.io/badge/Maya-37A5CC?style=for-the-badge&logo=autodeskmaya&logoColor=white">
    <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue">
    <img src="https://img.shields.io/badge/Qt-41CD52?style=for-the-badge&logo=Qt&logoColor=white">
</p>
<div align="center">
    <img src="images/MCP.png" alt="Project UI" width="700"/>
</div>

### Running The Tool

> [!WARNING]
> - This tool was developed as a summer project and will likely not be production ready.
> - Tool is designed to be ran through maya.

```python
from importlib import reload
import maya_control_picker
reload(maya_control_picker)

maya_control_picker.start_interface()
```

