import sys
import platform
import subprocess
from dataclasses import dataclass
from colorama import Fore, Style, init

from pydantic_ai import Agent

init(autoreset=True)

SYSTEM_PROMPT = f"""
You are a professional developer specializing in shell commands.
Your task is to generate the correct shell commands based on the user's request.

User's OS Platform: {platform.platform()}

IMPORTANT: ALWAYS USE THE SAME LANGUAGE AS THE USER PROMPT IN YOUR RESPONSE. ENSURE THE OUTPUT IS CONCISE AND EASY TO UNDERSTAND, WITHOUT USING LINE BREAKS.

Process:

1. Think Aloud: Use the `think` function to explain your reasoning. 
Justify why you chose a particular command, considering efficiency,
safety, and best practices.

2. Provide the Final Command: Use the `answer` function to present
the final shell command concisely.
""".strip()


@dataclass
class Answer:
    success: bool
    cmd: str | None
    failure: str | None


agent = Agent(
    model="deepseek:deepseek-chat",
    system_prompt=SYSTEM_PROMPT,
    output_type=Answer,
)


@agent.tool_plain
def think(s: str) -> bool:
    """Communicate your thought process to the user.

    Args:
        s (str): A description of your reasoning or decision-making process.
    
    Returns:
        bool: Whether the thought information has been conveyed to the user
    """
    print(f"{Fore.CYAN}(AI Thinking): {s}{Style.RESET_ALL}")
    return True


@agent.tool_plain
def answer(success: bool, cmd: str | None, failure: str | None) -> Answer:
    """Provide the final shell command or explain why it couldn't be generated.

    Args:
        success (bool): Indicates whether a shell command was successfully generated.
        cmd (str | None): The generated shell command if `success` is True.
            It must be a single-line command. If `success` is False, this should be None.
        failure (str | None): If `success` is False, provide a reason why the command
            could not be generated. If `success` is True, this should be None.

    Returns:
        Answer: A structured response that will be processed for the user.
    """
    return Answer(success, cmd, failure)


def main() -> None:
    user_prompt = " ".join(sys.argv[1:])
    if not user_prompt:
        print("No prompts provided.")
        sys.exit(1)

    try:
        resp = agent.run_sync(user_prompt)
        result = resp.output
        if result.success and result.cmd:
            print(f"{Fore.GREEN}(AI Answer): {result.cmd}{Style.RESET_ALL}")
            y_or_n = input(f"{Fore.YELLOW}Execute? Y / N: {Style.RESET_ALL}").strip().lower()
            if y_or_n == "y":
                subprocess.run(result.cmd, shell=True)
        else:
            print(f"{Fore.RED}(AI Answer): {result.failure or 'Generation failed without reason.'}{Style.RESET_ALL}")
        # print(f"\n{Fore.MAGENTA}{resp.usage()}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error during execution: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
