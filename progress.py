from time import sleep

GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"
MAGENTA = "\033[95m"


def show_banner():
    print()
    print(
        f"{CYAN}"
        " ██████╗ ██╗████████╗██████╗  █████╗ ███╗   ██╗██╗  ██╗\n"
        "██╔════╝ ██║╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║██║ ██╔╝\n"
        "██║  ███╗██║   ██║   ██████╔╝███████║██╔██╗ ██║█████╔╝\n"
        "██║   ██║██║   ██║   ██╔══██╗██╔══██║██║╚██╗██║██╔═██╗\n"
        "╚██████╔╝██║   ██║   ██║  ██║██║  ██║██║ ╚████║██║  ██╗\n"
        " ╚═════╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝"
        f"{RESET}"
    )
    print()

    print(f"{BOLD}{CYAN}          GitRank — Git Analytics Engine{RESET}")
    print(f"{YELLOW}                   bybhargav{RESET}")
    print()

def show_progress(stage: str, progress: int):
    filled = progress // 5
    bar = "█" * filled
    empty = "░" * (20 - filled)

    print(
        f"{GREEN}{BOLD}[{bar}{empty}]{RESET} "
        f"{GREEN}{BOLD}{progress}%{RESET} "
        f"{stage}"
    )
    


if __name__ == "__main__":
    show_progress("Validating repository", 10)
    sleep(1)

    show_progress("Reading commit history", 40)
    sleep(1)

    show_progress("Analyzing contributors", 70)
    sleep(1)

    show_progress("Building graph", 90)
    sleep(1)

    show_progress("Yeah. We cooked. 🔥", 100)