import asyncio

from src.logger.logger import logger

async def watch() -> bool:
    logger.opt(colors=True).info("<e>Frontend</e> | <e><b>Watching frontend...</b></e>")
    return await run_command("npm run watch")

async def build() -> bool:
    logger.opt(colors=True).info("<e>Frontend</e> | <e><b>Building frontend...</b></e>")
    return await run_command("npm run build")


async def run_command(command: str) -> bool:
    returncode = None
    logger.opt(colors=True).info(f"<e>Frontend</e> | <c>Starting command: <b>{command}</b></c>")

    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    async def read_stream(stream, log_func):
        while True:
            line = await stream.readline()
            if not line:
                break
            decoded_line = line.decode("utf-8").strip()
            if decoded_line:
                log_func(f"<e>Frontend</e> | {decoded_line}")

    stdout_task = asyncio.create_task(read_stream(process.stdout, logger.opt(colors=True).info))
    stderr_task = asyncio.create_task(read_stream(process.stderr, logger.opt(colors=True).error))

    try:
        returncode = await process.wait()
        await asyncio.gather(stdout_task, stderr_task)
    except asyncio.CancelledError:
        logger.opt(colors=True).info("<e>Frontend</e> | <c>Terminating the subprocess...</c>")
        process.terminate()
        await process.wait()
    finally:
        if process.returncode is None:
            logger.opt(colors=True).info("<e>Frontend</e> | <c>Force killing the subprocess...</c>")
            process.kill()
            await process.wait()

    logger.opt(colors=True).info(
        f"<e>Frontend</e> | <c>Process exited with code <b>{process.returncode}</b></c>"
    )
    return returncode == 0
