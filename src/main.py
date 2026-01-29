from server import mcp

import stage1.github_tools
# import stage1.discord_tools
# import stage1.eve_tools
# import stage1.invman_tools

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
