import asyncio
import sys
import argparse

MINIMUM_VERSION_PYTHON = (3, 12, 0)
RECOMMENDED_VERSION_PYTHON = (3, 12, 7)

try:
    from src.logger.logger import logger
    import server
    from src.backend import commands
    is_whether_dependencies_established = True
except ImportError:
    import logging
    from src.logger.default_logger import default_logger
    is_whether_dependencies_established = False
    default_logger.log(logging.CRITICAL, "Main | no dependencies for making applications are installed")
    logger = None
    class FakeServer:
        @staticmethod
        async def start():
            print("FakeServer | Starting fake server...")

    class FakeCommands:
        @staticmethod
        async def docker_start():
            print("FakeCmd | Starting fake Docker...")

        @staticmethod
        async def docker_stop():
            print("FakeCmd | Stopping fake Docker...")

        @staticmethod
        async def docker_build():
            print("FakeCmd | Building fake Docker...")

        @staticmethod
        async def docker_log():
            print("FakeCmd | Showing fake Docker logs...")

        @staticmethod
        async def frontend_build():
            print("FakeCmd | Building fake frontend...")

        @staticmethod
        async def frontend_watch():
            print("FakeCmd | Watching fake frontend...")

    server = FakeServer()
    commands = FakeCommands()

async def logger_check(level: str = "INFO", message: str = "") -> bool:
    if is_whether_dependencies_established:
        logger.opt(colors=True).log(level, message)
    else:
        level_dict = {"DEBUG": logging.DEBUG, "INFO": logging.INFO, "WARNING": logging.WARNING, "ERROR": logging.ERROR, "CRITICAL": logging.CRITICAL}
        default_logger.log(level_dict[level], message)
    return True

async def version_checking():
    current_version = sys.version_info[:3]
    if  current_version < MINIMUM_VERSION_PYTHON:
        await logger_check("CRITICAL", f"<le><b>Main</b></le> | <lc>Python version <c><b>{'.'.join(map(str, current_version))}</b></c> is <lr><b>not supported</b></lr>.</lc> | <lc>Minimum version: <c><b>{MINIMUM_VERSION_PYTHON}</b></c>.</lc>")
        raise SystemExit
    elif current_version < RECOMMENDED_VERSION_PYTHON:
        await logger_check("WARNING", f"<le><b>Main</b></le> | <lc>Python version <c><b>{'.'.join(map(str, current_version))}</b></c> is <ly><b>not recommended</b></ly>.</lc> | <lc>Recommended version: <c><b>{RECOMMENDED_VERSION_PYTHON}</b></c>.</lc>")
        return False
    await logger_check("INFO", f"<le><b>Main</b></le> | <lc>Python version <c><b>{'.'.join(map(str, current_version))}</b></c> is <lg><b>supported</b></lg>.</lc>")
    return True

async def start_function(program: dict, options: dict, ignore_package: bool = False):
    if is_whether_dependencies_established or ignore_package:
        run_list = []
        for option in options:
            if option not in run_list: run_list.append(program[option]())
        await asyncio.gather(*run_list)
        return True
    await logger_check("ERROR", "<le><b>Main</b></le> | <lr><b>You have not set up dependencies for making apps.</b></lr>")
    return False

async def docker_function(option):
    program = {"start": commands.docker_start, "stop": commands.docker_stop, "build": commands.docker_build, "log": commands.docker_log}
    await start_function(program, option)

async def database_function(option):
    program = {"start": commands.database_start, "stop": commands.database_stop}
    await start_function(program, option)

async def run_function(options):
    program = {"server": server.start, "f-build": commands.frontend_build, "f-watch": commands.frontend_watch}
    await start_function(program, options)

async def script_function(options):
    from scripts import create_venv, create_config
    scripts = {"c-venv": create_venv.create_venv, "c-config": create_config.create_configs_files}
    await start_function(scripts, options, ignore_package=True)

async def custom_error_handler(message):
    await logger_check("ERROR", f"<le><b>Argparse</b></le> | <lr>Argparse Error: <r><b>{message}</b></r></lr>")
    sys.exit(2)

async def add_arguments(parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Please select the type of application launch.", exit_on_error=False)) -> argparse.Namespace:
    subparsers = parser.add_subparsers(dest="command")

    docker_parser = subparsers.add_parser("docker")
    docker_parser.add_argument("actions", choices=["start", "stop", "build", "log"], help="Working with Docker teams.")

    database_parser = subparsers.add_parser("database")
    database_parser.add_argument("actions", choices=["start", "stop", "docker-start", "docker-stop"], help="run only the DBMS.")

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("actions", nargs='*', choices=["server", "f-build", "f-watch"], help="Run server or watch.")

    scripts_parser = subparsers.add_parser("scripts")
    scripts_parser.add_argument("actions", nargs='*', choices=["c-venv", "c-config"], help="Run scripts in the scripts folder.")
    return parser.parse_args()

async def start() -> bool:
    await version_checking()
    args = await add_arguments()

    if args.command is None and is_whether_dependencies_established:
        await logger_check("INFO", "<le><b>Main</b></le> | <lc>No arguments passed, automatic start of the <c>server</c>.</lc> <v><ly>(<b>command</b>: run server)</ly></v>")
        args.command = "run"; args.actions = ["server"]

    functions = {"docker": docker_function, "database": database_function, "run": run_function, "scripts": script_function}
    if args.command in functions:
        await functions[args.command](args.actions)
    else:
        await logger_check("ERROR", "<le><b>Main</b></le> | <lr><b>Unknown option. Write to <u>'help'</u> for more information.</b></lr>")

    await logger_check("INFO", "<le><b>Main</b></le> | <lm><b>Program finished.</b></lm>")

if __name__ == "__main__":
    asyncio.run(logger_check("INFO", "<le><b>Main</b></le> | <lm><b>Program started.</b></lm>"))
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        asyncio.run(logger_check("INFO", "<le><b>Main</b></le> | <lm><b>Program shutdown by user.</b></lm>"))
    except argparse.ArgumentError as e:
        asyncio.run(custom_error_handler(str(e)))
    except SystemExit as e:
        if e.code != 0: asyncio.run(logger_check("WARNING", f"<le><b>Main</b></le> | <ly><b>System exit triggered: <y><v>{e}</v></y></b></ly>"))
    except BaseException as e:
        print(e)
        asyncio.run(logger_check("CRITICAL", f"<le><b>Main</b></le> | <lr><b>The program has been shut down due to a critical error or unhandled exception, for more details: <r><v>{e}</v></r></b></lr>"))
        raise e