import os
import uuid
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def generate_excel_report(data, sheet_names=None, filename=None):
    """
    Generate an Excel report from data.
    
    Args:
        data (list or dict): Data to include in the report. If dict, keys are sheet names.
        sheet_names (list, optional): Sheet names for the Excel file.
        filename (str, optional): Filename for the Excel file.
        
    Returns:
        str: Path to the generated Excel file.
    """
    try:
        if filename is None:
            filename = f"report_{uuid.uuid4().hex}.xlsx"
        
        file_path = os.path.join(settings.MEDIA_ROOT, 'reports', filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            if isinstance(data, dict):
                for sheet_name, sheet_data in data.items():
                    df = pd.DataFrame(sheet_data)
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            else:
                if sheet_names and len(sheet_names) > 0:
                    sheet_name = sheet_names[0]
                else:
                    sheet_name = 'Sheet1'
                
                df = pd.DataFrame(data)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        return file_path
    except Exception as e:
        logger.error(f"Error generating Excel report: {str(e)}")
        return None

def generate_csv_report(data, filename=None):
    """
    Generate a CSV report from data.
    
    Args:
        data (list): Data to include in the report.
        filename (str, optional): Filename for the CSV file.
        
    Returns:
        str: Path to the generated CSV file.
    """
    try:
        if filename is None:
            filename = f"report_{uuid.uuid4().hex}.csv"
        
        file_path = os.path.join(settings.MEDIA_ROOT, 'reports', filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        
        return file_path
    except Exception as e:
        logger.error(f"Error generating CSV report: {str(e)}")
        return None

def generate_chart(data, chart_type, x_column, y_column, title=None, filename=None):
    """
    Generate a chart from data.
    
    Args:
        data (list): Data to include in the chart.
        chart_type (str): Type of chart to generate (bar, line, pie).
        x_column (str): Column to use for x-axis.
        y_column (str): Column to use for y-axis.
        title (str, optional): Title for the chart.
        filename (str, optional): Filename for the chart.
        
    Returns:
        str: Path to the generated chart.
    """
    try:
        if filename is None:
            filename = f"chart_{uuid.uuid4().hex}.png"
        
        file_path = os.path.join(settings.MEDIA_ROOT, 'reports', 'charts', filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        df = pd.DataFrame(data)
        
        plt.figure(figsize=(10, 6))
        
        if chart_type == 'bar':
            df.plot(kind='bar', x=x_column, y=y_column)
        elif chart_type == 'line':
            df.plot(kind='line', x=x_column, y=y_column)
        elif chart_type == 'pie':
            df.plot(kind='pie', y=y_column)
        else:
            df.plot(kind='bar', x=x_column, y=y_column)
        
        if title:
            plt.title(title)
        
        plt.tight_layout()
        plt.savefig(file_path)
        plt.close()
        
        return file_path
    except Exception as e:
        logger.error(f"Error generating chart: {str(e)}")
        return None

def get_report_data_from_service(service_url, endpoint, params=None, headers=None):
    """
    Get report data from a service.
    
    Args:
        service_url (str): URL of the service.
        endpoint (str): Endpoint to call.
        params (dict, optional): Parameters to include in the request.
        headers (dict, optional): Headers to include in the request.
        
    Returns:
        dict: Response data from the service.
    """
    import requests
    
    try:
        url = f"{service_url}{endpoint}"
        
        if headers is None:
            headers = {}
        
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        return response.json()
    except Exception as e:
        logger.error(f"Error getting report data from service: {str(e)}")
        return None