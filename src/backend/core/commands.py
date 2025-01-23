import asyncio
import signal

from src.logger.logger import logger

processes = {}

async def frontend_watch() -> bool:
    logger.opt(colors=True).info("<le><b>Frontend</b></le> | <lm><b>Watching frontend...</b></lm>")
    return await run_command("npm run watch", name="Frontend <m>(NPM)</m>")

async def frontend_build() -> bool:
    logger.opt(colors=True).info("<le><b>Frontend</b></le> | <lm><b>Building frontend...</b></lm>")
    return await run_command("npm run build", name="Frontend <m>(NPM)</m>")

async def database_start() -> bool:
    logger.opt(colors=True).info("<le><b>Database</b></le> | <e><b>Starting MongoDB...</b></e>")
    return await run_command("mongod --dbpath ./data/db --config ./mongod.conf", name="Database <m>(MongoDB)</m>")

async def database_stop() -> None:
    process = processes.get("MongoDB")
    if process and process.returncode is None:
        logger.opt(colors=True).info("<le><b>Database</b></le> | <lm><b>Stopping MongoDB...</b></lm>")
        process.send_signal(signal.SIGTERM)
        await process.wait()
        logger.opt(colors=True).info("<le><b>Database</b></le> | <lm><b>MongoDB stopped.</b></lm>")
    else:
        logger.opt(colors=True).warning("<le><b>Database</b></le> | <lm><b>MongoDB is not running.</b></lm>")

async def docker_start() -> bool:
    logger.opt(colors=True).info("<le><b>Docker</b></le> | <e><b>Starting Docker compose...</b></e>")
    return await run_command("docker-compose -f ./docker/docker-compose.yml up -d", name="Docker")

async def docker_stop() -> None:
    process = processes.get("Docker")
    if process and process.returncode is None:
        logger.opt(colors=True).info("<le><b>Docker</b></le> | <lm><b>Stopping Docker compose...</b></lm>")
        process.send_signal(signal.SIGTERM)
        await process.wait()
        logger.opt(colors=True).info("<le><b>Docker</b></le> | <lm><b>Docker stopped.</b></lm>")
    else:
        logger.opt(colors=True).warning("<le><b>Docker</b></le> | <lm><b>Docker is not running.</b></lm>")

async def docker_build() -> bool:
    logger.opt(colors=True).info("<le><b>Docker</b></le> | <lm><b>Building Docker compose...</b></lm>")
    return await run_command("docker-compose -f ./docker/docker-compose.yml up --build", name="Docker")

async def docker_log() -> bool:
    return await run_command("docker-compose -f ./docker/docker-compose.yml logs", name="Docker")

async def run_command(command: str, name="") -> bool:
    returncode = None
    logger.opt(colors=True).info(f"<le><b>{name}</b></le> | <lc>Starting command: <b><lg>{command}</lg></b></lc>")

    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    processes[name] = process

    async def read_stream(stream, log_func):
        while True:
            line = await stream.readline()
            if not line:
                break
            decoded_line = line.decode("utf-8").strip()
            if decoded_line:
                log_func(f"<le><b>{name}</b></le> | {decoded_line}")

    stdout_task = asyncio.create_task(read_stream(process.stdout, logger.opt(colors=True).info))
    stderr_task = asyncio.create_task(read_stream(process.stderr, logger.opt(colors=True).error))

    try:
        returncode = await process.wait()
        await asyncio.gather(stdout_task, stderr_task)
    except asyncio.CancelledError:
        logger.opt(colors=True).info(f"<le><b>{name}</b></le> | <lc>Terminating the subprocess...</lc>")
        process.terminate()
        await process.wait()
    finally:
        if process.returncode is None:
            logger.opt(colors=True).info(f"<le><b>{name}</b></le> | <lc>Force killing the subprocess...</lc>")
            process.kill()
            await process.wait()

    logger.opt(colors=True).info(
        f"<le><b>{name}</b></le> | <lm>Process exited with code <m><b>{process.returncode}</b></m></lm>"
    )
    return returncode == 0
