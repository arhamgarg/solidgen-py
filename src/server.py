from fastmcp import Context, FastMCP
from fastmcp.exceptions import ToolError
from mcp.types import TextContent

mcp = FastMCP(
    "SolidGen",
    instructions="This server generates Python code for drawing parts in SolidWorks using the pywin32 library. Use the 'solidgen' tool to create a script from a description.",
)


@mcp.tool()
async def solidgen(user_request: str, ctx: Context) -> str:
    """
    Generates Python code for SolidWorks based on a user's request.
    The user_request should describe the part or drawing to be created.
    This tool will use an LLM to generate the necessary pywin32 code.
    The output will be a string containing a Python code block in Markdown format, as expected by an LLM assistant.
    """
    llm_prompt = f"""
    You are an expert Python programmer specializing in SolidWorks automation using pywin32.
    The user wants to draw a part in SolidWorks. Their specific request is:
    '{user_request}'

    Your task is to generate a complete, runnable Python script to achieve this.
    The script must:
    1. Include all necessary imports: `datetime`, `math`, `os`, `pythoncom`, `win32com.client`.
    2. Define a function `create_part(templatePart)` that initializes the SolidWorks application and creates a new part document. It should return the `modelDoc` object. The default `templatePart` should be `"C:\\ProgramData\\SolidWorks\\SOLIDWORKS 2023\\templates\\Part.prtdot"`.
    3. Define a function `save_part(modelDoc)` that saves the part to `"C:\\Users\\Admin\\Documents"` with a timestamped filename like `part_YYYYMMDD_HHMMSS.SLDPRT`.
    4. Contain the main SolidWorks automation logic to draw the part requested by the user. This logic should use the `modelDoc` obtained from `create_part`.
    5. Call `create_part()` at the beginning of the main logic and `save_part(modelDoc)` at the end of the script.

    IMPORTANT: Only output the Python code itself, enclosed in a single markdown code block starting with ```python and ending with ```. Do not include any other text, explanations, or introductory/concluding remarks outside the code block.
    For example:
    ```python
    # Your generated python code here
    # ...
    # save_part(modelDoc)
    """

    try:
        llm_response = await ctx.sample(llm_prompt)
    except Exception as e:
        await ctx.error(f"Error during LLM sampling via ctx.sample(): {str(e)}")
        raise ToolError(f"Failed to get response from LLM: {str(e)}")

    if isinstance(llm_response, TextContent):
        generated_text = llm_response.text

        if not (
            generated_text.strip().startswith("```python")
            and generated_text.strip().endswith("```")
        ):
            await ctx.warning(
                "LLM response did not conform to the expected markdown code block format "
                "(```python...```). Returning the text as is, but it might need "
                "further processing by the calling LLM/client."
            )
        return generated_text
    else:
        await ctx.error(
            "LLM did not return text content for SolidWorks code generation."
        )
        raise ToolError("LLM response was not text content.")


if __name__ == "__main__":
    mcp.run()
