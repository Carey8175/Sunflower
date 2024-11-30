import psutil
import asyncio

import cv2
import numpy
import random
from loguru import logger
from numpy import ndarray
from paddleocr import PaddleOCR
from dataclasses import dataclass
from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.adb_device_async import AdbDeviceTcpAsync


@dataclass
class BoundingBox:
    x: int
    y: int
    width: int
    height: int

    def get_middle_coordinate(self) -> tuple[int, int]:
        """
        Get the middle coordinate of the bounding box.
        :return:
        """
        return self.x + self.width // 2, self.y + self.height // 2


@dataclass
class OcrResult(BoundingBox):
    text: str


class AdbOCR:
    def __init__(self):
        self._device: AdbDeviceTcpAsync | None = None
        self.ocr_engine = None
        self._random = random.Random()

    async def load(self, port: int, host: str = "localhost", scan_if_fail=True, language: str = 'ch') -> None:
        """
        Load the ADB connection.

        Args:
            port: The port to connect to.
            host: The host to connect to.
            scan_if_fail: Whether to scan for local devices if the connection fails.
            language: The language to use for the OCR engine.
        Returns:
        """
        task1 = asyncio.create_task(self._init_ocr_engine(language=language))
        task2 = asyncio.create_task(self._connect_device(port=port, host=host, scan_if_fail=scan_if_fail))

        await task1
        await task2

    async def _connect_device(
            self,
            port: int,
            host: str = "localhost",
            scan_if_fail: bool = True
    ) -> None:
        """
        Connect to the device.

        Args:
            port: The port to connect to.
            host: The host to connect to.
            scan_if_fail: Whether to scan for devices if the connection fails.

        Returns:
        """
        if self._device is not None:
            return

        device = AdbDeviceTcpAsync(host=host, port=port, default_transport_timeout_s=9)
        logger.debug(f"Connecting to Device[{host}:{port}]...")

        try:
            connection = await device.connect()
            if connection:
                self._device = device
                logger.info(f"Connected to Device[{host}:{port}]!")
                return
        except OSError:
            if scan_if_fail:
                logger.warning(f"[X]Failed to connect to Device[{host}:{port}].")
            else:
                logger.error(f"Failed to connect to Device[{host}:{port}].")

        # scan for devices at localhost if the connection failed
        if host == "localhost" and scan_if_fail:
            # scan the local devices
            port_found = await self._scan_local_devices()

            if port_found:
                try:
                    connection = await self._connect_device(port=port_found, host=host, scan_if_fail=False)
                    if connection:
                        self._device = device
                        logger.info(f"Connected to Device[{host}:{port_found}]!")
                        return
                except OSError:
                    logger.error(
                        f"Failed to connect to emulator, please make sure the ADB is enabled on your emulator.")

    async def _scan_local_devices(self) -> int | None:
        """
        Scan for devices at localhost.

        Returns: the open adb ports or None if no device was found.
        """
        logger.info("Scanning for open adb devices at localhost...")

        try:
            connections = [
                conn for conn in psutil.net_connections("tcp4") if conn.laddr.port >= 5555 and conn.status == "LISTEN"
            ]
        except psutil.AccessDenied:
            logger.error("Permission denied while scanning ports. Please run this script as an administrator.")
            return None

        logger.warning(f"There are {len(connections)} open ports, trying to find the abd port.")

        for conn in connections:
            logger.debug(f"Scanning port {conn.laddr.port} for ADB...")
            try:
                adb_device = AdbDeviceTcp("localhost", port=conn.laddr.port, default_transport_timeout_s=0.5)
                if adb_device.connect(read_timeout_s=0.5):
                    adb_device.close()
                    return conn.laddr.port
            # Reason for disable: The code above can throw a lot of different exceptions, this is the simplest solution.
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.debug(f"Port {conn.laddr.port} threw '{e}'.")

        logger.warning("No local device was found. Make sure ADB is enabled in your emulator's settings.")
        return None

    async def _init_ocr_engine(self, language: str = 'ch') -> None:
        """
        Initialize the OCR engine.

        Returns:
        """
        self.ocr_engine = PaddleOCR(lang=language, show_log=False)

    def is_connected(self) -> bool:
        """
        Check if the device is connected.

        Returns:
        """
        return self._device and self._device.available

    async def get_screen_size(self) -> tuple[int, int]:
        """
        Get the screen size.

        Returns:
            (width, height) of the screen.
        """
        if not self.is_connected():
            return 0, 0

        shell_output = await self._device.shell("wm size | awk 'END{print $3}'")
        return shell_output.replace("\n", "")

    async def get_screen_density(self) -> int:
        """
        Get the screen density.

        Returns:
             the number of pixels per inch.
        """
        shell_output = await self._device.shell("wm density | awk 'END{print $3}'")

        return shell_output.replace("\n", "")

    async def set_screen_size(self, width: int, height: int) -> None:
        """
        Set the screen size.

        Args:
            width: The width to set.
            height: The height to set.

        Returns:
        """
        await self._device.shell(f"wm size {width}x{height}")

    async def set_screen_density(self, density: int) -> None:
        """
        Set the screen density.

        Args:
            density: The density to set.

        Returns:
        """
        await self._device.shell(f"wm density {density}")

    async def get_memory(self) -> int:
        """
        Get the memory of the device.

        Returns:
            The memory in MB.
        """
        shell_output = await self._device.shell("cat /proc/meminfo | grep MemTotal")
        return int(shell_output.split()[1]) // 1024

    async def get_screen(self) -> ndarray | None:
        """
        Get the screen.
        But

        Returns:
            The screen as an ndarray or None if it failed.
        """
        image_bytes_str = await self._device.exec_out("screencap -p", decode=False)
        raw_image = numpy.frombuffer(image_bytes_str, dtype=numpy.uint8)
        return cv2.imdecode(raw_image, cv2.IMREAD_GRAYSCALE)

    async def click(self, x: int, y: int) -> None:
        """
        Click on the screen.

        Returns:
        """
        await self._device.shell(f"input swipe {x} {y} {x} {y} {self._random.randint(60, 120)}")

    async def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int | None = None) -> None:
        """
        Swipe on the screen.

        Args:
            x1: The x coordinate to start the swipe.
            y1: The y coordinate to start the swipe.
            x2: The x coordinate to end the swipe.
            y2: The y coordinate to end the swipe.
            duration: The duration of the swipe.

        Returns:
        """
        await self._device.shell(
            f"input swipe {x1} {y1} {x2} {y2} {self._random.randint(60, 120) if not duration else duration}")

    async def go_back(self):
        """
        Send a back key press event to the device.
        """
        await self._device.shell("input keyevent 4")

    async def get_screen_text(self, detect_area: BoundingBox | None = None, confidence=0.85) -> list[OcrResult] | None:
        """
        Get the text on the screen.

        Args:
            detect_area: The area to detect text in.
            confidence: The confidence level to use when detecting text. Defaults to 0.85.

        Returns:
            The text on the screen.
        """
        if not self.is_connected():
            logger.warning("Please use the load method to connect to the device before OCR.")
            return None

        screen = await self.get_screen()
        # crop screen according to detect_area
        if detect_area:
            screen = screen[detect_area.y:detect_area.y + detect_area.height,
                            detect_area.x:detect_area.x + detect_area.width]

        if not (result := self.ocr_engine.ocr(screen, cls=False)):
            logger.debug("No text was found on the screen.")
            return None

        ocr_results: list[OcrResult] = []

        if not (result := result[0]):
            logger.debug("No text was found on the screen.")
            return None

        for res in result:
            ocr_results.append(OcrResult(
                x=res[0][0][0],
                y=res[0][0][1],
                width=res[0][2][0] - res[0][0][0],
                height=res[0][2][1] - res[0][0][1],
                text=res[1][0]
            )) if res[1][1] > confidence else None

        return ocr_results if ocr_results else None
