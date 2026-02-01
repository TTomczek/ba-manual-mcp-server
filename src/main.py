from server import mcp

# import stage1b.github_tools
# import stage1b.discord_tools
# import stage1b.eve_tools
import stage1b.invman_tools

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
