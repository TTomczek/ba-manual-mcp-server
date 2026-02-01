import asyncio
import logging
import unittest

from src.rate_limiter import rate_limit


class TestRateLimiter(unittest.IsolatedAsyncioTestCase):
    async def test_rate_limit(self):

        @rate_limit(3, 5)
        async def dummy_function():
            return 1

        with self.assertLogs('src.rate_limiter', level='WARNING') as logs:
            for _ in range(5):
                result = await dummy_function()
                self.assertEqual(result, 1)

            self.assertEqual(len(logs), 2)


    async def test_not_rate_limited(self):
        @rate_limit(3, 4)
        async def dummy_function():
            return 1

        logger = logging.getLogger('src.rate_limiter')
        records = []

        class ListHandler(logging.Handler):
            def emit(self, record):
                records.append(record)

        handler = ListHandler()
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING)

        try:
            for _ in range(4):
                result = await dummy_function()
                await asyncio.sleep(1.5)
                self.assertEqual(result, 1)
            self.assertEqual(len(records), 0)
        finally:
            logger.removeHandler(handler)


if __name__ == '__main__':
    unittest.main()
