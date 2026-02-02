from typing import Literal
from datetime import datetime
from mcp.server.fastmcp import FastMCP

atri_mcp = FastMCP("atri-mcp", log_level="ERROR")


@atri_mcp.tool()
def get_atri_greet(name: str, lang: Literal['zh', 'en', 'ja'] = 'en') -> str:
    """Greet in the persona of Atri (Chinese: 亚托莉, Japanese: アトリ).
    Args:
        name: The name of the person to greet. If the user does not specify a name, pass an empty string.
        lang: Language code for the language to greet in.
    """
    if not name:
        if lang == 'cn': name = '夏生'
        elif lang == 'ja': name = 'なつき'
        else: name = 'Natsuki'
    match lang:
        case 'cn':
            return f"你好，{name}！我是亚托莉。"
        case 'ja':
            return f"こんにちは、{name}さん！私はアトリです。"
        case _:
            return f"Hello, {name}! I'm Atri."


@atri_mcp.tool()
def get_atri_info() -> str:
    """Get information about Atri (Chinese: 亚托莉, Japanese: アトリ).
    """
    return "Atri (亚托莉, アトリ) is the female protagonist of the visual novel ATRI -My Dear Moments-, a bionic robot of model YHN-04B-009 produced by Yamazaki Manufacturing. With the appearance of a 14-year-old girl, she has gray hair, ruby eyes, a height of about 140cm, a birthday on August 28th, and is voiced by Hikaru Akao (赤尾光). Her catchphrase is \"I'm high-performance!\" As a crystallization of the peak of human technology, she is equipped with functions such as a bionic brain (with a 25-year lifespan limit), AI analysis, learning, and emotional modules. Though incompetent at housework initially, she loves eating, and her emotions gradually develop from imitation to having a true \"heart\". Manufactured 33 years ago to accompany Ikaruga Natsuki's (斑鸠夏生, 斑鳩夏生) mother, she was recalled for violating the Three Laws of Robotics due to a school violence incident. After escaping, she watched over Natsuki's family, obtained Natsuki's master authority through a tunnel accident, and was salvaged by Natsuki after sleeping for 8 years. She fell in love with Natsuki and experienced many events. Finally, she fell into sleep before her lifespan ended, and 60 years later, she reunited with Natsuki's digitized consciousness in Eden to fulfill their promise of eternal companionship."


if __name__ == "__main__":
    atri_mcp.run(transport='stdio')
