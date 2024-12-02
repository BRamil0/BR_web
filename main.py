import asyncio
import sys
import argparse

MINIMUM_VERSION_PYTHON = (3, 12, 0)
RECOMMENDED_VERSION_PYTHON = (3, 12, 7)

try:
    from src.logger.logger import logger
    import server
    from src.frontend import frontend
    is_whether_dependencies_established = True
except ImportError:
    server, frontend = None, None
    from src.logger.default_logger import logger
    is_whether_dependencies_established = False
    logger.log("CRITICAL", "Main | no dependencies for making applications are installed")

async def logger_check(level: str = "INFO", message: str = "") -> bool:
    if is_whether_dependencies_established:
        logger.opt(colors=True).log(level, message)
    else:
        logger.log(level, message)
    return True

async def version_checking():
    current_version = sys.version_info[:3]
    if  current_version < MINIMUM_VERSION_PYTHON:
        await logger_check("CRITICAL", f"<e>Main</e> | <c>Python version  <b>{'.'.join(map(str, current_version))}</b> is not supported. Minimum version: <b>{MINIMUM_VERSION_PYTHON}</b>.</c>")
        raise SystemExit
    elif current_version < RECOMMENDED_VERSION_PYTHON:
        await logger_check("WARNING", f"<e>Main</e> | <c>Python version  <b>{'.'.join(map(str, current_version))}</b> is not recommended. Recommended version: <b>{RECOMMENDED_VERSION_PYTHON}</b>.</c>")
        return False
    await logger_check("INFO", f"<e>Main</e> | <c>Python version <b>{'.'.join(map(str, current_version))}</b> is supported.</c>")
    return True

async def docker_function(option):
    pass

async def run_function(options):
    if is_whether_dependencies_established:
        run_list = []
        program = {"server": server.start, "f-build": frontend.build, "f-watch": frontend.watch}
        for option in options:
            if option not in run_list: run_list.append(program[option]())
        await asyncio.gather(*run_list)
        return True
    await logger_check("ERROR", "<e>Main</e> | <e><b>You have not set up dependencies for making apps.</b></e>")
    return False

async def script_function(options):
    from scripts import create_venv, create_config
    run_list = []
    scripts = {"c-venv": create_venv.create_venv, "c-config": create_config.create_configs_files}
    for option in options:
        if option not in run_list: run_list.append(scripts[option]())
    await asyncio.gather(*run_list)
    return True


async def add_arguments(parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Please select the type of application launch.")) -> argparse.Namespace:
    subparsers = parser.add_subparsers(dest="command")

    docker_parser = subparsers.add_parser("docker")
    docker_parser.add_argument("actions", choices=["start", "stop", "restart"], help="Working with Docker teams.")

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("actions", nargs='*', choices=["server", "f-build", "f-watch"], help="Run server or watch.")

    scripts_parser = subparsers.add_parser("scripts")
    scripts_parser.add_argument("actions", nargs='*', choices=["c-venv", "c-config"], help="Run scripts in the scripts folder.")
    return parser.parse_args()

async def start() -> bool:
    await version_checking()
    args = await add_arguments()

    if args.command is None:
        await logger_check("INFO", "<e>Main</e> | <c>No arguments passed, automatic start of the server.</c> <y>(<b>command</b>: run server)</y>")
        args.command = "run"; args.actions = ["server"]

    functions = {"docker": docker_function, "run": run_function, "scripts": script_function}
    if args.command in functions:
        await functions[args.command](args.actions)
    else:
        await logger_check("ERROR", "<e>Main</e> | <e><b>Unknown option.</b></e>")

    await logger_check("INFO", "<e>Main</e> | <e><b>Program finished.</b></e>")

if __name__ == "__main__":
    asyncio.run(logger_check("INFO", "<e>Main</e> | <e><b>Program started.</b></e>"))
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        asyncio.run(logger_check("INFO", "<e>Main</e> | <e><b>Program shutdown by user.</b></e>"))
    except BaseException as e:
        asyncio.run(logger_check("CRITICAL", f"<e>Main</e> | <e><b>The program has been shut down due to a critical error or unhandled exception, for more details: {e}</b></e>"))
        raise e