from fastmcp import FastMCP

mcp = FastMCP("add-mcp-http")

@mcp.tool
def add(a: int, b: int) -> int:
    
    return a + b

if __name__ == "__main__" :
    mcp.run(transport="http", host="0.0.0.0" , port=8080)