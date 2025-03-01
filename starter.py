import os
import sys
import argparse
from pathlib import Path
import json
import datetime

def create_directory(directory_path):
    """Create directory if it doesn't exist."""
    try:
        os.makedirs(directory_path, exist_ok=True)
        print(f"Created directory: {directory_path}")
    except Exception as e:
        print(f"Error creating directory {directory_path}: {e}")
        sys.exit(1)

def create_file(file_path, content=""):
    """Create a file with optional content."""
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"Created file: {file_path}")
    except Exception as e:
        print(f"Error creating file {file_path}: {e}")
        sys.exit(1)

def setup_rpa_structure(base_dir, project_name):
    """Create the RPA project structure."""
    # Create project base directory
    project_dir = os.path.join(base_dir, project_name)
    create_directory(project_dir)
    
    # Define structure
    structure = {
        "src": {
            "bots": {
                "main.py": "# Main entry point for the RPA bot\n\nfrom config import settings\nfrom modules import data_handler\nfrom utils import logger\n\ndef main():\n    logger.setup_logging()\n    logger.log_info('Starting RPA process')\n    # Your main bot logic here\n    \nif __name__ == '__main__':\n    main()\n"
            },
            "config": {
                "settings.py": "# Configuration settings for the RPA solution\n\n# Application paths\nAPP_PATHS = {\n    'input_folder': 'data/input',\n    'output_folder': 'data/output',\n    'temp_folder': 'data/temp',\n    'logs_folder': 'logs'\n}\n\n# Processing settings\nSETTINGS = {\n    'retry_attempts': 3,\n    'timeout_seconds': 30,\n    'debug_mode': True\n}\n"
            },
            "modules": {
                "data_handler.py": "# Module for handling data processing\n\ndef read_input_data(file_path):\n    \"\"\"Read and parse input data\"\"\"\n    # Implementation\n    pass\n\ndef process_data(data):\n    \"\"\"Process the data\"\"\"\n    # Implementation\n    pass\n\ndef export_results(data, output_path):\n    \"\"\"Export processed data to output\"\"\"\n    # Implementation\n    pass\n",
                "workflow.py": "# Module containing workflow steps\n\nclass Workflow:\n    def __init__(self):\n        self.status = 'initialized'\n        \n    def step1_data_extraction(self):\n        \"\"\"Extract data from source systems\"\"\"\n        # Implementation\n        self.status = 'data_extracted'\n        \n    def step2_data_transformation(self):\n        \"\"\"Transform the extracted data\"\"\"\n        # Implementation\n        self.status = 'data_transformed'\n        \n    def step3_data_loading(self):\n        \"\"\"Load data to target systems\"\"\"\n        # Implementation\n        self.status = 'data_loaded'\n        \n    def execute_workflow(self):\n        \"\"\"Execute the complete workflow\"\"\"\n        self.step1_data_extraction()\n        self.step2_data_transformation()\n        self.step3_data_loading()\n        return {'status': 'completed'}\n",
                "__init__.py": ""
            },
            "utils": {
                "excel_handler.py": "# Utility for Excel operations\n\ndef read_excel(file_path, sheet_name=None):\n    \"\"\"Read data from Excel file\"\"\"\n    # Implementation\n    pass\n\ndef write_excel(data, file_path, sheet_name=None):\n    \"\"\"Write data to Excel file\"\"\"\n    # Implementation\n    pass\n",
                "logger.py": "# Logging utility\n\nimport logging\nimport os\nfrom datetime import datetime\nfrom config import settings\n\ndef setup_logging():\n    \"\"\"Setup logging configuration\"\"\"\n    log_dir = settings.APP_PATHS['logs_folder']\n    os.makedirs(log_dir, exist_ok=True)\n    \n    log_file = os.path.join(log_dir, f\"rpa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log\")\n    \n    logging.basicConfig(\n        level=logging.DEBUG if settings.SETTINGS['debug_mode'] else logging.INFO,\n        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',\n        handlers=[\n            logging.FileHandler(log_file),\n            logging.StreamHandler()\n        ]\n    )\n\ndef log_info(message):\n    \"\"\"Log info message\"\"\"\n    logging.info(message)\n\ndef log_error(message):\n    \"\"\"Log error message\"\"\"\n    logging.error(message)\n\ndef log_debug(message):\n    \"\"\"Log debug message\"\"\"\n    logging.debug(message)\n",
                "ui_automation.py": "# UI automation helper\n\ndef find_element(selector, timeout=10):\n    \"\"\"Find UI element by selector\"\"\"\n    # Implementation\n    pass\n\ndef click_element(element):\n    \"\"\"Click UI element\"\"\"\n    # Implementation\n    pass\n\ndef type_text(element, text):\n    \"\"\"Type text into UI element\"\"\"\n    # Implementation\n    pass\n",
                "__init__.py": ""
            },
            "__init__.py": ""
        },
        "data": {
            "input": {
                ".gitkeep": ""
            },
            "output": {
                ".gitkeep": ""
            },
            "temp": {
                ".gitkeep": ""
            }
        },
        "logs": {
            ".gitkeep": ""
        },
        "tests": {
            "test_data_handler.py": "# Tests for data_handler module\n\nimport unittest\nfrom src.modules import data_handler\n\nclass TestDataHandler(unittest.TestCase):\n    def test_read_input_data(self):\n        # Test implementation\n        pass\n        \n    def test_process_data(self):\n        # Test implementation\n        pass\n        \n    def test_export_results(self):\n        # Test implementation\n        pass\n\nif __name__ == '__main__':\n    unittest.main()\n",
            "test_workflow.py": "# Tests for workflow module\n\nimport unittest\nfrom src.modules.workflow import Workflow\n\nclass TestWorkflow(unittest.TestCase):\n    def setUp(self):\n        self.workflow = Workflow()\n        \n    def test_workflow_execution(self):\n        result = self.workflow.execute_workflow()\n        self.assertEqual(result['status'], 'completed')\n\nif __name__ == '__main__':\n    unittest.main()\n",
            "__init__.py": ""
        },
        ".gitignore": "# Python\n__pycache__/\n*.py[cod]\n*$py.class\n*.so\n.Python\nbuild/\ndevelop-eggs/\ndist/\ndownloads/\neggs/\n.eggs/\nlib/\nlib64/\nparts/\nsdist/\nvar/\nwheels/\n*.egg-info/\n.installed.cfg\n*.egg\n\n# Virtual Environments\nvenv/\nenv/\nENV/\n\n# IDE specific files\n.idea/\n.vscode/\n*.swp\n*.swo\n\n# Logs\nlogs/*\n!logs/.gitkeep\n\n# Temp files\ndata/temp/*\n!data/temp/.gitkeep\n",
        "requirements.txt": "# Core RPA libraries\npyautogui==0.9.53\npython-dotenv==0.19.2\nrequests==2.27.1\npandas==1.4.1\nopenpyxl==3.0.9\nselenium==4.1.0\npywin32==303; platform_system == 'Windows'\n\n# For testing\npytest==7.0.0\npytest-cov==3.0.0\n",
        "README.md": f"# {project_name}\n\nModular/Hybrid RPA Python Automation Project\n\n## Project Structure\n\n```\n{project_name}/\n├── src/                    # Source code\n│   ├── bots/              # Entry points for RPA bots\n│   ├── config/            # Configuration files\n│   ├── modules/           # Business logic modules\n│   └── utils/             # Utility functions and helpers\n├── data/                  # Data directories\n│   ├── input/             # Input files\n│   ├── output/            # Output files\n│   └── temp/              # Temporary files\n├── logs/                  # Log files\n├── tests/                 # Test files\n├── requirements.txt       # Dependencies\n└── README.md             # Project documentation\n```\n\n## Setup\n\n1. Create a virtual environment:\n```\npython -m venv venv\nvenv\\Scripts\\activate  # Windows\nsource venv/bin/activate  # Linux/Mac\n```\n\n2. Install dependencies:\n```\npip install -r requirements.txt\n```\n\n## Usage\n\nRun the main bot:\n```\npython src/bots/main.py\n```\n\n## Testing\n\nRun tests:\n```\npython -m pytest tests/\n```\n\n## Created on\n{datetime.datetime.now().strftime('%Y-%m-%d')}\n"
    }
    
    # Create the structure
    for dir_name, content in structure.items():
        dir_path = os.path.join(project_dir, dir_name)
        
        if isinstance(content, dict):
            # If it's a dictionary, it's either a directory with subdirectories or files
            create_directory(dir_path)
            
            for sub_name, sub_content in content.items():
                sub_path = os.path.join(dir_path, sub_name)
                
                if isinstance(sub_content, dict):
                    # Handle nested directories
                    setup_nested_structure(sub_path, sub_content)
                else:
                    # It's a file
                    create_file(sub_path, sub_content)
        else:
            # It's a file at the root level
            create_file(dir_path, content)
    
    print(f"\nRPA project structure '{project_name}' created successfully!")
    print(f"Location: {project_dir}")
    print("\nRecommended next steps:")
    print("1. Navigate to your project directory")
    print(f"   cd {project_name}")
    print("2. Create a virtual environment")
    print("   python -m venv venv")
    print("3. Activate the virtual environment")
    print("   Windows: venv\\Scripts\\activate")
    print("   Linux/Mac: source venv/bin/activate")
    print("4. Install dependencies")
    print("   pip install -r requirements.txt")
    print("5. Start developing your RPA solution!")

def setup_nested_structure(base_path, structure):
    """Set up nested directory structure."""
    if os.path.splitext(base_path)[1]:  # If it has a file extension
        create_file(base_path, structure)
    else:
        create_directory(base_path)
        
        for name, content in structure.items():
            path = os.path.join(base_path, name)
            
            if isinstance(content, dict):
                setup_nested_structure(path, content)
            else:
                create_file(path, content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create an RPA project structure")
    parser.add_argument("project_name", help="Name of the RPA project")
    parser.add_argument("--directory", "-d", default=".", help="Base directory to create the project in (default: current directory)")
    
    args = parser.parse_args()
    
    setup_rpa_structure(args.directory, args.project_name)