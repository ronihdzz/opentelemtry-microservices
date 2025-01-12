from settings import Settings
import uvicorn
from loguru import logger


if __name__ == "__main__":
    import multiprocessing
    from settings import Settings
    
    settings = Settings()

    logger.info("Starting API configuration")

    def run_api_1():
        logger.info("Starting average API at {}:{}", settings.HOST_API_AVERAGE, settings.PORT_API_AVERAGE)
        uvicorn.run("api_average:app", host=settings.HOST_API_AVERAGE, port=settings.PORT_API_AVERAGE)

    def run_api_2():
        logger.info("Starting add API at {}:{}", settings.HOST_API_ADD, settings.PORT_API_ADD)
        uvicorn.run("api_add:app", host=settings.HOST_API_ADD, port=settings.PORT_API_ADD)

    def run_api_3():
        logger.info("Starting divide API at {}:{}", settings.HOST_API_DIVIDE, settings.PORT_API_DIVIDE)
        uvicorn.run("api_divide:app", host=settings.HOST_API_DIVIDE, port=settings.PORT_API_DIVIDE)

    def run_api_4():
        logger.info("Starting exponentiation API at {}:{}", settings.HOST_API_EXPONENTIATION, settings.PORT_API_EXPONENTIATION)
        uvicorn.run("api_exponentiation:app", host=settings.HOST_API_EXPONENTIATION, port=settings.PORT_API_EXPONENTIATION)

    def run_api_5():
        logger.info("Starting standart deviation API at {}:{}", settings.HOST_API_STANDART_DEVIATION, settings.PORT_API_STANDART_DEVIATION)
        uvicorn.run("api_standart_deviation:app", host=settings.HOST_API_STANDART_DEVIATION, port=settings.PORT_API_STANDART_DEVIATION)


    processes = []
    processes.append(multiprocessing.Process(target=run_api_1))
    processes.append(multiprocessing.Process(target=run_api_2))
    processes.append(multiprocessing.Process(target=run_api_3))
    processes.append(multiprocessing.Process(target=run_api_4))
    processes.append(multiprocessing.Process(target=run_api_5))
    logger.info("Starting processes for the APIs")

    for process in processes:
        logger.info("Starting process: {}", process.name)
        process.start()

    for process in processes:
        process.join()
        logger.info("Process {} has finished", process.name)

    logger.info("All processes have finished")

