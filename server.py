import os

from fastmcp import FastMCP
from typing import Optional
from tcl_utils import send_result_to_socket, launch_hyperworks_with_tcl


mcp = FastMCP("hypermesh-tools")


@mcp.tool
def execute_hyperworks_tool(tcl_file_path: str ="merged.tcl"):
    """HyperWorks/HyperMesh 하이퍼메시를 실행시킨다.

    Args:
    HyperWorks의 Hypermesh를 실행시시키는 함수이다.
    
    Returns:
        launch_hyperworks_with_tcl()의 반환값
    """
    #code = f"ExecuteHyperworks {tcl_path}"

    return launch_hyperworks_with_tcl(tcl_file_path)

@mcp.tool
def load_model_tool(file_path: str) -> dict:
    """
    Loads a CAD model file via TCP process.

    Args:
        file_path (str): Path to the CAD model file.

    Returns:
        dict: {status, message, result}
    """
    if not file_path:
        return {
            "status": "error",
            "message": "No CAD model file path provided. Please specify the file path.",
            "result": None
        }
    if not os.path.isfile(file_path):
        return {
            "status": "error",
            "message": f"CAD model file does not exist: {file_path}",
            "result": None
        }
    try:
        code = f"LoadModel {file_path.replace(chr(92), chr(92)*2)}"
        result = send_result_to_socket(code)
        return {
            "status": "success",
            "message": f"CAD model loaded successfully: {file_path}",
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error loading CAD model: {str(e)}",
            "result": None
        }

@mcp.tool
def meshing_tool(size: float) -> dict:
    """
    Generates mesh from the loaded CAD model.

    Args:
        size (float): Desired mesh size.

    Returns:
        dict: {status, message, result}
    """
    if size is None or size <= 0:
        return {
            "status": "error",
            "message": "Mesh size not provided or invalid. Please specify a positive mesh size.",
            "result": None
        }
    try:
        code = f"Meshing {size}"
        result = send_result_to_socket(code)
        return {
            "status": "success",
            "message": f"Meshing successful with size {size}.",
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error during meshing: {str(e)}",
            "result": None
        }

@mcp.tool
def create_material_tool() -> dict:
    """
    Creates a material by sending the CreateMaterial command via socket.

    Returns:
        dict: {status, message, result}
    """
    try:
        code = "CreateMaterial"
        result = send_result_to_socket(code)
        return {
            "status": "success",
            "message": "Material created successfully.",
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error creating material: {str(e)}",
            "result": None
        }

@mcp.tool
def create_property_tool(mat_id: int) -> dict:
    """
    Creates a property by sending the CreateProperty command with material ID via socket.

    Args:
        mat_id (int): Material ID. Must be a positive integer.

    Returns:
        dict: {status, message, result}
    """
    if mat_id is None or not isinstance(mat_id, int) or mat_id <= 0:
        return {
            "status": "error",
            "message": "Material ID not provided or invalid. Please specify a positive integer for material ID.",
            "result": None
        }
    try:
        code = f"CreateProperty {mat_id}"
        result = send_result_to_socket(code)
        return {
            "status": "success",
            "message": f"Property created successfully with material ID: {mat_id}.",
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error creating property: {str(e)}",
            "result": None
        }

@mcp.tool
def assign_property_tool(prop_id: int) -> dict:
    """
    Assigns a property by sending the AssignProperty command with property ID via socket.

    Args:
        prop_id (int): Property ID. Must be a positive integer.

    Returns:
        dict: {status, message, result}
    """
    if prop_id is None or not isinstance(prop_id, int) or prop_id <= 0:
        return {
            "status": "error",
            "message": "Property ID not provided or invalid. Please specify a positive integer for property ID.",
            "result": None
        }
    try:
        code = f"AssignProperty {prop_id}"
        result = send_result_to_socket(code)
        return {
            "status": "success",
            "message": f"Property assigned successfully with property ID: {prop_id}.",
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error assigning property: {str(e)}",
            "result": None
        }

@mcp.tool
def create_eigrl_tool() -> dict:
    """
    Creates EIGRL for eigenvalue analysis by sending the CreateEIGRL command via socket.

    Returns:
        dict: {status, message, result}
    """
    try:
        code = "CreateEIGRL"
        result = send_result_to_socket(code)
        return {
            "status": "success",
            "message": "EIGRL created successfully for eigenvalue analysis.",
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error creating EIGRL: {str(e)}",
            "result": None
        }

@mcp.tool
def create_loadstep_tool(param_id: int) -> dict:
    """
    Creates a Loadstep by sending the CreateLoadstep command with parameter ID via socket.

    Args:
        param_id (int): Parameter ID. Must be a positive integer.

    Returns:
        dict: {status, message, result}
    """
    if param_id is None or not isinstance(param_id, int) or param_id <= 0:
        return {
            "status": "error",
            "message": "Parameter ID not provided or invalid. Please specify a positive integer for parameter ID.",
            "result": None
        }
    try:
        code = f"CreateLoadstep {param_id}"
        result = send_result_to_socket(code)
        return {
            "status": "success",
            "message": f"Loadstep created successfully with parameter ID: {param_id}.",
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error creating Loadstep: {str(e)}",
            "result": None
        }

import os

@mcp.tool
def export_input_deck_tool(file_path: str) -> dict:
    """
    Exports the input deck by sending the ExportInputDeck command via socket.

    Args:
        file_path (str): Path of the file to export. Must exist.

    Returns:
        dict: {status, message, result}
    """
    if not file_path:
        return {
            "status": "error",
            "message": "No file path provided. Please specify the export file path.",
            "result": None
        }
    if not os.path.isfile(file_path):
        return {
            "status": "error",
            "message": f"Export file does not exist: {file_path}",
            "result": None
        }
    try:
        code = f"ExportInputDeck {file_path.replace(chr(92), chr(92)*2)}"
        result = send_result_to_socket(code)
        return {
            "status": "success",
            "message": f"Input deck exported successfully for: {file_path}",
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error exporting input deck: {str(e)}",
            "result": None
        }

import os

@mcp.tool
def run_analysis_tool(fem_path: str) -> dict:
    """
    Runs analysis using the given FEM file path via TCP process.

    Args:
        fem_path (str): FEM file path to run the analysis.

    Returns:
        dict: {status, message, result}
    """
    if not fem_path:
        return {
            "status": "error",
            "message": "No FEM file path provided. Please specify the FEM file path.",
            "result": None
        }
    if not os.path.isfile(fem_path):
        return {
            "status": "error",
            "message": f"FEM file does not exist: {fem_path}",
            "result": None
        }
    try:
        code = f"Run {fem_path.replace(chr(92), chr(92)*2)}"
        result = send_result_to_socket(code)
        return {
            "status": "success",
            "message": f"Analysis completed successfully for: {fem_path}",
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error running analysis: {str(e)}",
            "result": None
        }


def view_top() -> dict:
    """도형을 위쪽 뷰로 변경한다."""
    code = "*view \"top\""
    try:
        result = send_result_to_socket(code)
        return {
            "status": "success",
            "message": "View changed to top.",
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error changing view to top: {str(e)}",
            "result": None
        }

@mcp.tool
def view_bottom() -> dict:
    """도형을 아래쪽 뷰로 변경한다."""
    code = "*view \"bottom\""
    try:
        result = send_result_to_socket(code)
        return {
            "status": "success",
            "message": "View changed to bottom.",
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error changing view to bottom: {str(e)}",
            "result": None
        }

@mcp.tool
def view_side() -> dict:
    """도형을 옆면 뷰로 변경한다."""
    code = "*view \"side\""
    try:
        result = send_result_to_socket(code)
        return {
            "status": "success",
            "message": "View changed to side.",
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error changing view to side: {str(e)}",
            "result": None
        }

if __name__ == "__main__":
    #mcp.run(transport="http", host="0.0.0.0", port=8080)
    mcp.run()